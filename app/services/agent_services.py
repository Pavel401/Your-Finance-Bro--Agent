from pydantic_ai import Agent, RunContext

from app.configs.model_config import LLMModelName
from app.services.llm_service import get_llm_model_config


agent = Agent(model=get_llm_model_config(LLMModelName.GPT_4_TURBO))
