# API Endpoints with JSON Bodies

## Chat Endpoints

### POST /ai/chat
```json
{
  "session_id": "sess-123",
  "message": "Your question here",
  "mode": "normal"
}
```

### POST /ai/chat/stream
```json
{
  "session_id": "sess-123",
  "message": "Your question here",
  "mode": "teaching"
}
```

### GET /ai/chat/history/{session_id}
No body required

### POST /ai/quick-suggestions
```json
{
  "session_id": "sess-123",
  "concept": "Photosynthesis",
  "topic_id": "biology-101"
}
```

### POST /ai/contextual
```json
{
  "session_id": "sess-123",
  "message": "I dont understand this",
  "lesson_id": "lesson-456",
  "quiz_id": null,
  "context_type": "lesson"
}
```

---

## Session Endpoints

### POST /session/create
No body required

### GET /session/{session_id}
No body required

### GET /session/user/{user_id}
No body required

---

## Progress Endpoints

### POST /progress/update
```json
{
  "user_id": "student-123",
  "topic_id": "algebra",
  "score": 85.5,
  "attempts": 3,
  "correct_answers": 17,
  "total_questions": 20,
  "time_spent_seconds": 1800
}
```

### GET /progress/{user_id}
No body required

### GET /progress/stats/{user_id}
No body required

---

## Adaptive Learning Endpoints

### POST /adaptive/next-topic
```json
{
  "user_id": "student-123",
  "current_topic": "algebra"
}
```

### POST /adaptive/assess
```json
{
  "topic_id": "algebra",
  "score": 75.0,
  "time_spent_seconds": 1200
}
```

### POST /adaptive/adjust-difficulty
```json
{
  "current_difficulty": "intermediate",
  "last_score": 65.5
}
```

---

## Feedback Endpoints

### POST /feedback/{user_id}/{topic_id}
No body required (topic_id in path)

### GET /feedback/{user_id}
No body required

### POST /feedback/performance-gap/{user_id}
```json
{
  "topic_id": "algebra",
  "current_score": 65,
  "target_score": 85
}
```

### POST /feedback/strengths-weaknesses/{user_id}
```json
{
  "topic_id": "biology"
}
```

---

## Proactive Learning Endpoints

### POST /proactive/progress-based-nudges/{user_id}
No body required

### POST /proactive/smart-reminders/{user_id}
```json
{
  "include_streak": true,
  "include_pending": true
}
```

### GET /proactive/engagement-level/{user_id}
No body required

### POST /proactive/motivational-nudge/{user_id}
```json
{
  "include_achievements": true
}
```

---

## Learning Path Endpoints

### POST /learning-path/generate
```json
{
  "goal": "Master Data Structures",
  "duration_days": 30
}
```

### GET /learning-path/goal/{goal}
No body required

---

## Recommendation Endpoints

### POST /recommendations/{user_id}/generate
No body required

### GET /recommendations/{user_id}
No body required

### POST /recommendations/acknowledge/{recommendation_id}
```json
{
  "user_id": "student-123"
}
```

---

## Document Endpoints

### POST /documents/upload
```
Form Data:
- file: <file_object> (PDF, DOCX, JPG, PNG, TXT)
- session_id: "sess-123"
```

### GET /documents/{doc_id}
No body required

### POST /documents/{doc_id}/ask
```json
{
  "session_id": "sess-123",
  "question": "Summarize this document",
  "context_length": 5
}
```

### GET /documents/list/{session_id}
No body required

### DELETE /documents/{doc_id}
No body required

---

## Voice Endpoints

### POST /voice/transcribe
```
Form Data:
- file: <audio_file> (MP3, WAV, M4A, OGG, FLAC, PCM)
```

### POST /voice/chat-and-speak
```
Form Data:
- file: <audio_file>
- session_id: "sess-123"
- mode: "normal"
- include_speech: true
- voice: "alloy"
```

### POST /voice/text-to-speech
```json
{
  "text": "Your text here",
  "voice": "alloy"
}
```

---

## Analytics Endpoints

### GET /analytics/session/{session_id}
No body required

### GET /analytics/user/{user_id}
No body required

### GET /analytics/global
No body required

### POST /analytics/cleanup
No body required

---

## Health & Info Endpoints

### GET /health
No body required

### GET /
No body required

---

## Query Parameters Reference

### Chat Endpoints
- `mode`: "normal" | "teaching" | "guiding"
- `session_id`: string

### Voice Endpoints
- `voice`: "alloy" | "echo" | "fable" | "onyx" | "nova" | "shimmer"
- `include_speech`: boolean

### Progress Endpoints
- Optional filters for date range, topic filter

### Learning Path
- `goal`: learning objective
- `duration_days`: number of days
