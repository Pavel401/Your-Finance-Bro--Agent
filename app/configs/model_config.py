# Enum class to define different LLM (Large Language Model) names
from enum import Enum


class LLMModelName(Enum):
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_3S5_TURBO = "gpt-3.5-turbo"
    GPT_4O = "gpt-4-o"
    LLAMA3 = "llama3"
    GPT_4O_MINI = "gpt-4o-mini-2024-07-18"

    # GPT-5 Models (Released August 7, 2025)
    GPT_5 = "gpt-5"  # Input: $1.25/1M tokens, Output: $10.00/1M tokens
    GPT_5_MINI = "gpt-5-mini"  # Input: $0.25/1M tokens, Output: $2.00/1M tokens

    # Gemini 2.5 Models
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite"

    # Gemini 2.0 Models
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite"


def get_model_name(model: LLMModelName):
    """
    Returns the model name for the given LLM model.

    Args:
    - model (LLMModelName): The LLM model.

    Returns:
    - str: The model name.
    """
    return model.value


# Enum class to define different embedding model names
class EmbeddingModelName(Enum):
    nomic_embed_text = "nomic-embed-text"
    text2_ada_openai = "text-embedding-ada-002"
    text_embedding_3_small = "text-embedding-3-small"
