import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError


from app.services.dream_service import DreamService, get_dream_service
from app.services.concept_service import ConceptService, get_concept_service
from app.schemas.dream_schema import (
    DreamCreateResponse,
    DreamGetResponse,
    DreamStartRequest,
    DreamStartResponse,
    DreamContinueResponse,
    DreamListResponse,
    DreamSummary,
)
from app.schemas.concept_schema import ConceptResponse


# Create router with prefix and tags
router = APIRouter(prefix="/v1/dream", tags=["dreams"])

# Configure logger for this module
logger = logging.getLogger(__name__)


@router.get("/new", response_model=DreamCreateResponse)
async def create_new_dream(
    concept_service: ConceptService = Depends(get_concept_service),
) -> DreamCreateResponse:
    """
    Generate two initial AI-generated concepts for a new dream.

    This endpoint:
    - Generates two distinct random concepts using Groq LLM (not persisted)
    - Returns the generated concepts for user review/editing
    - No dream record is created at this stage

    Returns:
        DreamCreateResponse: The generated concepts

    Raises:
        HTTPException: 500 if concept generation fails
    """

    logger.info("Generating initial concepts for new dream")

    try:
        # Generate concepts (not persisted to database)
        logger.info("Generating initial concepts using ConceptService")
        concepts = concept_service.generate_initial_concepts()
        logger.info(f"Successfully generated {len(concepts)} initial concepts")

        # Return structured response
        return DreamCreateResponse(concepts=concepts)

    except Exception as e:
        # General error (including Groq API failures)
        logger.error(
            f"General error while generating concepts: {str(e)}", exc_info=True
        )
        raise HTTPException(
            status_code=500, detail=f"Failed to generate concepts: {str(e)}"
        )


@router.get("/list", response_model=DreamListResponse)
async def list_dreams(
    offset: int = Query(0, ge=0, description="Number of dreams to skip"),
    limit: int = Query(
        20, ge=1, le=100, description="Maximum number of dreams to return"
    ),
    dream_service: DreamService = Depends(get_dream_service),
) -> DreamListResponse:
    """
    List dreams with pagination, ordered by creation date (newest first).

    Each dream includes a label derived from the first word of its initial concepts.
    Initial concepts are those without parent concepts.

    Args:
        offset: Number of dreams to skip (for pagination)
        limit: Maximum number of dreams to return (1-100)

    Returns:
        DreamListResponse: List of dream summaries with pagination info

    Raises:
        HTTPException: 500 if database error occurs
    """

    logger.info(f"Listing dreams with offset={offset}, limit={limit}")

    try:
        # Get dreams with initial concepts from service
        dreams, total_count = dream_service.list_dreams_with_labels(offset, limit)

        # Convert to response format with labels
        dream_summaries = []
        for dream in dreams:
            # Create label from first word of each initial concept
            label_parts = []
            for concept in dream.concepts:
                first_word = (
                    concept.content.split()[0] if concept.content.strip() else "Unknown"
                )
                label_parts.append(first_word)

            # Join with space or use fallback
            label = " ".join(label_parts) if label_parts else "Unlabeled"

            dream_summaries.append(
                DreamSummary(id=dream.id, created_at=dream.created_at, label=label)
            )

        # Determine if there are more dreams
        has_more = (offset + limit) < total_count

        logger.info(
            f"Successfully listed {len(dream_summaries)} dreams (total: {total_count}, has_more: {has_more})"
        )

        return DreamListResponse(
            dreams=dream_summaries, has_more=has_more, total_count=total_count
        )

    except SQLAlchemyError as e:
        # Database-specific error
        logger.error(f"Database error while listing dreams: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Database error occurred while listing dreams: {str(e)}",
        )
    except Exception as e:
        # General error
        logger.error(f"General error while listing dreams: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list dreams: {str(e)}")


@router.get("/{dream_id}", response_model=DreamGetResponse)
async def get_dream(
    dream_id: str,
    dream_service: DreamService = Depends(get_dream_service),
) -> DreamGetResponse:
    """
    Get a dream and its associated concepts by UUID.

    Args:
        dream_id: UUID of the dream to retrieve

    Returns:
        DreamGetResponse: The dream and its associated concepts

    Raises:
        HTTPException: 404 if dream not found, 500 if database error occurs
    """

    logger.info(f"Retrieving dream with id: {dream_id}")

    try:
        # Get dream from database
        dream = dream_service.get_dream_by_id(dream_id)

        if not dream:
            logger.warning(f"Dream with id {dream_id} not found")
            raise HTTPException(
                status_code=404, detail=f"Dream with id {dream_id} not found"
            )

        logger.info(
            f"Successfully retrieved dream {dream_id} with {len(dream.concepts)} concepts"
        )

        # Convert concepts to response format
        concept_responses = [
            ConceptResponse.model_validate(concept) for concept in dream.concepts
        ]

        # Return structured response
        return DreamGetResponse(dream=dream, concepts=concept_responses)

    except SQLAlchemyError as e:
        # Database-specific error
        logger.error(
            f"Database error while retrieving dream {dream_id}: {str(e)}", exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Database error occurred while retrieving dream: {str(e)}",
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        # General error
        logger.error(
            f"General error while retrieving dream {dream_id}: {str(e)}", exc_info=True
        )
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve dream: {str(e)}"
        )


