# AI Learning Chatbot Backend - Implementation Guide

## Project Overview

A production-ready FastAPI backend for an AI-powered learning platform with streaming responses, session management, analytics, and multi-mode chat support.

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone/Navigate to project
cd "ai chatbot"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Configure OpenAI API

Add your OpenAI API key to `.env`:
```env
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Run Development Server

```bash
python -m uvicorn app.main:app --reload
```

Server will start at: `http://localhost:8000`

API Documentation available at: `http://localhost:8000/docs`

## 📁 Project Structure

```
ai_chatbot/
├── app/
│   ├── main.py                 # Main FastAPI application
│   ├── core/
│   │   └── config.py          # Configuration settings
│   ├── models/
│   │   ├── chat_models.py     # Chat request/response models
│   │   └── session_models.py  # Session and analytics models
│   ├── services/
│   │   ├── ai_service.py      # OpenAI API integration
│   │   ├── prompt_builder.py  # Prompt engineering
│   │   ├── session_service.py # Session management
│   │   ├── analytics_service.py # Usage tracking
│   │   └── rag_service.py     # Document retrieval (RAG)
│   ├── routes/
│   │   ├── chat.py            # Chat endpoints
│   │   ├── session.py         # Session endpoints
│   │   ├── analytics.py       # Analytics endpoints
│   │   └── voice.py           # Voice endpoints (placeholder)
│   └── utils/
│       ├── memory.py          # Session memory management
│       └── tokenizer.py       # Token counting utilities
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🔌 API Endpoints

### Chat Endpoints (`/ai`)

#### POST `/ai/chat`
Standard chat request with context
```json
{
  "user_id": "user123",
  "session_id": "session-uuid",
  "message": "What is photosynthesis?",
  "mode": "teaching",
  "lesson_context": "Chapter 2: Photosynthesis",
  "quiz_context": null
}
```

**Response:**
```json
{
  "session_id": "session-uuid",
  "user_message": "What is photosynthesis?",
  "ai_response": "Photosynthesis is the process...",
  "mode": "teaching",
  "timestamp": "2024-03-31T10:30:00Z"
}
```

#### POST `/ai/chat/stream`
Streaming chat response (Server-Sent Events)
Same request format as `/ai/chat`

**Response:** Streamed text chunks via SSE
```
data: Photosynthesis
data: is
data: the
...
data: [DONE]
```

#### GET `/ai/chat/history/{session_id}`
Get complete chat history

**Response:**
```json
{
  "session_id": "session-uuid",
  "user_id": "user123",
  "messages": [
    {"role": "user", "content": "Hi", "timestamp": "2024-03-31T10:00:00Z"},
    {"role": "assistant", "content": "Hello!", "timestamp": "2024-03-31T10:00:05Z"}
  ],
  "total_messages": 2
}
```

### Session Endpoints (`/session`)

#### POST `/session/create`
Create a new chat session
```json
{
  "user_id": "user123"
}
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "created_at": "2024-03-31T10:00:00Z",
  "status": "active"
}
```

#### GET `/session/{session_id}`
Get session information

#### GET `/session/user/{user_id}`
Get all sessions for a user

### Analytics Endpoints (`/analytics`)

#### GET `/analytics/user/{user_id}`
Get user analytics
```json
{
  "user_id": "user123",
  "total_queries": 15,
  "mode_usage": {"teaching": 8, "guiding": 5, "normal": 2},
  "avg_response_time": 1.23,
  "topics_discussed": ["biology", "photosynthesis"]
}
```

#### GET `/analytics/session/{session_id}`
Get session-specific analytics

#### GET `/analytics/global`
Get platform-wide analytics

#### POST `/analytics/cleanup`
Clean up expired sessions (admin endpoint)

### Voice Endpoints (`/voice`)

- **POST `/voice/transcribe`** - Audio to text (coming soon)
- **POST `/voice/speak`** - Text to speech (coming soon)
- **POST `/voice/chat`** - Full voice chat (coming soon)

## 💬 Chat Modes

### 1. **Normal Mode** (Default)
Standard Q&A responses
- Direct, clear answers
- Concise explanations
- Professional tone

### 2. **Teaching Mode**
Detailed educational responses
- Step-by-step explanations
- Practical examples
- Encourages learning

### 3. **Guiding Mode** (Socratic Method)
Hints and thought-provoking questions
- Asks clarifying questions
- Provides hints instead of answers
- Encourages independent thinking

### 4. **Quiz Mode** (Context-based)
Safe mode during quizzes
- No direct answers
- Hints only
- Guides without revealing answers

## 🧠 Memory & Context

### How It Works

1. **Session Creation**: Each user gets unique sessions via UUID
2. **Message Storage**: Last 5 messages stored in session memory
3. **Context Injection**: Previous messages injected into AI prompts
4. **Conversation Flow**: Maintains context across multiple turns

### Session Memory Structure
```python
{
  "session_id": "uuid",
  "user_id": "user123",
  "created_at": "timestamp",
  "last_activity": "timestamp",
  "messages": [
    {"role": "user", "content": "...", "timestamp": "..."},
    {"role": "assistant", "content": "...", "timestamp": "..."}
  ],
  "message_count": 2
}
```

## 📊 Analytics

### Tracked Metrics

- **Query Logs**: Every interaction is logged with timing
- **Mode Usage**: Tracks which modes are used most
- **Response Time**: Measures AI response latency
- **Topic Analysis**: Extracts key topics from queries
- **User Patterns**: Individual and collective usage patterns

### Example Usage

```python
# Get user analytics
GET /analytics/user/user123

