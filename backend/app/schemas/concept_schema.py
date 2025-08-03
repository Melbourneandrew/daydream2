from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ConceptResponse(BaseModel):
    """
    Response model for Concept API operations.
    Represents a persisted concept with all its database fields.
    """

    id: str = Field(..., description="UUID of the concept")
    content: str = Field(..., description="Content of the concept")
    parent1_id: Optional[str] = Field(
        None, description="UUID of the first parent concept"
    )
    parent2_id: Optional[str] = Field(
        None, description="UUID of the second parent concept"
    )
    dream_id: str = Field(..., description="UUID of the dream this concept belongs to")
    created_at: datetime = Field(
        ..., description="ISO timestamp when the concept was created"
    )

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility
