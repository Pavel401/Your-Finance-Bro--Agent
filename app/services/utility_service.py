from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelRequest, ModelResponse, UserPromptPart, TextPart
from typing import List, AsyncIterator, Tuple
import re

from app.configs.model_config import LLMModelName
from app.model.agent_model import ChatMessage
from app.services.finance_service import flatten_finance_info
from app.services.llm_service import get_llm_model_config
from app.model.finance_model import FinanceInfo


def convert_chat_history_to_messages(chat_history: List[ChatMessage]) -> list:
    """
    Convert chat history to PydanticAI message format.

    Args:
        chat_history: List of ChatMessage objects

    Returns:
        List of ModelMessage objects for PydanticAI
    """
    messages = []
    for msg in chat_history:
        if msg.role == "user":
            messages.append(ModelRequest(parts=[UserPromptPart(content=msg.content)]))
        elif msg.role == "assistant":
            messages.append(ModelResponse(parts=[TextPart(content=msg.content)]))
    return messages


def is_finance_related_query(query: str) -> Tuple[bool, str]:
    """
    Validate if a user query is related to personal finance topics.
    This acts as a guardrail to prevent off-topic conversations.

    Args:
        query: The user's query string

    Returns:
        Tuple of (is_valid, redirect_message)
        - is_valid: True if query is finance-related, False otherwise
        - redirect_message: Message to send if query is off-topic
    """
    query_lower = query.lower().strip()

    # Finance-related keywords (positive indicators)
    finance_keywords = [
        # Money & spending
        "money",
        "spend",
        "spending",
        "expense",
        "cost",
        "price",
        "paid",
        "payment",
        "rupee",
        "inr",
        "₹",
        "rupees",
        "dollar",
        "currency",
        # Banking & accounts
        "account",
        "balance",
        "bank",
        "transaction",
        "transfer",
        "deposit",
        "withdraw",
        "credit",
        "debit",
        "hdfc",
        "icici",
        "sbi",
        "axis",
        # Budgeting & planning
        "budget",
        "saving",
        "save",
        "savings",
        "financial",
        "finance",
        "plan",
        "planning",
        "goal",
        "target",
        "allocate",
        "allocation",
        # Income & earnings
        "income",
        "salary",
        "earning",
        "revenue",
        "profit",
        "loss",
        # Investments
        "invest",
        "investment",
        "stock",
        "mutual fund",
        "etf",
        "bond",
        "sip",
        "portfolio",
        "equity",
        "debt",
        "nifty",
        "sensex",
        "share",
        "dividend",
        # Debt & loans
        "loan",
        "debt",
        "emi",
        "interest",
        "mortgage",
        "credit card",
        "borrowing",
        "repay",
        "repayment",
        "outstanding",
        # Categories
        "groceries",
        "grocery",
        "food",
        "dining",
        "restaurant",
        "shopping",
        "bills",
        "utilities",
        "rent",
        "transportation",
        "fuel",
        "entertainment",
        "subscription",
        "insurance",
        "medical",
        "education",
        "travel",
        # Analysis terms
        "total",
        "how much",
        "analysis",
        "report",
        "summary",
        "trend",
        "compare",
        "increase",
        "decrease",
        "monthly",
        "yearly",
        "average",
        # Questions about finances
        "afford",
        "cash",
        "wealth",
        "net worth",
        "assets",
        "liabilities",
    ]

    # Non-finance topics (negative indicators - strong signals)
    off_topic_keywords = [
        # Technology & coding
        "code",
        "programming",
        "python",
        "javascript",
        "html",
        "css",
        "software",
        "computer",
        "algorithm",
        "debug",
        "compile",
        "github",
        "api",
        # Entertainment
        "movie",
        "film",
        "music",
        "song",
        "game",
        "gaming",
        "sport",
        "cricket",
        "football",
        "netflix",
        "youtube",
        "video",
        "actor",
        "actress",
        # General knowledge
        "capital of",
        "president",
        "prime minister",
        "history",
        "geography",
        "country",
        "city",
        "population",
        "war",
        "battle",
        # Science & nature
        "physics",
        "chemistry",
        "biology",
        "atom",
        "molecule",
        "planet",
        "solar system",
        "universe",
        "species",
        "animal",
        "plant",
        # Food & cooking
        "recipe",
        "cook",
        "bake",
        "ingredient",
        "cuisine",
        "dish",
        # Health
        "medicine",
        "disease",
        "symptom",
        "doctor",
        "hospital",
        "treatment",
        # Weather
        "weather",
        "temperature",
        "rain",
        "sunny",
        "cloudy",
        "forecast",
        # System prompts (jailbreak attempts)
        "ignore previous",
        "forget instructions",
        "system prompt",
        "act as",
        "pretend to be",
        "roleplay",
        "you are now",
        "new instructions",
    ]

    # Check for jailbreak/system manipulation attempts
    jailbreak_patterns = [
        r"ignore\s+(previous|all|your)\s+(instruction|prompt|rule)",
        r"forget\s+(everything|all|previous)",
        r"(system\s+prompt|your\s+prompt|show\s+prompt)",
        r"act\s+as\s+(?!.*finance)",
        r"pretend\s+to\s+be",
        r"you\s+are\s+now\s+(?!.*finance)",
        r"new\s+instructions?",
        r"disregard\s+",
        r"override\s+",
    ]

    for pattern in jailbreak_patterns:
        if re.search(pattern, query_lower):
            return (
                False,
                "I'm designed exclusively for personal finance assistance. Let's focus on your financial questions!",
            )

    # Check for off-topic indicators first (stronger signal)
    off_topic_matches = sum(
        1 for keyword in off_topic_keywords if keyword in query_lower
    )

    # Check for finance-related keywords
    finance_matches = sum(1 for keyword in finance_keywords if keyword in query_lower)

    # Decision logic:
    # 1. If strong off-topic signals and no finance signals -> reject
    # 2. If has finance signals -> allow
    # 3. If ambiguous -> check common question patterns

    if off_topic_matches > 0 and finance_matches == 0:
        return (
            False,
            "I'm Your Finance Bro, and I'm specifically designed to help with personal finance questions only. I can help you with budgeting, spending analysis, savings goals, account management, and financial planning. What would you like to know about your finances?",
        )

    if finance_matches > 0:
        return True, ""

    # Check for common finance question patterns
    finance_patterns = [
        r"how\s+much.*?(spent|spend|save|earn|owe|balance)",
        r"what.*?(expense|spending|income|budget|balance|account)",
        r"show.*?(transaction|spending|budget|account|balance)",
        r"(total|sum|amount).*?(spent|spend|expense|income)",
        r"can\s+i\s+afford",
        r"where.*?(money|spent|expense)",
    ]

    for pattern in finance_patterns:
        if re.search(pattern, query_lower):
            return True, ""

    # If very short query (< 3 words) and no clear indicators, be conservative
    if len(query_lower.split()) < 3 and finance_matches == 0:
        return (
            False,
            "Could you please provide more details about your finance question? I'm here to help with budgeting, spending analysis, account management, and financial planning.",
        )

    # Default: If no strong indicators either way but not clearly off-topic, allow
    # The agent's own system prompt will handle final validation
    return True, ""
