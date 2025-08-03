from typing import List, Optional
from pydantic import BaseModel, Field

from datetime import datetime

# Import the models for clean API serialization
from app.models.dream_model import Dream
from app.schemas.concept_schema import ConceptResponse


class GeneratedConcept(BaseModel):
    """
    Schema for AI-generated concepts that haven't been persisted yet.
    """

    content: str = Field(..., description="The generated concept content")


class DreamCreateResponse(BaseModel):
    """
    Response model for Dream creation API.
    Returns only generated (non-persisted) concepts.
    """

    concepts: List[GeneratedConcept] = Field(
        ..., description="List of AI-generated concepts (not yet persisted)"
    )


class DreamGetResponse(BaseModel):
    """
    Response model for Dream get API.
    Returns the dream and its associated persisted concepts.
    """

    dream: Dream = Field(..., description="The dream")
    concepts: List[ConceptResponse] = Field(
        ..., description="List of concepts associated with this dream"
    )


class DreamStartRequest(BaseModel):
    """
    Request model for starting a dream with two initial concepts.
    """

    concept_1: str = Field(..., description="First initial concept content")
    concept_2: str = Field(..., description="Second initial concept content")


class DreamStartResponse(BaseModel):
    """
    Response model for Dream start API.
    Returns success status and dream ID.
    """

    success: bool = Field(..., description="Whether the dream was started successfully")
    dream_id: str = Field(..., description="UUID of the created dream")


class DreamContinueResponse(BaseModel):
    """
    Response model for Dream continue API.
    Returns success status.
    """

    success: bool = Field(
        ..., description="Whether the dream was continued successfully"
    )


class DreamSummary(BaseModel):
    """
    Summary model for a dream with its initial concepts for labeling.
    """

    id: str = Field(..., description="UUID of the dream")
    created_at: datetime = Field(..., description="When the dream was created")
    label: str = Field(..., description="Label derived from initial concepts")


class DreamListResponse(BaseModel):
    """
    Response model for listing dreams with pagination.
    """

    dreams: List[DreamSummary] = Field(..., description="List of dream summaries")
    has_more: bool = Field(..., description="Whether there are more dreams to load")
    total_count: int = Field(..., description="Total number of dreams available")
