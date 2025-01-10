"""Unit tests for metadata model."""


# Standard
import pytest

# Local
from rasd_fastapi.models import metadata
from tests import conftest


def test_metadata_format() -> None:
    """Basic test to check expected data formats are successfully parsed."""
    # Load Data
    data = conftest.load_data_json("metadata.json")

    # Parse Data
    metadata.RASDMetadata.parse_obj(data)


@pytest.mark.parametrize(
    "invalid_date",
    [
        "December 17th 1997",  # Wrong format
        "17/12/1997",          # Wrong format
        "12-12-1997",          # Wrong format
    ],
)
def test_invalid_date_entries(invalid_date: str) -> None:
    """Validates date format and range checking for ISO8601Date class.

    Args:
        invalid_date (str): date in a format that is expected to fail validation
    """
    # Load Data
    data = conftest.load_data_json("metadata.json")

    # Replace Date with an Invalid Date
    data["temporal_coverage_from"] = invalid_date

    # Assert Error is Raised
    with pytest.raises(ValueError, match=r".*temporal_coverage_from.*"):
        # Parse Data
        metadata.RASDMetadata.parse_obj(data)


@pytest.mark.parametrize(
    "valid_doi",
    [
        "10.1000/123456",
        "10.1038/issn.1476-4687",
        "10.978.86123/45678",
        "10.1001/doiurl210.1002/doiurl3 10.1003/doiurl4\n10.1004/doiurl5",
    ],
)
def test_valid_doi_entries(valid_doi: str) -> None:
    """Validates acceptance of true positive entries for DataSourceDOI class.

    Three example DOIs from https://www.doi.org/the-identifier/resources/handbook/2_numbering/
    One example DOI from the developers' imagination.

    Args:
        valid_doi (str): DOI entry that is known to be valid
    """
    # Load Data
    data = conftest.load_data_json("metadata.json")

    # Replace DOI with Unit Test DOI
    data["data_source_doi"] = valid_doi

    # Parse Data
    metadata.RASDMetadata.parse_obj(data)


@pytest.mark.parametrize(
    "invalid_doi",
    [
        "10,1000/123456",
        "10.1038.issn.1476-4687",
        "10/978.86123/45678",
        "120.1001/doiurl210.1002/doiurl3 10.1003/doiurl4\n10.1004/doiurl5",
    ],
)
def test_invalid_doi_entries(invalid_doi: str) -> None:
    """Validates refusal of true negative entries for DataSourceDOI class.

    Three example DOIs intentionally mistyped from https://www.doi.org/the-identifier/resources/handbook/2_numbering/
    One example DOI from the developers' imagination.

    Args:
        invalid_doi (str): DOI entry that is known to be invalid
    """
    # Load Data
    data = conftest.load_data_json("metadata.json")

    # Replace DOI with Unit Test DOI
    data["data_source_doi"] = invalid_doi

    # Assert Error is Raised
    with pytest.raises(ValueError, match=r".*data_source_doi.*"):
        # Parse Data
        metadata.RASDMetadata.parse_obj(data)
