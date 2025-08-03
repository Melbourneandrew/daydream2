from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import uuid4

from sqlmodel import SQLModel, Field, Relationship, Index
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from .concept_model import Concept


class Dream(SQLModel, table=True):
    """
    Dream table model representing a dream entity in the database.
    Each dream has a unique UUID and creation timestamp.
    """

    __tablename__ = "dreams"

    # Database-specific field configurations
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(String(36), primary_key=True, index=True),
    )

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime, server_default=func.now(), nullable=False),
    )

    # Relationships only
    concepts: List["Concept"] = Relationship(
        back_populates="dream", cascade_delete=True
    )

    # Table arguments for additional indexes
    __table_args__ = (
        # Index on created_at in descending order for efficient recent dream queries
        Index(
            "ix_dreams_created_at_desc",
            "created_at",
        ),
    )
