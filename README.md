# AI-TUTOR

## Project Overview

Developed a comprehensive backend system for intelligent tutoring that leverages multiple AI models (OpenAI, Google Generative AI, and LLaMA) to deliver personalized educational experiences. The system manages user queries, generates intelligent responses, and maintains complete conversation history. It implements cost tracking and token management to monitor AI API usage and expenses. The architecture ensures data persistence, accurate cost estimation, and seamless integration with various AI providers. The design supports scalability through modular service architecture and consistent tracking of user engagement, learning patterns, and usage metrics for analytics and optimization.

---

## Key Features

### 🤖 Multi-Model AI Integration
- **OpenAI Integration**: GPT-based models for advanced reasoning and complex explanations
- **Google Generative AI**: Gemini models for diverse learning content generation
- **LLaMA Support**: Open-source models for flexible deployment options
- Dynamic model selection based on topic or user preferences

### 💾 Persistent Chat Management
- Complete conversation history storage for each user
- Topic-based organization of learning sessions
- Timestamp tracking for all interactions
- Efficient retrieval of past conversations for review and analytics

### 💰 Cost Tracking & Transparency
- Real-time token counting for every interaction
- Automatic cost estimation based on model usage
- Aggregated usage statistics per user
- Cost monitoring to prevent budget overruns and optimize model selection

### 📊 Usage Analytics
- Track total messages sent by users
- Monitor cumulative token consumption
- Calculate estimated expenses across learning sessions
- User-level analytics for engagement insights

### 🏗️ Scalable Architecture
- Modular service layer (separate AI providers, cost calculations)
- Database-backed persistence (PostgreSQL)
- RESTful API design for easy frontend integration
- Health monitoring and error handling

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   FastAPI Application                │
│              (Main: main.py)                         │
└─────────────────────────────────────────────────────┘
         │                                     │
         ▼                                     ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│   Chat Routes            │      │   Usage Routes           │
│ • POST /chat/            │      │ • GET /usage/{user_id}   │
│ • GET /chat/history      │      └──────────────────────────┘
└──────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│                 Services Layer                        │
├──────────────────────────────────────────────────────┤
│ • ai_service.py (AI reply generation)                │
│ • cost_service.py (Cost estimation)                  │
│ • openai_service.py (OpenAI integration)             │
│ • gemini_service.py (Google Gemini integration)      │
│ • llama_service.py (LLaMA integration)               │
└──────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│            Models & Database Layer                    │
├──────────────────────────────────────────────────────┤
│ • chat_model.py (Chat ORM model)                     │
│ • db.py (Database connection & session)              │
│ • PostgreSQL Database                                │
└──────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. **Chat Module** (`routes/chat.py`)
- Accepts user queries with topic and model selection
- Generates AI responses with token tracking
- Stores conversations with metadata to database
- Retrieves complete chat history for users

### 2. **Usage Module** (`routes/usage.py`)
- Aggregates user statistics
- Calculates total tokens consumed
- Computes estimated costs
- Provides usage insights for monitoring

### 3. **AI Services** (`services/`)
- **ai_service.py**: Orchestrates AI response generation
- **openai_service.py**: OpenAI API integration
- **gemini_service.py**: Google Generative AI integration
- **llama_service.py**: LLaMA model integration

### 4. **Cost Service** (`services/cost_service.py`)
- Estimates costs based on token usage
- Model-specific pricing calculations
- Cost aggregation and reporting

### 5. **Data Model** (`models/chat_model.py`)
- Chat schema with user, topic, message, and response fields
- Token tracking and cost per interaction
- Timestamp and model metadata

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/chat/` | Save user message and get AI response |
| `GET` | `/api/v1/chat/history/{user_id}` | Retrieve chat history for user |
| `GET` | `/api/v1/usage/{user_id}` | Get usage statistics for user |
| `GET` | `/health` | Health check endpoint |

---

## Data Flow

```
1. User sends message with topic and model selection
   ↓
2. API validates request and extracts parameters
   ↓
3. AI Service selects appropriate AI provider
   ↓
4. AI model generates response with token count
   ↓
5. Cost Service calculates estimated expense
   ↓
6. Chat record saved to database (user, topic, message, reply, tokens, cost)
   ↓
7. Response returned to user with chatId and metadata
   ↓
8. User can access chat history and usage statistics anytime
```

---

## Technology Stack

- **Framework**: FastAPI (modern, fast Python web framework)
- **Database**: PostgreSQL (reliable relational database)
- **ORM**: SQLAlchemy (database interaction)
- **AI APIs**: OpenAI, Google Generative AI, LLaMA
- **HTTP Client**: Requests & httpx
- **Testing**: Pytest
- **Server**: Uvicorn (ASGI server)

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- API keys for OpenAI and/or Google Generative AI

### Steps
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables (`.env` file)
4. Set up database: `python backend/config/db.py`
5. Run server: `uvicorn backend.main:app --reload`

---

## Usage Example

### Send a Chat Message
```bash
curl -X POST "http://localhost:8000/api/v1/chat/" \
  -H "Content-Type: application/json" \
  -d {
    "userId": "student_123",
    "topicId": "biology_photosynthesis",
    "message": "Explain photosynthesis",
    "model": "openai"
  }
```

### Get Chat History
```bash
curl "http://localhost:8000/api/v1/chat/history/student_123"
```

### Get Usage Statistics
```bash
curl "http://localhost:8000/api/v1/usage/student_123"
```

---

## Benefits

✅ **Cost Transparency**: Real-time tracking of AI API expenses  
✅ **Learning Continuity**: Complete conversation history for review  
✅ **Flexible AI Selection**: Choose optimal model per use case  
✅ **Scalable Architecture**: Modular design for easy expansion  
✅ **Educational Analytics**: Track user engagement and learning patterns  
✅ **Reliable Persistence**: Database-backed storage ensures data integrity  

---

## Future Enhancements

- [ ] User progress tracking and adaptive learning paths
- [ ] Advanced analytics and learning insights
- [ ] Real-time streaming responses
- [ ] Multi-language support
- [ ] Caching layer for frequently asked questions
- [ ] User authentication and role-based access
- [ ] Admin dashboard for monitoring
