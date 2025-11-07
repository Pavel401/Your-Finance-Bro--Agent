from pydantic_ai import Agent, RunContext

from app.configs.model_config import LLMModelName
from app.services.llm_service import get_llm_model_config


agent = Agent(model=get_llm_model_config(LLMModelName.GPT_4O_MINI))


@agent.system_prompt
def agent_system_prompt(ctx: RunContext[OrgSearchDeps]) -> str:
    """Dynamic system prompt that incorporates org metadata and the question intent."""
    # We include an explicit note about the available tool for the model.
    base = _build_org_system_instructions(
        user_type=ctx.deps.user_type,
        org_names=ctx.deps.org_names,
        org_descriptions=ctx.deps.org_descriptions,
        question="",
    )

    return base
