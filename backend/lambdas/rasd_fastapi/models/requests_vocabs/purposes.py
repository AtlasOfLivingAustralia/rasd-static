"""RASD FastAPI Purpose Restricted Vocabulary."""


# Standard
import enum


class Purpose(str, enum.Enum):
    """Purpose Restricted Vocabulary Enumeration."""
    TO_DELIVER_GOVERNMENT_SERVICES = "To deliver government services"
    TO_INFORM_GOVERNMENT_POLICIES_AND_PROGRAMS = "To inform government policies and programs"
    FOR_RESEARCH_AND_DEVELOPMENT = "For Research and development"
    FOR_COMPLIANCE_AND_OR_ENFORCEMENT_ACTIVITIES = "For compliance and / or enforcement activities"
    FOR_CONSERVATION_MANAGEMENT = "For conservation management"
    FOR_PLANNING_APPROVAL = "For planning approval"
    FOR_A_GOVERNMENT_FUNDED_GRANT_PROGRAM = "For a government-funded grant program"
    TO_INFORM_ENVIRONMENTAL_IMPACT_ASSESSMENT = "To inform environmental impact assessment"
    FOR_LAND_MANAGEMENT = "For land management"
