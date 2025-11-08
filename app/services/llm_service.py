# Configure the OpenAI model
import os
from pydantic_ai import ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from app.configs.model_config import LLMModelName
from app.services.envManager import get_env_variable


def openai_model(llm: LLMModelName) -> OpenAIChatModel:
    """
    Create and configure an OpenAI model instance.

    Args:
        llm: The LLM model name from LLMModelName enum

    Returns:
        Configured OpenAIChatModel instance

    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set
    """
    api_key = get_env_variable("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set. "
            "Please set it before using OpenAI models."
        )

    return OpenAIChatModel(
        llm.value,
        provider=OpenAIProvider(api_key=api_key),
        settings=ModelSettings(temperature=0.7),
    )


def google_model(llm: LLMModelName) -> GoogleModel:
    """
    Create and configure a Google Gemini model instance.

    Args:
        llm: The LLM model name from LLMModelName enum

    Returns:
        Configured GoogleModel instance

    Raises:
        ValueError: If GOOGLE_API_KEY environment variable is not set
    """
    api_key = get_env_variable("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is not set. "
            "Please set it before using Google Gemini models."
        )

    return GoogleModel(
        llm.value,
        provider=GoogleProvider(api_key=api_key),
        settings=ModelSettings(temperature=0.7),
    )


def get_llm_model_config(model_name: LLMModelName):
    """
    Returns the LLM model configuration for the given model name.

    Args:
        model_name: The LLM model name from LLMModelName enum

    Returns:
        Model configuration object (OpenAIChatModel or GoogleModel)

    Raises:
        ValueError: If model name is unsupported or required API key is missing
    """
    if model_name in {
        LLMModelName.GPT_4_TURBO,
        LLMModelName.GPT_3S5_TURBO,
        LLMModelName.GPT_4O,
        LLMModelName.GPT_4O_MINI,
        LLMModelName.GPT_5,
        LLMModelName.GPT_5_MINI,
    }:
        return openai_model(model_name)
    elif model_name in {
        LLMModelName.GEMINI_2_5_PRO,
        LLMModelName.GEMINI_2_5_FLASH,
        LLMModelName.GEMINI_2_5_FLASH_LITE,
        LLMModelName.GEMINI_2_0_FLASH,
        LLMModelName.GEMINI_2_0_FLASH_LITE,
    }:
        return google_model(model_name)
    else:
        raise ValueError(f"Unsupported model name: {model_name}")