# Get session-specific metrics
GET /analytics/session/session-id

# Get overall platform stats
GET /analytics/global
```

## 🔐 Configuration

Edit `app/core/config.py` or `.env`:

```env
OPENAI_API_KEY=sk-xxx
ENV=development
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000
MAX_CONTEXT_MESSAGES=5
SESSION_TIMEOUT=3600
LOG_LEVEL=INFO
```

## 🚀 Deployment

### Production Checklist

- [ ] Set `ENV=production` in `.env`
- [ ] Update CORS origins
- [ ] Configure production database (optional)
- [ ] Set up monitoring/logging
- [ ] Use environment variables for all secrets
- [ ] Configure rate limiting
- [ ] Set up SSL/TLS certificates

### Docker Deployment (Future)

```bash
docker build -t ai-chatbot-backend .
docker run -p 8000:8000 --env-file .env ai-chatbot-backend
```

## 🔄 Future Enhancements

### Planned Features

1. **Database Integration**
   - PostgreSQL for persistent storage
   - Redis for caching
   - Message history archival

2. **RAG (Retrieval-Augmented Generation)**
   - Document upload
   - Vector embeddings
   - Semantic search

3. **Voice Features**
   - Whisper ASR for speech-to-text
   - TTS for audio responses
   - Real-time voice chat

4. **Advanced Analytics**
   - User progress tracking
   - Learning path recommendations
   - Performance insights

5. **Security**
   - User authentication (JWT)
   - Rate limiting
   - Request validation

## 🧪 Testing

### Manual Testing with cURL

```bash
# Create session
curl -X POST http://localhost:8000/session/create \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123"}'

# Chat (replace session_id)
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "session_id": "YOUR_SESSION_ID",
    "message": "What is AI?",
    "mode": "teaching"
  }'

# Get history
curl http://localhost:8000/ai/chat/history/YOUR_SESSION_ID

# Get analytics
curl http://localhost:8000/analytics/user/user123
```

## 🛠️ Troubleshooting

### Common Issues

**Issue**: OpenAI API key error
- **Solution**: Verify API key in `.env`, check quota/billing

**Issue**: Session not found
- **Solution**: Ensure you created a session before chatting

**Issue**: CORS errors
- **Solution**: Update CORS origins in `main.py`

## 📝 Notes for Future Modules

When your friend provides additional modules:

1. Create new route file in `app/routes/`
2. Create services in `app/services/`
3. Add models in `app/models/`
4. Include router in `app/main.py`:
   ```python
   from app.routes import new_module
   app.include_router(new_module.router)
   ```

## 🎯 Architecture Principles

- **Modularity**: Separated concerns (routes, services, models)
- **Scalability**: Stateless design, ready for horizontal scaling
- **Maintainability**: Clear naming, DRY principles
- **Extensibility**: Easy to add new features/modules
- **Error Handling**: Comprehensive exception handling

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Python Pydantic](https://docs.pydantic.dev/)
- [Uvicorn Server](https://www.uvicorn.org/)

## 📄 License

Proprietary - AI Learning Platform

## 👥 Support

For issues or questions, contact the development team.

---

**Last Updated**: March 31, 2024
**Version**: 1.0.0
