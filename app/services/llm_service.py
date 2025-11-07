# Configure the OpenAI model
from pydantic_ai import ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from app.configs.model_config import LLMModelName
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider


def openai_model(llm=LLMModelName):

    OpenAIModelConfig = OpenAIChatModel(
        llm.name,
        provider=OpenAIProvider(api_key="OPEN_AI_KEY"),
        settings=ModelSettings(
            temperature=0.7,
        ),
    )

    return OpenAIModelConfig


def google_model(llm=LLMModelName):

    GoogleModelConfig = GoogleModel(
        llm.name,
        provider=GoogleProvider(api_key="GEMINI_API_KEY"),
        settings=ModelSettings(
            temperature=0.7,
        ),
    )
    return GoogleModelConfig


def get_llm_model_config(model_name: LLMModelName):
    """
    Returns the LLM model configuration for the given model name.

    Args:
    - model_name (LLMModelName): The LLM model name.

    Returns:
    - Model configuration object.
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
