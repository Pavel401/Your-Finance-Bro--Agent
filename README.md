# Your Finance Bro 💰

An AI-powered financial assistant API that helps users understand and manage their finances through natural conversation.

## Features

- 🤖 **AI-Powered Chat**: Uses PydanticAI with GPT-4 or Gemini models
- 💬 **Conversation History**: Maintains chat context for better responses
- 📊 **Financial Analysis**: Analyzes transactions, accounts, and budgets
- 🔄 **Streaming Responses**: Real-time streaming for better UX
- 🔒 **Secure**: Environment-based API key management

## Setup

### Prerequisites

- Python 3.13+
- OpenAI API key or Google API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Your Finance Bro"
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI API Key (for GPT models)
OPENAI_API_KEY=your_openai_api_key_here

# Google API Key (for Gemini models)
GOOGLE_API_KEY=your_google_api_key_here
```

## Running the Application

### Development Mode

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 80
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /agent/chat

Chat with the financial assistant.

**Request Body:**
```json
{
  "user_query": "What's my total spending this month?",
  "finance_info": {
    "transactions": [...],
    "accounts": [...],
    "budgets": [...]
  },
  "chat_history": [
    {
      "role": "user",
      "content": "Previous question"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    }
  ]
}
```

**Response:**
Streams the assistant's response in real-time as plain text.

## Project Structure

```
Your Finance Bro/
├── app/
│   ├── configs/
│   │   └── model_config.py      # LLM model configurations
│   ├── endpoint/
│   │   └── agent.py             # FastAPI endpoints
│   ├── model/
│   │   └── finance_model.py     # Pydantic models
│   └── services/
│       ├── agent_services.py    # PydanticAI agent logic
│       └── llm_service.py       # LLM provider setup
├── main.py                      # Application entry point
├── pyproject.toml              # Dependencies
├── .env.example                # Example environment variables
└── README.md                   # This file
```

## Security Best Practices

1. **Never commit `.env` files** - They're in `.gitignore`
2. **Use environment variables** for API keys
3. **Validate all inputs** at the endpoint level
4. **Configure CORS** properly for production
5. **Use HTTPS** in production environments

## Development

### Adding a New LLM Model

1. Add the model to `LLMModelName` enum in `app/configs/model_config.py`
2. Update `get_llm_model_config()` in `app/services/llm_service.py`

### Customizing the Agent

Edit the system prompt in `app/services/agent_services.py`:

```python
finance_agent = Agent(
    model=get_llm_model_config(LLMModelName.GPT_4O_MINI),
    deps_type=FinanceDeps,
    system_prompt="Your custom system prompt here",
)
```

