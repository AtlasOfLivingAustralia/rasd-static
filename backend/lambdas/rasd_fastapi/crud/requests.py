"""RASD FastAPI CRUD for Data Access Requests."""


# Standard
import functools
import operator
import uuid

# Third-Party
import boto3
import boto3.dynamodb.conditions as con
import pydantic

# Local
from rasd_fastapi import types
from rasd_fastapi import utils
from rasd_fastapi.core import settings
from rasd_fastapi.crud import base
from rasd_fastapi.crud import metadata as metadata_crud
from rasd_fastapi.crud import organisations as org_crud
from rasd_fastapi.emails import email
from rasd_fastapi.models import requests as req_models
from rasd_fastapi.schemas import audit as audit_schemas
from rasd_fastapi.schemas import auth as auth_schemas
from rasd_fastapi.schemas import requests as req_schemas

# Typing
from typing import Any, Optional


class DataAccessRequestCRUD(
    base.CRUDBase[
        req_models.DataAccessRequest,
        req_schemas.DataAccessRequestCreate,
        req_schemas.DataAccessRequestUpdate,
        types.rasd.RASDIdentifier,
    ],
):
    """Data Access Request CRUD Abstraction."""

    def create_with_user(
        self,
        db_session: boto3.Session,
        *,
        obj_in: req_schemas.DataAccessRequestCreate,
        user: auth_schemas.User,
    ) -> req_models.DataAccessRequest:
        """Creates a Data Access Request for a User in the database.

        Args:
            db_session (boto3.Session): Database session to use.
            obj_in (req_schemas.DataAccessRequestCreate): Data to create item with.
            user (auth_schemas.User): User to create DataAccessRequest for.

        Returns:
            req_models.DataAccessRequest: Created DataAccessRequest in the database.
        """
        # Retrieve Metadata for Data Access Request
        # Duplicates are removed by casting the list of IDs to a set
        metadata = [
            utils.unwrap_or_404(
                value=metadata_crud.metadata.get(db_session, pk=metadata_id),
            ) for metadata_id in set(obj_in.metadata_ids)
        ]

        # Extract Custodian IDs from Metadata
        # Duplicates are removed via set comprehension, then casting to a list
        custodian_ids = list({m.organisation_id for m in metadata})

        # Retrieve Custodian Organisations for Metadata
        # Dictionary is a mapping of Organisation IDs to Organisation Objects
        custodian_orgs = {
            custodian_id: utils.unwrap_or_404(
                value=org_crud.organisation.get(db_session, pk=custodian_id),
            ) for custodian_id in custodian_ids
        }

        # Retrieve User Organisation
        user_org = org_crud.organisation.get(db_session, pk=user.organisation_id)

        # Check Organisation
        if not user_org:
            # Error
            raise ValueError(
                f"User associated with non-existant Organisation: '{user.organisation_id}'"
            )

        # Generate Data Access Request ID
        # This must be generated ahead of time for the Dataset Requests
        identifier=types.rasd.RASDIdentifier.generate()

        # Create Audit Log Entry
        log_entry = audit_schemas.AuditLogEntry(
            action=audit_schemas.Action.CREATED,
            by=user.email,
        )

        # Create Dataset Requests
        dataset_requests = [
            req_models.DatasetRequest(
                id=identifier.generate_sub(index),
                metadata_id=m.id,
                metadata_title=m.title,
                metadata_data_source_doi=m.data_source_doi,
                metadata_data_source_url=m.data_source_url,
                custodian_id=m.organisation_id,
                custodian_name=custodian_orgs[m.organisation_id].name,
                custodian_email=custodian_orgs[m.organisation_id].email,
                audit=[log_entry],
            ) for (index, m) in enumerate(metadata, start=1)
        ]

        # Allow super class to handle the Creation
        req = super().create(
            db_session,
            obj_in=obj_in,
            id=identifier,
            dataset_requests=dataset_requests,
            custodian_ids=custodian_ids,
            requestor_id=user.id,
            requestor_given_name=user.given_name,
            requestor_family_name=user.family_name,
            requestor_email=user.email,
            requestor_organisation_id=user_org.id,
            requestor_organisation_name=user_org.name,
            requestor_organisation_email=user_org.email,
        )

        # Send Created Emails
        email.access_request_created.send(
            to_addresses=[req.requestor_email, req.requestor_organisation_email],
            given_name=req.requestor_given_name,
            family_name=req.requestor_family_name,
            request_id=req.id,
            rasd_support_email=settings.SETTINGS.RASD_SUPPORT_EMAIL,
        )
        for dataset_request in req.dataset_requests:
            # Send!
            email.dataset_request_created.send(
                to_addresses=dataset_request.custodian_email,
                project_title=req.project_title,
                request_id=dataset_request.id,
                rasd_support_email=settings.SETTINGS.RASD_SUPPORT_EMAIL,
            )

        # Return
        return req

    def get_dataset_request(
        self,
        *,
        db_obj: req_models.DataAccessRequest,
        pk: types.rasd.RASDIdentifier,
    ) -> Optional[req_models.DatasetRequest]:
        """Finds a DatasetRequest inside the provided DataAccessRequest.

        Args:
            db_obj (req_models.DataAccessRequest): DataAccessRequest to search.
            pk (types.rasd.RASDIdentifier): Primary key of the DatasetRequest.

        Returns:
            Optional[req_models.DatasetRequest]: DatasetRequest if found.
        """
        # Loop through Dataset Requests
        for dataset_request in db_obj.dataset_requests:
            # Check Identifier
            if dataset_request.id == pk:
                # Found!
                return dataset_request

        # Not found
        return None

    def censor_for_custodian(
        self,
        user: auth_schemas.User,
        *access_requests: req_models.DataAccessRequest,
    ) -> None:
        """Censors the provided DataAccessRequests for a given Custodian.

        Censoring is a two stage process:
            1. Remove all of the `custodian_ids` that are *not* the provided
               user's Organisation.
            2. Remove all of the `dataset_requests` that do *not* involve the
               provided user's Organisation.

        This prevents any leak of information regarding the other Custodians
        involved in the Data Access Request.

        Note that this censoring is done *in-place*, and nothing is returned.

        Args:
            user (auth_schemas.User): Custodian user to censor for.
            *access_requests (req_models.DataAccessRequest): Data Access
                Requests to be censored.
        """
        # Loop through Data Access Requests
        for access_request in access_requests:
            # Remove unrelated Custodian IDs
            access_request.custodian_ids = [user.organisation_id]

            # Remove unrelated Dataset Requests
            access_request.dataset_requests = [
                d for d in access_request.dataset_requests if d.custodian_id == user.organisation_id
            ]

    def update_dataset_request(
        self,
        db_session: boto3.Session,
        *,
        db_obj: req_models.DataAccessRequest,
        dataset_request: req_models.DatasetRequest,
        obj_in: req_schemas.DatasetRequestUpdate,
        **kwargs: Any,
    ) -> req_models.DatasetRequest:
        """Updates the DatasetRequest inside the provided DataAccessRequest.

        Args:
            db_session (boto3.Session): Database session to use.
            db_obj (req_models.DataAccessRequest): DataAccessRequest to update.
            dataset_request (req_models.DatasetRequest): DatasetRequest to update.
            obj_in (req_schemas.DatasetRequestUpdate): Update data.
            kwargs (Any): Extra data required for update.

        Returns:
            req_models.DatasetRequest: Updated DatasetRequest.
        """
        # Construct Updated Dataset Request
        updated_data = dataset_request.dict() | obj_in.dict(exclude_unset=True) | kwargs  # Merge dictionaries
        updated_dataset_request = req_models.DatasetRequest.parse_obj(updated_data)  # Re-parse to re-run any validation

        # Replace Dataset Request Object within Data Access Request
        db_obj.dataset_requests = [
            updated_dataset_request if d.id == updated_dataset_request.id else d
            for d in db_obj.dataset_requests
        ]

        # Check if the Data Access Request is now Done
        if self.is_done(db_obj) and not db_obj.completed_at:
            # Set the `completed_at` Timestamp
            db_obj.completed_at = utils.utcnow()

            # Send Completed Email
            email.access_request_completed.send(
                to_addresses=[
                    db_obj.requestor_email,
                    db_obj.requestor_organisation_email,
                    settings.SETTINGS.EMAIL_ADMIN_INBOX,
                ],
                given_name=db_obj.requestor_given_name,
                family_name=db_obj.requestor_family_name,
                project_title=db_obj.project_title,
                request_id=db_obj.id,
                rasd_support_email=settings.SETTINGS.RASD_SUPPORT_EMAIL,
                rasd_url=settings.SETTINGS.RASD_URL,
            )

        # Update Data Access Request in Database
        self.update(
            db_session,
            db_obj=db_obj,
            obj_in=req_schemas.DataAccessRequestUpdate(),  # Dummy object - required for update
        )

        # Return
        return updated_dataset_request

    def transition(
        self,
        db_session: boto3.Session,
        *,
        db_obj: req_models.DataAccessRequest,
        dataset_request: req_models.DatasetRequest,
        from_status: req_models.Status,
        to_status: req_models.Status,
        action: audit_schemas.Action,
        actioned_by: pydantic.EmailStr,
    ) -> req_models.DatasetRequest:
        """Transitions a DatasetRequest from one status to another.

        This method reduces the duplication of effort and boilerplate required
        to transition a DatasetRequest between different statuses.

        Args:
            db_session (boto3.Session): Database session to use.
            db_obj (req_models.DataAccessRequest): DataAccessRequest to transition.
            dataset_request (req_models.DatasetRequest): DatasetRequest to transition.
            from_status (req_models.Status): The initial required status of the DatasetRequest.
            to_status (req_models.Status): The status the DatasetRequest will transition to.
            action (audit_schemas.Action): The action to add to the audit log.
            actioned_by (pydantic.EmailStr): The email address of the actioning user.

        Returns:
            req_models.DatasetRequest: Transitioned DatasetRequest.
        """
        # Check current status
        if dataset_request.status != from_status:
            # Error
            raise ValueError(f"Dataset Request cannot transition from '{dataset_request.status}' -> {to_status}")

        # Update and Return Dataset Request in Database
        return self.update_dataset_request(
            db_session,
            db_obj=db_obj,
            dataset_request=dataset_request,
            obj_in=req_schemas.DatasetRequestUpdate(),  # Dummy object - required for update
            status=to_status,
            audit=[*dataset_request.audit, audit_schemas.AuditLogEntry(action=action, by=actioned_by)]
        )

    def is_done(
        self,
        db_obj: req_models.DataAccessRequest,
    ) -> bool:
        """Checks whether a Data Access Request is done.

        Args:
            db_obj (req_models.DataAccessRequest): DataAccessRequest to check.

        Returns:
            bool: Whether the Data Access Request is done.
        """
        # Check and Return
        # Currently, a Data Access Request is considered "done" if *all* of its
        # child Dataset Requests have a status of `COMPLETE` or `DECLINED`.
        return all(
            d.status in (req_models.Status.COMPLETE, req_models.Status.DECLINED)
            for d in db_obj.dataset_requests
        )

    def acknowledge(
        self,
        db_session: boto3.Session,
        *,
        db_obj: req_models.DataAccessRequest,
        dataset_request: req_models.DatasetRequest,
        actioned_by: pydantic.EmailStr,
    ) -> req_models.DatasetRequest:
        """Acknowledges a Dataset Request.

        Args:
            db_session (boto3.Session): Database session to use.
            db_obj (req_models.DataAccessRequest): DataAccessRequest to acknowledge.
            dataset_request (req_models.DatasetRequest): DatasetRequest to acknowledge.
            actioned_by (pydantic.EmailStr): The email address of the actioning user.

        Returns:
            req_models.DatasetRequest: Acknowledged Dataset Request.
        """
        # Transition Dataset Request
        dataset_request = self.transition(
            db_session,
            db_obj=db_obj,
            dataset_request=dataset_request,
            from_status=req_models.Status.NEW,
            to_status=req_models.Status.ACKNOWLEDGED,
            action=audit_schemas.Action.ACKNOWLEDGED,
            actioned_by=actioned_by,
        )

        # Send Acknowledge Email
        email.dataset_request_acknowledged.send(
            to_addresses=db_obj.requestor_email,
            given_name=db_obj.requestor_given_name,
            family_name=db_obj.requestor_family_name,
            project_title=db_obj.project_title,
            request_id=dataset_request.id,
            rasd_support_email=settings.SETTINGS.RASD_SUPPORT_EMAIL,
        )

        # Return
        return dataset_request

    def approve(
        self,
        db_session: boto3.Session,
        *,
        db_obj: req_models.DataAccessRequest,
        dataset_request: req_models.DatasetRequest,
        actioned_by: pydantic.EmailStr,
    ) -> req_models.DatasetRequest:
        """Approves a Dataset Request.

        Args:
            db_session (boto3.Session): Database session to use.
            db_obj (req_models.DataAccessRequest): DataAccessRequest to approve.
            dataset_request (req_models.DatasetRequest): DatasetRequest to approve.
            actioned_by (pydantic.EmailStr): The email address of the actioning user.

        Returns:
            req_models.DatasetRequest: Approved Dataset Request.
        """
        # Transition Dataset Request
        dataset_request = self.transition(
            db_session,
            db_obj=db_obj,
            dataset_request=dataset_request,
            from_status=req_models.Status.ACKNOWLEDGED,
            to_status=req_models.Status.APPROVED,
            action=audit_schemas.Action.APPROVED,
            actioned_by=actioned_by,
        )

        # Send Approve Email
        email.dataset_request_approved.send(
            to_addresses=db_obj.requestor_email,
            given_name=db_obj.requestor_given_name,
            family_name=db_obj.requestor_family_name,
            request_id=dataset_request.id,
            rasd_support_email=settings.SETTINGS.RASD_SUPPORT_EMAIL,
        )

        # Return
        return dataset_request

    def decline(
        self,
        db_session: boto3.Session,
        *,
        db_obj: req_models.DataAccessRequest,
        dataset_request: req_models.DatasetRequest,
        actioned_by: pydantic.EmailStr,
    ) -> req_models.DatasetRequest:
        """Declines a Dataset Request.

        Args:
            db_session (boto3.Session): Database session to use.
            db_obj (req_models.DataAccessRequest): DataAccessRequest to decline.
            dataset_request (req_models.DatasetRequest): DatasetRequest to decline.
            actioned_by (pydantic.EmailStr): The email address of the actioning user.

        Returns:
            req_models.DatasetRequest: Declined Dataset Request.
        """
        # Transition Dataset Request
        dataset_request = self.transition(
            db_session,
            db_obj=db_obj,
            dataset_request=dataset_request,
            from_status=req_models.Status.ACKNOWLEDGED,
            to_status=req_models.Status.DECLINED,
            action=audit_schemas.Action.DECLINED,
            actioned_by=actioned_by,
        )

        # Send Decline Email
        email.dataset_request_declined.send(
            to_addresses=db_obj.requestor_email,
            given_name=db_obj.requestor_given_name,
            family_name=db_obj.requestor_family_name,
            request_id=dataset_request.id,
            rasd_framework_url=settings.SETTINGS.RASD_FRAMEWORK_URL,
            rasd_support_email=settings.SETTINGS.RASD_SUPPORT_EMAIL,
        )

        # Return
        return dataset_request

    def agreement_sent(
        self,
        db_session: boto3.Session,
        *,
        db_obj: req_models.DataAccessRequest,
        dataset_request: req_models.DatasetRequest,
        actioned_by: pydantic.EmailStr,
    ) -> req_models.DatasetRequest:
        """Agreement Sent for a Dataset Request.

        Args:
            db_session (boto3.Session): Database session to use.
            db_obj (req_models.DataAccessRequest): DataAccessRequest to agree.
            dataset_request (req_models.DatasetRequest): DatasetRequest to agree.
            actioned_by (pydantic.EmailStr): The email address of the actioning user.

        Returns:
            req_models.DatasetRequest: Agreement Sent Dataset Request.
        """
        # Transition Dataset Request
        dataset_request = self.transition(
            db_session,
            db_obj=db_obj,
            dataset_request=dataset_request,
            from_status=req_models.Status.APPROVED,
            to_status=req_models.Status.DATA_AGREEMENT_SENT,
            action=audit_schemas.Action.DATA_AGREEMENT_SENT,
            actioned_by=actioned_by,
        )

        # Send Agreement Sent Email
        email.dataset_request_agreement.send(
            to_addresses=db_obj.requestor_email,
            given_name=db_obj.requestor_given_name,
            family_name=db_obj.requestor_family_name,
            request_id=dataset_request.id,
            rasd_support_email=settings.SETTINGS.RASD_SUPPORT_EMAIL,
        )

        # Return
        return dataset_request

    def complete(
        self,
        db_session: boto3.Session,
        *,
        db_obj: req_models.DataAccessRequest,
        dataset_request: req_models.DatasetRequest,
        actioned_by: pydantic.EmailStr,
    ) -> req_models.DatasetRequest:
        """Completes a Dataset Request.

        Args:
            db_session (boto3.Session): Database session to use.
            db_obj (req_models.DataAccessRequest): DataAccessRequest to complete.
            dataset_request (req_models.DatasetRequest): DatasetRequest to complete.
            actioned_by (pydantic.EmailStr): The email address of the actioning user.

        Returns:
            req_models.DatasetRequest: Completed Dataset Request.
        """
        # Transition Dataset Request
        dataset_request = self.transition(
            db_session,
            db_obj=db_obj,
            dataset_request=dataset_request,
            from_status=req_models.Status.DATA_AGREEMENT_SENT,
            to_status=req_models.Status.COMPLETE,
            action=audit_schemas.Action.COMPLETE,
            actioned_by=actioned_by,
        )

        # Send Complete Email
        email.dataset_request_completed.send(
            to_addresses=db_obj.requestor_email,
            given_name=db_obj.requestor_given_name,
            family_name=db_obj.requestor_family_name,
            request_id=dataset_request.id,
            rasd_support_email=settings.SETTINGS.RASD_SUPPORT_EMAIL,
            rasd_url=settings.SETTINGS.RASD_URL,
        )

        # Return
        return dataset_request

    def build_filter(
        self,
        active_only: bool = True,
        requestor_id: Optional[uuid.UUID] = None,
        custodian_id: Optional[uuid.UUID] = None,
    ) -> Optional[con.ConditionBase]:
        """Builds the filter for the Data Access Requests table.

        Each of the provided values is combined into a single filter using a
        logical AND. That is, all of the supplied filter values must match in
        an underlying Data Access request instance for the filter to return
        them.

        The interface that `boto3` provides for constructing DynamoDB filters
        does not cater very well for dynamic filter generation. As such, the
        syntax used to generate the filter below is slightly obscure. In order
        to be terse we utilise functional concepts like the `reduce` method to
        combine individual filters.

        Args:
            active_only (bool): Filter for `active` only Data Access Requests.
            requestor_id (Optional[uuid.UUID]): Filter results based on `requestor_id`.
            custodian_id (Optional[uuid.UUID]): Filter results based on `custodian_id`.

        Returns:
            Optional[con.ConditionBase]: Possible built filter.
        """
        # Generate Filters
        # Here we construct all of the required filters in a list.
        # Based on the input data, the items in this list will either be an
        # individually constructed filter (if a value is supplied) or `None`.
        filters = [
            # `active` filter - `active` must equal `True`
            con.Attr("active").eq(True) if active_only else None,
            # `requestor_id` filter - `requestor_id` must equal the provided UUID
            con.Attr("requestor_id").eq(str(requestor_id)) if requestor_id else None,
            # `custodian_id` filter - `custodian_ids` must contain the provided UUID
            con.Attr("custodian_ids").contains(str(custodian_id)) if custodian_id else None
        ]

        # Next, we remove all of the `None`s from the filters list
        # This removes any of the filters that a value was not supplied for
        filters = [f for f in filters if f]

        # Finally, we reduce the list of filters to a single filter where all
        # of the individual filters must be true (i.e., logical AND).
        combined_filter = functools.reduce(operator.and_, filters) if filters else None

        # Return
        return combined_filter


# Instantiate Data Access Request CRUD Singleton
data_access_request = DataAccessRequestCRUD(
    model=req_models.DataAccessRequest,
    table=settings.SETTINGS.AWS_DYNAMODB_TABLE_ACCESS_REQUESTS,
    pk="id",
)
