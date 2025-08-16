"""Data models for the CDSS backend."""

from typing import List
from pydantic import BaseModel


class PatientData(BaseModel):
    """
    Schema representing a patient's key information.

    Fields can be extended to include additional structured clinical data such
    as vital signs, laboratory results or FHIR resources.
    """

    patient_id: str
    age: int
    gender: str
    symptoms: List[str]


class RecommendationRequest(PatientData):
    """
    Request model for the recommendation endpoint.  It inherits from
    PatientData but may be extended in the future.
    """

    pass


class RecommendationResponse(BaseModel):
    """
    Response model for the recommendation endpoint.
    """

    patient_id: str
    query: str
    snippet: str
    explanation: str
