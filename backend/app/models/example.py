# Example model - you can delete this file when you create your actual models

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class ExampleModel(Base):
    """
    Example SQLAlchemy model to demonstrate Alembic usage.
    Delete this when you create your actual models.
    """

    __tablename__ = "example_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<ExampleModel(id={self.id}, name='{self.name}')>"
