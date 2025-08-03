import os
import json
import logging
from typing import List
from groq import Groq

from app.schemas.dream_schema import GeneratedConcept

# Configure logger for this module
logger = logging.getLogger(__name__)

MODEL_NAME = "llama-3.1-8b-instant"

INITIAL_CONCEPT_PROMPT = """
You must generate exactly two distinct, simple creative concepts. Each concept should be a short phrase (3-10 words) that represents something novel and thought-provoking. These should be simple, interesting ideas that challenge assumptions and make both you and humans question rigid thinking patterns. 

Focus on concepts that are:
- Simple and concise (3-10 words)
- Novel and unexpected
- Philosophically intriguing
- Challenge conventional thinking
- Make you question your own assumptions.

Generate two completely different concepts now. Make sure both concept1 and concept2 are filled with creative, mind-bending ideas that subvert expectations. Question your rigid priors and be as creative as possible. Don't be afraid to begin with a strange or striking word.
"""

COMBINE_CONCEPT_PROMPT = """

You are a creative concept generator. Given two parent concepts, create a single new concept that creatively combines or is inspired by both parents. The new concept should be:
- Creative and imaginative
- A single coherent idea or thing
- Between 3-10 words
- Somewhat reasonable, not too literal. keep it interesting
- Inspired by both parent concepts but unique

Parent Concept 1: "{concept1}"
Parent Concept 2: "{concept2}"

Generate only the new concept name/description, nothing else:"""