@router.post("/start", response_model=DreamStartResponse)
async def start_dream(
    request: DreamStartRequest,
    dream_service: DreamService = Depends(get_dream_service),
    concept_service: ConceptService = Depends(get_concept_service),
) -> DreamStartResponse:
    """
    Start a dream by creating a dream record, two initial concepts, and generating a combined concept.

    This endpoint:
    - Creates a new dream record in the database
    - Creates two initial concept records in the database
    - Generates a combined concept using the ConceptService
    - Creates a concept record for the generated combined concept
    - Returns success status and dream ID

    Args:
        request: DreamStartRequest containing concept_1 and concept_2

    Returns:
        DreamStartResponse: Success status and dream ID

    Raises:
        HTTPException: 500 if creation fails
    """

    logger.info("Starting new dream with provided concepts")

    try:
        # Create the dream record
        logger.info("Creating dream record in database")
        dream = dream_service.create_dream()
        logger.info(f"Successfully created dream with id: {dream.id}")

        # Create the two initial concept records
        logger.info("Creating initial concept records")
        concept1 = dream_service.create_concept(dream.id, request.concept_1)
        concept2 = dream_service.create_concept(dream.id, request.concept_2)
        logger.info(f"Created initial concepts: {concept1.id}, {concept2.id}")

        # Generate a combined concept using the ConceptService
        logger.info("Generating combined concept")
        generated_concept = concept_service.combine_concepts(
            request.concept_1, request.concept_2
        )
        logger.info(f"Generated combined concept: {generated_concept.content}")

        # Create a concept record for the generated combined concept
        # The combined concept has both initial concepts as parents
        combined_concept = dream_service.create_concept(
            dream_id=dream.id,
            content=generated_concept.content,
            parent1_id=concept1.id,
            parent2_id=concept2.id,
        )
        logger.info(f"Created combined concept record: {combined_concept.id}")

        return DreamStartResponse(success=True, dream_id=str(dream.id))

    except SQLAlchemyError as e:
        # Database-specific error
        logger.error(
            f"Database error while starting dream: {str(e)}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=500,
            detail=f"Database error occurred while starting dream: {str(e)}",
        )
    except Exception as e:
        # General error (including Groq API failures)
        logger.error(
            f"General error while starting dream: {str(e)}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=f"Failed to start dream: {str(e)}")


@router.post("/{dream_id}/continue", response_model=DreamContinueResponse)
async def continue_dream(
    dream_id: str,
    dream_service: DreamService = Depends(get_dream_service),
    concept_service: ConceptService = Depends(get_concept_service),
) -> DreamContinueResponse:
    """
    Continue a dream by sampling 2 random concepts and combining them.

    This endpoint:
    - Validates that the dream exists
    - Samples 2 random concepts from the dream using PostgreSQL's random() function
    - Generates a combined concept using the ConceptService
    - Creates a concept record for the generated combined concept
    - Returns success status

    Args:
        dream_id: UUID of the dream to continue

    Returns:
        DreamContinueResponse: Success status

    Raises:
        HTTPException: 404 if dream not found, 400 if insufficient concepts, 500 if operation fails
    """

    logger.info(f"Continuing dream with id: {dream_id}")

    try:
        # Validate that the dream exists
        dream = dream_service.get_dream_by_id(dream_id)
        if not dream:
            logger.warning(f"Dream with id {dream_id} not found for continuing")
            raise HTTPException(
                status_code=404, detail=f"Dream with id {dream_id} not found"
            )

        logger.info(f"Dream {dream_id} validated successfully for continuation")

        # Sample 2 random concepts from the dream
        logger.info("Sampling 2 random concepts from dream")
        random_concepts = dream_service.get_random_concepts(dream_id, count=2)
        logger.info(
            f"Sampled concepts: {random_concepts[0].id} ({random_concepts[0].content}), {random_concepts[1].id} ({random_concepts[1].content})"
        )

        # Generate a combined concept using the ConceptService
        logger.info("Generating combined concept from sampled concepts")
        generated_concept = concept_service.combine_concepts(
            random_concepts[0].content, random_concepts[1].content
        )
        logger.info(f"Generated combined concept: {generated_concept.content}")

        # Create a concept record for the generated combined concept
        # The combined concept has both sampled concepts as parents
        combined_concept = dream_service.create_concept(
            dream_id=dream_id,
            content=generated_concept.content,
            parent1_id=random_concepts[0].id,
            parent2_id=random_concepts[1].id,
        )
        logger.info(f"Created combined concept record: {combined_concept.id}")

        return DreamContinueResponse(success=True)

    except ValueError as e:
        # Insufficient concepts or other validation error
        logger.error(f"Validation error while continuing dream {dream_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        # Database-specific error
        logger.error(
            f"Database error while continuing dream {dream_id}: {str(e)}", exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Database error occurred while continuing dream: {str(e)}",
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        # General error (including Groq API failures)
        logger.error(
            f"General error while continuing dream {dream_id}: {str(e)}", exc_info=True
        )
        raise HTTPException(
            status_code=500, detail=f"Failed to continue dream: {str(e)}"
        )
