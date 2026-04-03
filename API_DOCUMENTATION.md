# AI-TUTOR API Documentation

## Project Overview

**AI-TUTOR** is an intelligent tutoring backend system that enables interactive learning experiences through AI-powered conversations. The system allows users to engage with multiple AI models (OpenAI, Google Generative AI, and LLaMA) to learn about various topics. It intelligently manages API costs by tracking token usage and estimated expenses for each interaction, while maintaining a complete history of all conversations. This makes it an ideal solution for educational platforms seeking to integrate advanced AI capabilities with cost transparency and conversation persistence.

---

## Base URL

```
http://localhost:8000/api/v1
```

## Health Check

### Get Backend Status
- **Endpoint:** `GET /health`
- **Description:** Check if the backend is running
- **Response:**
  ```json
  {
    "status": "Backend healthy"
  }
  ```

---

## Chat Endpoints

### 1. Save Chat Message
Send a message to an AI model and get an intelligent response.

- **Endpoint:** `POST /chat/`
- **Description:** Save a user message, generate an AI reply, track token usage, and store in database

**Request Body:**
```json
{
  "userId": "string",
  "topicId": "string",
  "message": "string",
  "model": "string"
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userId | string | Yes | Unique identifier for the user |
| topicId | string | Yes | Topic ID that the user is learning about |
| message | string | Yes | The user's message/question |
| model | string | Yes | AI model to use (e.g., "openai", "gemini", "llama") |

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "reply": "The AI generated response...",
    "chatId": "unique-chat-id",
    "model": "openai",
    "tokensUsed": 150,
    "estimatedCost": 0.00225
  }
}
```

**Error Response (500):**
```json
{
  "detail": "Failed to save chat: [error message]"
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| status | string | Status of the request ("success" or error) |
| reply | string | The AI-generated response |
| chatId | string | Unique identifier for the saved chat record |
| model | string | The AI model that generated the reply |
| tokensUsed | integer | Number of tokens consumed |
| estimatedCost | float | Estimated cost in USD for this interaction |

---

### 2. Get Chat History
Retrieve all conversation history for a specific user.

- **Endpoint:** `GET /chat/history/{user_id}`
- **Description:** Fetch all chat messages and replies for a user

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | The user ID whose history to retrieve |

**Success Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "chatId": "chat-123",
      "userId": "user-456",
      "topicId": "topic-789",
      "message": "What is photosynthesis?",
      "reply": "Photosynthesis is the process...",
      "model": "openai",
      "tokensUsed": 120,
      "estimatedCost": 0.0018,
      "timestamp": "2026-03-19T10:30:00"
    },
    {
      "chatId": "chat-124",
      "userId": "user-456",
      "topicId": "topic-789",
      "message": "Can you explain it more simply?",
      "reply": "Sure! Photosynthesis is simply...",
      "model": "gemini",
      "tokensUsed": 95,
      "estimatedCost": 0.0014,
      "timestamp": "2026-03-19T10:45:00"
    }
  ]
}
```

**Error Response (500):**
```json
{
  "detail": "Failed to retrieve chat history: [error message]"
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| chatId | string | Unique identifier for this chat record |
| userId | string | ID of the user |
| topicId | string | Topic being discussed |
| message | string | The user's message |
| reply | string | The AI's response |
| model | string | Model used for this reply |
| tokensUsed | integer | Tokens consumed for this exchange |
| estimatedCost | float | Cost in USD |
| timestamp | string | ISO format timestamp of the conversation |

---

## Usage Endpoints

### Get User Usage Statistics
Retrieve aggregated usage metrics for a specific user.

- **Endpoint:** `GET /usage/{user_id}`
- **Description:** Get total messages, tokens used, and estimated costs for a user

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | The user ID to get usage statistics for |

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "userId": "user-456",
    "totalMessages": 45,
    "tokensUsed": 12500,
    "estimatedCost": 0.1875
  }
}
```

**Error Response (500):**
```json
{
  "detail": "Failed to retrieve usage: [error message]"
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| userId | string | ID of the user |
| totalMessages | integer | Total number of messages sent |
| tokensUsed | integer | Cumulative tokens used across all messages |
| estimatedCost | float | Total estimated cost in USD |

---

## Error Handling

All errors return HTTP status codes with descriptive messages:

| Status Code | Description |
|-------------|-------------|
| 200 | Success - Request completed successfully |
| 400 | Bad Request - Invalid input parameters |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error or database issue |

**Error Response Format:**
```json
{
  "detail": "Error description"
}
```

---

## Example Usage

### Save a Chat Message
```bash
curl -X POST "http://localhost:8000/api/v1/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "john_doe",
    "topicId": "biology_101",
    "message": "What is cellular respiration?",
    "model": "openai"
  }'
```

### Get Chat History
```bash
curl -X GET "http://localhost:8000/api/v1/chat/history/john_doe"
```

### Get Usage Statistics
```bash
curl -X GET "http://localhost:8000/api/v1/usage/john_doe"
```

---

## Database Schema

**Chat Table:**
- `chat_id`: Primary key (unique identifier)
- `user_id`: User identifier
- `topic_id`: Topic identifier
- `message`: User's message
- `reply`: AI-generated reply
- `model`: AI model used
- `tokens_used`: Tokens consumed
- `cost`: Estimated cost
- `timestamp`: Timestamp of interaction

---

## Supported AI Models

- **openai**: OpenAI GPT models
- **gemini**: Google Generative AI (Gemini)
- **llama**: LLaMA models

---

## Notes

- All timestamps are in ISO 8601 format
- Costs are estimated and may vary based on actual API pricing
- Token counts vary by model
- Chat history is persistent and stored in the database
- All API responses include a `status` field indicating success or failure
