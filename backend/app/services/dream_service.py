import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from fastapi import Depends

from typing import Optional, List

from app.models.dream_model import Dream
from app.models.concept_model import Concept
from app.database import get_db

# Configure logger for this module
logger = logging.getLogger(__name__)


class DreamService:
    """
    Service for handling dream database operations.
    Focuses only on dream persistence, not concept generation.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_dream(self) -> Dream:
        """
        Create a new dream record in the database.

        Returns:
            Dream: The created dream

        Raises:
            SQLAlchemyError: If database operation fails
        """
        logger.info("Creating new dream record in database")
        try:
            # Create the dream record
            dream = Dream()
            self.db.add(dream)
            self.db.commit()

            # Refresh object to get updated timestamps
            self.db.refresh(dream)

            logger.info(f"Successfully created dream with id: {dream.id}")
            return dream

        except SQLAlchemyError as e:
            # Rollback transaction on database error
            logger.error(
                f"Database error while creating dream: {str(e)}", exc_info=True
            )
            self.db.rollback()
            raise e

    def get_dream_by_id(self, dream_id: str) -> Optional[Dream]:
        """
        Get a dream by its UUID, including its associated concepts.

        Args:
            dream_id: UUID of the dream to retrieve

        Returns:
            Dream: The dream with its concepts sorted in reverse-chronological order, or None if not found

        Raises:
            SQLAlchemyError: If database operation fails
        """
        logger.info(f"Retrieving dream by id: {dream_id}")
        try:
            # Query dream first
            dream = self.db.query(Dream).filter(Dream.id == dream_id).first()

            if dream:
                # Manually load concepts in reverse-chronological order
                from app.models.concept_model import Concept

                concepts = (
                    self.db.query(Concept)
                    .filter(Concept.dream_id == dream_id)
                    .order_by(Concept.created_at.desc())
                    .all()
                )
                # Replace the concepts relationship with our ordered list
                dream.concepts = concepts

                logger.info(
                    f"Successfully retrieved dream {dream_id} with {len(dream.concepts)} concepts (reverse-chronological order)"
                )
            else:
                logger.warning(f"Dream with id {dream_id} not found in database")

            return dream

        except SQLAlchemyError as e:
            logger.error(
                f"Database error while retrieving dream {dream_id}: {str(e)}",
                exc_info=True,
            )
            raise e

    def create_concept(
        self,
        dream_id: str,
        content: str,
        parent1_id: Optional[str] = None,
        parent2_id: Optional[str] = None,
    ) -> Concept:
        """
        Create a new concept record in the database.

        Args:
            dream_id: UUID of the dream this concept belongs to
            content: Content of the concept
            parent1_id: Optional UUID of the first parent concept
            parent2_id: Optional UUID of the second parent concept

        Returns:
            Concept: The created concept

        Raises:
            SQLAlchemyError: If database operation fails
        """
        logger.info(f"Creating concept for dream {dream_id}: {content[:50]}...")
        try:
            # Create the concept record
            concept = Concept(
                content=content,
                dream_id=dream_id,
                parent1_id=parent1_id,
                parent2_id=parent2_id,
            )
            self.db.add(concept)
            self.db.commit()

            # Refresh object to get updated timestamps and ID
            self.db.refresh(concept)

            logger.info(
                f"Successfully created concept {concept.id} for dream {dream_id}"
            )
            return concept

        except SQLAlchemyError as e:
            # Rollback transaction on database error
            logger.error(
                f"Database error while creating concept for dream {dream_id}: {str(e)}",
                exc_info=True,
            )
            self.db.rollback()
            raise e

    def get_random_concepts(self, dream_id: str, count: int = 2) -> List[Concept]:
        """
        Get random concepts from a dream using PostgreSQL's random() function.

        Args:
            dream_id: UUID of the dream to sample concepts from
            count: Number of random concepts to retrieve (default: 2)

        Returns:
            List[Concept]: List of random concepts from the dream

        Raises:
            SQLAlchemyError: If database operation fails
            ValueError: If not enough concepts exist for the dream
        """
        logger.info(f"Getting {count} random concepts from dream {dream_id}")
        try:
            # Query random concepts for the dream using PostgreSQL's random() function
            concepts = (
                self.db.query(Concept)
                .filter(Concept.dream_id == dream_id)
                .order_by(func.random())
                .limit(count)
                .all()
            )

            # Validate we have enough concepts
            if len(concepts) < count:
                logger.warning(
                    f"Dream {dream_id} has only {len(concepts)} concepts, but {count} were requested"
                )
                raise ValueError(
                    f"Dream {dream_id} has only {len(concepts)} concepts, but {count} were requested"
                )

            logger.info(
                f"Successfully retrieved {len(concepts)} random concepts from dream {dream_id}"
            )
            return concepts

        except SQLAlchemyError as e:
            logger.error(
                f"Database error while getting random concepts from dream {dream_id}: {str(e)}",
                exc_info=True,
            )
            raise e

    def list_dreams_with_labels(
        self, offset: int = 0, limit: int = 20
    ) -> tuple[List[Dream], int]:
        """
        List dreams with their initial concepts for labeling, ordered by creation date (newest first).

        Args:
            offset: Number of dreams to skip (for pagination)
            limit: Maximum number of dreams to return

        Returns:
            tuple: (List of dreams with initial concepts loaded, total count of dreams)

        Raises:
            SQLAlchemyError: If database operation fails
        """
        logger.info(f"Listing dreams with labels (offset={offset}, limit={limit})")
        try:
            # Get total count of dreams
            total_count = self.db.query(Dream).count()

            # Query dreams ordered by creation date (newest first)
            dreams = (
                self.db.query(Dream)
                .order_by(Dream.created_at.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )

            # For each dream, load only the initial concepts (those without parents)
            for dream in dreams:
                initial_concepts = (
                    self.db.query(Concept)
                    .filter(
                        Concept.dream_id == dream.id,
                        Concept.parent1_id.is_(None),
                        Concept.parent2_id.is_(None),
                    )
                    .order_by(Concept.created_at.asc())
                    .limit(2)  # We expect exactly 2 initial concepts
                    .all()
                )
                # Replace the concepts relationship with just the initial concepts
                dream.concepts = initial_concepts

            logger.info(
                f"Successfully retrieved {len(dreams)} dreams with initial concepts (total: {total_count})"
            )
            return dreams, total_count

        except SQLAlchemyError as e:
            logger.error(
                f"Database error while listing dreams: {str(e)}",
                exc_info=True,
            )
            raise e


# Dependency injection function
def get_dream_service(db: Session = Depends(get_db)) -> DreamService:
    """
    Dependency injection function for DreamService.

    Args:
        db: Database session injected by FastAPI

    Returns:
        DreamService: Configured dream service instance
    """
    return DreamService(db)