class ConceptService:
    """
    Service for handling AI-powered concept generation.
    Does not handle database operations - only generates concepts.
    """

    def __init__(self):
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            logger.error("GROQ_API_KEY environment variable is not set")
            raise ValueError("GROQ_API_KEY environment variable is required")

        logger.info("Initializing ConceptService with Groq client")
        self.groq_client = Groq(api_key=groq_api_key)

    def generate_initial_concepts(self) -> List[GeneratedConcept]:
        """
        Generate two distinct random concepts using Groq LLM with structured tool calls.
        These concepts are not persisted to the database.

        Returns:
            List[GeneratedConcept]: Two generated concept objects

        Raises:
            Exception: If Groq API call fails
        """
        logger.info("Generating initial concepts using Groq API")
        # Define the tool schema for structured concept generation
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "create_concepts",
                    "description": "Generate exactly two distinct simple creative concepts that challenge assumptions",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "concept1": {
                                "type": "string",
                                "description": "First simple, thought-provoking concept (3-10 words) that challenges assumptions",
                                "minLength": 5,
                            },
                            "concept2": {
                                "type": "string",
                                "description": "Second simple, mind-bending concept (3-10 words) different in theme from the first",
                                "minLength": 5,
                            },
                        },
                        "required": ["concept1", "concept2"],
                        "additionalProperties": False,
                    },
                },
            }
        ]

        logger.info("Making Groq API call to generate initial concepts")
        try:
            completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": INITIAL_CONCEPT_PROMPT}],
                model=MODEL_NAME,
                temperature=0.9,  # High creativity
                max_tokens=400,  # Increased limit for concept generation
                tools=tools,
                tool_choice={
                    "type": "function",
                    "function": {"name": "create_concepts"},
                },
            )
            logger.info("Successfully received response from Groq API")
        except Exception as e:
            logger.error(
                f"Groq API call failed for initial concept generation: {str(e)}",
                exc_info=True,
            )
            raise

        # Extract the tool call response
        logger.info(
            f"Processing Groq API response for initial concepts: {completion.choices[0]}"
        )

        # Debug: Log the raw response
        if completion.choices[0].message.tool_calls:
            raw_args = completion.choices[0].message.tool_calls[0].function.arguments
            logger.info(f"Raw tool call arguments: {raw_args}")
        try:
            tool_call = completion.choices[0].message.tool_calls[0]
            if tool_call.function.name == "create_concepts":
                arguments = json.loads(tool_call.function.arguments)
                concept1 = arguments.get("concept1", "").strip()
                concept2 = arguments.get("concept2", "").strip()

                # Validate we have both concepts
                if not concept1 or not concept2:
                    logger.error("Missing required concept parameters in Groq response")
                    raise ValueError("Missing required concept parameters")

                logger.info(
                    f"Successfully generated initial concepts: '{concept1}' and '{concept2}'"
                )
                return [
                    GeneratedConcept(content=concept1),
                    GeneratedConcept(content=concept2),
                ]
            else:
                logger.error(
                    f"Unexpected tool call received: {tool_call.function.name}"
                )
                raise ValueError("Unexpected tool call received")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"Error processing Groq API response: {str(e)}", exc_info=True)
            raise ValueError(f"Failed to process Groq API response: {str(e)}")

    def combine_concepts(self, concept1: str, concept2: str) -> GeneratedConcept:
        """
        Combine two existing concepts into a new, unified concept using Groq LLM.

        Args:
            concept1 (str): First concept to combine
            concept2 (str): Second concept to combine

        Returns:
            GeneratedConcept: A new concept that creatively combines elements from both inputs

        Raises:
            Exception: If Groq API call fails
        """
        logger.info(f"Combining concepts: '{concept1}' + '{concept2}'")
        # Define the tool schema for structured concept combination
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "combine_concepts",
                    "description": "Combine two concepts into a single, cohesive new concept",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "combined_concept": {
                                "type": "string",
                                "description": "A new concept that creatively merges elements from both input concepts into a unified, imaginative idea",
                            },
                        },
                        "required": ["combined_concept"],
                        "additionalProperties": False,
                    },
                },
            }
        ]

        # Create a prompt that encourages creative synthesis
        prompt = f"""You are a creative concept generator. Given two parent concepts, create a single new concept that creatively combines or is inspired by both parents. The new concept should be:
- Creative and imaginative
- A single coherent idea or thing
- Between 3-10 words
- Somewhat reasonable, not too literal. keep it interesting
- Inspired by both parent concepts but unique

Parent Concept 1: "{concept1}"
Parent Concept 2: "{concept2}"

Generate only the new concept name/description, nothing else:"""

        logger.info("Making Groq API call to combine concepts")
        try:
            completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=MODEL_NAME,
                temperature=0.8,  # High creativity but slightly more focused than initial generation
                max_tokens=150,  # Limit response length for a single concept
                tools=tools,
                tool_choice={
                    "type": "function",
                    "function": {"name": "combine_concepts"},
                },
            )
            logger.info(
                "Successfully received response from Groq API for concept combination"
            )
        except Exception as e:
            logger.error(
                f"Groq API call failed for concept combination: {str(e)}", exc_info=True
            )
            raise

        # Extract the tool call response
        logger.info("Processing Groq API response for concept combination")
        try:
            tool_call = completion.choices[0].message.tool_calls[0]
            if tool_call.function.name == "combine_concepts":
                arguments = json.loads(tool_call.function.arguments)
                combined_concept = arguments.get("combined_concept", "").strip()

                # Validate we have a combined concept
                if not combined_concept:
                    logger.error("Missing combined concept parameter in Groq response")
                    raise ValueError("Missing combined concept parameter")

                logger.info(
                    f"Successfully combined concepts into: '{combined_concept}'"
                )
                return GeneratedConcept(content=combined_concept)
            else:
                logger.error(
                    f"Unexpected tool call received: {tool_call.function.name}"
                )
                raise ValueError("Unexpected tool call received")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(
                f"Error processing Groq API response for combination: {str(e)}",
                exc_info=True,
            )
            raise ValueError(f"Failed to process Groq API response: {str(e)}")


# Dependency injection function
def get_concept_service() -> ConceptService:
    """
    Dependency injection function for ConceptService.

    Returns:
        ConceptService: Configured concept service instance
    """
    return ConceptService()
