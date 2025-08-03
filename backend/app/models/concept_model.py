from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import uuid4

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import (
    Column,
    DateTime,
    Text,
    ForeignKey,
    Index,
    CheckConstraint,
    String,
)
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from .dream_model import Dream


class Concept(SQLModel, table=True):
    """
    Concept table model representing a concept within a dream in the database.
    Each concept can have up to two parent concepts and belongs to a dream.
    """

    __tablename__ = "concepts"

    # Database-specific field configurations
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(String(36), primary_key=True, index=True),
    )

    content: str = Field(
        sa_column=Column(Text, nullable=False),
        description="Content of the concept",
    )

    parent1_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(36), ForeignKey("concepts.id"), nullable=True),
        description="UUID of the first parent concept",
    )

    parent2_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(36), ForeignKey("concepts.id"), nullable=True),
        description="UUID of the second parent concept",
    )

    dream_id: str = Field(
        sa_column=Column(
            String(36),
            ForeignKey("dreams.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        description="UUID of the dream this concept belongs to",
    )

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime, server_default=func.now(), nullable=False),
        description="ISO timestamp when the concept was created",
    )

    # Relationships only
    dream: Optional["Dream"] = Relationship(back_populates="concepts")
    parent1: Optional["Concept"] = Relationship(
        sa_relationship_kwargs={
            "remote_side": "Concept.id",
            "foreign_keys": "Concept.parent1_id",
        }
    )
    parent2: Optional["Concept"] = Relationship(
        sa_relationship_kwargs={
            "remote_side": "Concept.id",
            "foreign_keys": "Concept.parent2_id",
        }
    )
