# 💰 Your Finance Bro

An AI-powered financial assistant that helps you analyze your financial data, track spending, and get personalized financial insights through natural conversations.

## 🌟 Features

- **AI-Powered Chat Interface**: Natural language conversations about your finances
- **Financial Data Analysis**: Upload and analyze transactions, accounts, and budgets
- **Real-time Streaming Responses**: Get instant feedback from the AI assistant
- **Interactive Web Interface**: Modern, responsive UI with drag-and-drop file upload
- **Multi-Model Support**: Built with PydanticAI supporting GPT-4 and other LLMs
- **Chat History**: Maintains conversation context for coherent interactions

## 🏗️ Project Structure

```
Your Finance Bro/
├── main.py                          # FastAPI application entry point
├── pyproject.toml                   # Project dependencies and metadata
├── output.json                      # Sample financial data file
├── README.md                        # Project documentation
├── app/
│   ├── configs/
│   │   └── model_config.py         # LLM model configuration
│   ├── endpoint/
│   │   └── agent.py                # Chat endpoint routes
│   ├── model/
│   │   ├── agent_model.py          # Pydantic models for chat
│   │   └── finance_model.py        # Financial data models
│   └── services/
│       ├── agent_services.py       # Core agent logic and streaming
│       ├── finance_service.py      # Finance data processing
│       ├── llm_service.py          # LLM model initialization
│       └── utility_service.py      # Helper utilities
└── frontend/
    ├── index.html                   # Main web interface
    ├── script.js                    # Frontend JavaScript logic
    └── styles.css                   # UI styling
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Pavel401/Your-Finance-Bro.git
   cd "Your Finance Bro"
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

   Or manually install required packages:
   ```bash
   pip install fastapi uvicorn pydantic-ai pydantic-ai-slim[google,openai] python-dotenv
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   # Or for Google models:
   # GOOGLE_API_KEY=your_google_api_key_here
   ```

### Running the Application

1. **Start the server**:
   ```bash
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080 --reload
   ```

2. **Access the application**:
   Open your browser and navigate to:
   ```
   http://localhost:8080
   ```

3. **Upload your financial data**:
   - Click the upload area or drag and drop your `output.json` file
   - The file should contain your financial transactions, accounts, and budgets
   - Click "Start Chatting" to begin

## 📊 Data Format

The application expects financial data in JSON format with the following structure:

```json
{
  "export_info": {
    "export_date": "2024-01-01T00:00:00Z",
    "app_version": "1.0.0",
    "data_format": "json",
    "total_transactions": 100,
    "total_accounts": 3,
    "total_budgets": 5
  },
  "transactions": [
    {
      "id": "uuid",
      "date": "2024-01-01T00:00:00Z",
      "type": "debit",
      "title": "Transaction Title",
      "amount": 100.00,
      "category": "other",
      "account_id": "uuid"
    }
  ],
  "accounts": [
    {
      "id": "uuid",
      "account_name": "Checking Account",
      "bank_name": "Bank Name",
      "account_type": "checking",
      "balance": 5000.00
    }
  ],
  "budgets": [
    {
      "id": "uuid",
      "year": 2024,
      "month": 1,
      "amount": 3000
    }
  ]
}
```

## 🛠️ API Endpoints

### Health Check
- **GET** `/health`
  - Returns API health status

### Chat Endpoint
- **POST** `/agent/chat`
  - Request body:
    ```json
    {
      "user_query": "What's my current balance?",
      "finance_info": { ... },
      "chat_history": []
    }
    ```
  - Response: Streaming NDJSON with AI responses

## 💡 Example Questions

Ask your Finance Bro questions like:

- "What's my current balance across all accounts?"
- "Show me my spending summary for this month"
- "Which category do I spend the most on?"
- "Give me tips to save money based on my spending"
- "What were my largest transactions last month?"
- "How much did I budget for this month?"



## 📄 Mere 3 Shabd 
Andi Mandi Sandi Jo project copy karega without forking and giving a star the repo wow hai ________ Baki **तुम समझदार हो ना?** (You're smart, right?) 😉
If you're using this project, at least give it a ⭐ and fork it properly.  
Remember: Good karma in open source = fewer bugs in your code! 🙏




