"""RASD FastAPI CRUD Base."""


# Third-Party
import boto3
import boto3.dynamodb.conditions
import fastapi.encoders

# Local
from rasd_fastapi.models import base as models_base
from rasd_fastapi.schemas import base as schemas_base
from rasd_fastapi.schemas import pagination

# Typing
from typing import Any, Optional, Generic, TypeVar


# TypeVars
ModelType = TypeVar("ModelType", bound=models_base.BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=schemas_base.BaseSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=schemas_base.BaseSchema)
PrimaryKeyType = TypeVar("PrimaryKeyType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, PrimaryKeyType]):
    """CRUD Base Abstraction."""

    # Filter Shortcuts
    ActiveOnly = boto3.dynamodb.conditions.Attr("active").eq(True)

    def __init__(
        self,
        model: type[ModelType],
        table: str,
        pk: str,
    ) -> None:
        """Instantiates the CRUD abstraction.

        Provides CRUD objects with default method to Create, Read, Update and
        Delete models (CRUD).

        Args:
            model (type[ModelType]): CRUD model.
            table (str): Table that the model is in.
            pk (str): Primary key of the table.
        """
        # Instance Variables
        self.model = model
        self.table = table
        self.pk = pk

    def get(
        self,
        db_session: boto3.Session,
        *,
        pk: PrimaryKeyType,
    ) -> Optional[ModelType]:
        """Retrieves an item from the database using its primary key.

        Args:
            db_session (boto3.Session): Database session to use.
            pk (PrimaryKeyType): Primary key for item to retrieve.

        Returns:
            Optional[ModelType]: Retrieved item if it exists, else None.
        """
        # Create Resource and Table
        resource = db_session.resource("dynamodb")
        table = resource.Table(self.table)

        # Retrieve Raw Item from Database
        response = table.get_item(Key={self.pk: str(pk)})
        item = response.get("Item")

        # Check if Item Exists
        if not item:
            return None

        # Parse from Raw Item
        model = self.model.parse_obj(item)

        # Return
        return model

    def scan(
        self,
        db_session: boto3.Session,
        *,
        filter: Optional[boto3.dynamodb.conditions.ConditionBase] = None,  # noqa: A002
        limit: Optional[int] = None,
        cursor: Optional[PrimaryKeyType] = None,
    ) -> pagination.PaginatedResult[ModelType]:
        """Scans for items in the database matching the supplied filters.

        Args:
            db_session (boto3.Session): Database session to use.
            filter (Optional[boto3.dynamodb.conditions.ConditionBase]): Optional
                filters to use.
            limit (Optional[int]): Number of items to limit to.
            cursor (Optional[PrimaryKeyType]): Cursor for pagination.

        Returns:
            list[ModelType]: List of retrieved items if applicable.
        """
        # Create Resource and Table
        resource = db_session.resource("dynamodb")
        table = resource.Table(self.table)

        # Construct Keyword Args for Scan
        filters = {"FilterExpression": filter} if filter else {}
        start_key = {"ExclusiveStartKey": {self.pk: str(cursor)}} if cursor else {}

        # Scan the Database
        response = table.scan(
            **filters,  # type: ignore[arg-type]
            **start_key,  # type: ignore[arg-type]
        )

        # Check if we need to keep scanning
        while limit and response["Count"] < limit and "LastEvaluatedKey" in response:
            # We need to keep scanning!
            next_response = table.scan(
                **filters,  # type: ignore[arg-type]
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )

            # Add the new results into the original response
            response["Count"] += next_response["Count"]
            response["Items"] += next_response["Items"]
            response["LastEvaluatedKey"] = next_response["LastEvaluatedKey"]

        # Check if we went over the limit
        if limit and response["Count"] > limit:
            # Truncate the response
            response["Count"] = limit
            response["Items"] = response["Items"][:limit]
            response["LastEvaluatedKey"] = {self.pk: response["Items"][-1][self.pk]}

        # Extract Data
        count = response["Count"]
        items = response["Items"]
        next_cursor = response.get("LastEvaluatedKey", {}).get(self.pk)

        # Parse Models from Raw Items
        models = [self.model.parse_obj(obj) for obj in items]

        # Construct Paginated Result
        page = pagination.PaginatedResult(
            count=count,
            cursor=next_cursor,  # type: ignore[arg-type]
            results=models,
        )

        # Return
        return page

    def create(
        self,
        db_session: boto3.Session,
        *,
        obj_in: CreateSchemaType,
        **kwargs: Any,
    ) -> ModelType:
        """Creates an item in the database.

        Args:
            db_session (boto3.Session): Database session to use.
            obj_in (CreateSchemaType): Data to create item with.
            kwargs (Any): Extra data required for creation.

        Returns:
            ModelType: Created item in the database.
        """
        # Construct Create Data
        obj_in_data = obj_in.dict() | kwargs  # Merge dictionaries

        # Construct Database Model
        db_obj = self.model.parse_obj(obj_in_data)

        # Encode Database Model
        db_encoded = fastapi.encoders.jsonable_encoder(db_obj)

        # Create Resource and Table
        resource = db_session.resource("dynamodb")
        table = resource.Table(self.table)

        # Create Item in Database
        table.put_item(Item=db_encoded)

        # Return
        return db_obj

    def update(
        self,
        db_session: boto3.Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        **kwargs: Any,
    ) -> ModelType:
        """Creates an item in the database.

        Args:
            db_session (boto3.Session): Database session to use.
            db_obj (ModelType): Item to update.
            obj_in (UpdateSchemaType): Data to update item with.
            kwargs (Any): Extra data required for creation.

        Returns:
            ModelType: Updated item in the database.
        """
        # Construct Updated Item
        updated_data = db_obj.dict() | obj_in.dict(exclude_unset=True) | kwargs  # Merge dictionaries
        updated_db_obj = self.model.parse_obj(updated_data)  # Re-parse to re-run any validation

        # Encode Updated Database Model
        db_encoded = fastapi.encoders.jsonable_encoder(updated_db_obj)

        # Create Resource and Table
        resource = db_session.resource("dynamodb")
        table = resource.Table(self.table)

        # Create Item in Database
        table.put_item(Item=db_encoded)

        # Return
        return updated_db_obj

    def delete(
        self,
        db_session: boto3.Session,
        *,
        pk: PrimaryKeyType,
    ) -> Optional[ModelType]:
        """Deletes an item in the database.

        Args:
            db_session (boto3.Session): Database session to use.
            pk (PrimaryKeyType): Primary key for item to delete.

        Returns:
            Optional[ModelType]: Deleted item if it exists, else None.
        """
        # Retrieve Item
        item = self.get(db_session, pk=pk)

        # Check if Item Exists
        if not item:
            return None

        # Create Resource and Table
        resource = db_session.resource("dynamodb")
        table = resource.Table(self.table)

        # Delete Item
        table.delete_item(Key={self.pk: str(pk)})

        # Return
        return item

    def deactivate(
        self,
        db_session: boto3.Session,
        *,
        pk: PrimaryKeyType,
    ) -> Optional[ModelType]:
        """Deactivates an item in the database.

        Args:
            db_session (boto3.Session): Database session to use.
            pk (PrimaryKeyType): Primary key for item to deactivate.

        Returns:
            ModelType: Deactivated item if it exists, else None.
        """
        # Retrieve Item
        item = self.get(db_session, pk=pk)

        # Check if Item Exists
        if not item:
            return None

        # Deactivate
        item.active = False

        # Encode Database Model
        db_encoded = fastapi.encoders.jsonable_encoder(item)

        # Create Resource and Table
        resource = db_session.resource("dynamodb")
        table = resource.Table(self.table)

        # Create Item in Database
        table.put_item(Item=db_encoded)

        # Return
        return item

    def reactivate(
        self,
        db_session: boto3.Session,
        *,
        pk: PrimaryKeyType,
    ) -> Optional[ModelType]:
        """Reactivates an item in the database.

        Args:
            db_session (boto3.Session): Database session to use.
            pk (PrimaryKeyType): Primary key for item to reactivate.

        Returns:
            ModelType: Reactivated item if it exists, else None.
        """
        # Retrieve Item
        item = self.get(db_session, pk=pk)

        # Check if Item Exists
        if not item:
            return None

        # Reactivate
        item.active = True

        # Encode Database Model
        db_encoded = fastapi.encoders.jsonable_encoder(item)

        # Create Resource and Table
        resource = db_session.resource("dynamodb")
        table = resource.Table(self.table)

        # Create Item in Database
        table.put_item(Item=db_encoded)

        # Return
        return item
