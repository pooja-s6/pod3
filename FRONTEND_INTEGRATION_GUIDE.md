# Frontend Integration Guide - API Summary for Team

---

## Quick Overview

The backend now has **40 fully documented endpoints** across 12 categories. This guide helps frontend developers integrate these APIs efficiently.

---

## 🚀 API Base URL

```
http://localhost:8000
```

**For Production:** Replace `localhost:8000` with your production domain.

---

## 📋 Main Categories & Routes

### 1. **Chat Endpoints** (5 endpoints)
Send messages to AI tutor with different modes (normal, teaching, guiding).

| Feature | Endpoint | Method |
|---------|----------|--------|
| Send Message | `/ai/chat` | POST |
| Stream Response | `/ai/chat/stream` | POST |
| Chat History | `/ai/chat/history/{session_id}` | GET |
| Quick Suggestions | `/ai/quick-suggestions` | POST |
| Contextual Response | `/ai/contextual` | POST |

**Use this for:** Main chat interface, real-time conversations, quick help features.

---

### 2. **Session Endpoints** (3 endpoints)
Create and manage learning sessions — **CREATE SESSION FIRST before calling chat endpoints**.

| Feature | Endpoint | Method |
|---------|----------|--------|
| Create Session | `/session/create` | POST |
| Get Session Details | `/session/{session_id}` | GET |
| Get User Sessions | `/session/user/{user_id}` | GET |

**Use this for:** Session initialization, tracking active sessions, user session history.

**⚠️ IMPORTANT:** Always create a session first and save the `session_id` before using chat endpoints.

---

### 3. **Progress Endpoints** (3 endpoints)
Track and display student learning progress.

| Feature | Endpoint | Method |
|---------|----------|--------|
| Update Progress | `/progress/update` | POST |
| Get User Progress | `/progress/{user_id}` | GET |
| Get Statistics | `/progress/stats/{user_id}` | GET |

**Use this for:** Progress dashboard, score displays, topic completion tracking.

---

### 4. **Adaptive Learning** (3 endpoints)
Recommend next topics and adjust difficulty dynamically.

| Feature | Endpoint | Method |
|---------|----------|--------|
| Next Topic | `/adaptive/next-topic` | POST |
| Assess Mastery | `/adaptive/assess` | POST |
| Adjust Difficulty | `/adaptive/adjust-difficulty` | POST |

**Use this for:** Personalized learning paths, difficulty level adjustment, course sequencing.

---

### 5. **Feedback Endpoints** (4 endpoints)
Generate personalized AI feedback on performance.

| Feature | Endpoint | Method |
|---------|----------|--------|
| Get Feedback | `/feedback/{user_id}/{topic_id}` | POST |
| Feedback History | `/feedback/{user_id}` | GET |
| Performance Gap | `/feedback/performance-gap/{user_id}` | POST |
| Strengths/Weaknesses | `/feedback/strengths-weaknesses/{user_id}` | POST |

**Use this for:** Personalized feedback displays, performance analysis, improvement suggestions.

---

### 6. **Proactive Learning** (4 endpoints)
Send nudges, reminders, and motivational messages to students.

| Feature | Endpoint | Method |
|---------|----------|--------|
| Progress Nudges | `/proactive/progress-based-nudges/{user_id}` | POST |
| Smart Reminders | `/proactive/smart-reminders/{user_id}` | POST |
| Engagement Level | `/proactive/engagement-level/{user_id}` | GET |
| Motivational Nudge | `/proactive/motivational-nudge/{user_id}` | POST |

**Use this for:** Notification/push alerts, dashboard widgets, engagement indicators.

---

### 7. **Learning Path** (1 endpoint)
Generate personalized learning plans.

| Feature | Endpoint | Method |
|---------|----------|--------|
| Generate Path | `/learning-path/generate` | POST |

**Use this for:** Course planning, goal-based learning paths, weekly schedules.

---

### 8. **Recommendations** (3 endpoints)
AI-powered learning recommendations.

| Feature | Endpoint | Method |
|---------|----------|--------|
| Generate Recommendations | `/recommendations/{user_id}/generate` | POST |
| Get Recommendations | `/recommendations/{user_id}` | GET |
| Acknowledge Recommendation | `/recommendations/acknowledge/{recommendation_id}` | POST |

**Use this for:** Recommendation cards, "Next Learn" suggestions, personalized course recommendations.

---

### 9. **Document Endpoints** (5 endpoints)
Upload and analyze learning documents (PDF, Word, Images).

| Feature | Endpoint | Method |
|---------|----------|--------|
| Upload Document | `/documents/upload` | POST |
| Get Document | `/documents/{doc_id}` | GET |
| Ask About Document | `/documents/{doc_id}/ask` | POST |
| List Documents | `/documents/list/{session_id}` | GET |
| Delete Document | `/documents/{doc_id}` | DELETE |

**Use this for:** File upload UI, document library, Q&A on documents.

**📤 Upload Format:** Multipart form-data with file and session_id.

---

### 10. **Voice Endpoints** (3 endpoints)
Voice transcription and speech synthesis.

| Feature | Endpoint | Method |
|---------|----------|--------|
| Transcribe Audio | `/voice/transcribe` | POST |
| Voice Chat | `/voice/chat-and-speak` | POST |
| Text to Speech | `/voice/text-to-speech` | POST |

**Use this for:** Voice input features, audio chat interface, text-to-speech conversion.

**📤 Upload Format:** Multipart form-data with audio file (MP3, WAV, M4A, OGG, FLAC, PCM).

---

### 11. **Analytics Endpoints** (4 endpoints)
Retrieve learning analytics and platform metrics.

| Feature | Endpoint | Method |
|---------|----------|--------|
| Session Analytics | `/analytics/session/{session_id}` | GET |
| User Analytics | `/analytics/user/{user_id}` | GET |
| Global Analytics | `/analytics/global` | GET |
| Cleanup Analytics | `/analytics/cleanup` | POST |

**Use this for:** Analytics dashboard, learning statistics, performance charts.

---

### 12. **Health & Info** (2 endpoints)
Server status and API information.

| Feature | Endpoint | Method |
|---------|----------|--------|
| Health Check | `/health` | GET |
| Home Info | `//` | GET |

**Use this for:** Server status checks, API version information.

---

## 🔄 Frontend Integration Flow

### **Step 1: Initialize Session**
```javascript
// First thing - create a session
POST /session/create
Response: { session_id: "sess-123", ... }
// Save session_id in state/localStorage
```

### **Step 2: Use Chat with Session**
```javascript
// Now use the session_id for chat
POST /ai/chat
Body: {
  "session_id": "sess-123",  // from step 1
  "message": "Your question",
  "mode": "normal"
}
```

### **Step 3: Track Progress**
```javascript
// After user completes an activity
POST /progress/update
Body: {
  "user_id": "student-123",
  "topic_id": "algebra",
  "score": 85.5,
  ...
}
```

### **Step 4: Get Recommendations**
```javascript
// Show personalized recommendations
POST /recommendations/{user_id}/generate
// Display recommendations to user
```

### **Step 5: Send Nudges**
```javascript
// Optional: Send engagement nudges
POST /proactive/progress-based-nudges/{user_id}
// Display as notifications/alerts
```

---

## 📤 Common Request Patterns

### **JSON Request Pattern**
```javascript
const response = await fetch('http://localhost:8000/ai/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    "session_id": "sess-123",
    "message": "Your question here",
    "mode": "normal"
  })
});
const data = await response.json();
```

### **File Upload Pattern (Multipart)**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('session_id', 'sess-123');

const response = await fetch('http://localhost:8000/documents/upload', {
  method: 'POST',
  body: formData  // NO Content-Type header - browser sets it
});
const data = await response.json();
```

### **Simple GET Pattern**
```javascript
const response = await fetch('http://localhost:8000/progress/stats/student-123');
const data = await response.json();
```

---

## 📊 Response Structure

All endpoints return JSON with:

```json
{
  "field1": "value",
  "field2": 123,
  "nested_object": {
    "key": "value"
  },
  "arrays": [
    { "item": 1 },
    { "item": 2 }
  ]
}
```

**Check COMPLETE_API_REFERENCE.md for example responses for each endpoint.**

---

## 🎯 UI Components & Recommended Endpoints

### **Dashboard**
- `/progress/{user_id}` - Overall progress display
- `/progress/stats/{user_id}` - Statistics and trends
- `/analytics/user/{user_id}` - User analytics

### **Chat Interface**
- `/session/create` - Initialize chat
- `/ai/chat` or `/ai/chat/stream` - Send messages
- `/ai/chat/history/{session_id}` - Load conversation history

### **Learning Path Page**
- `/learning-path/generate` - Create personalized paths
- `/adaptive/next-topic` - Recommend next topic

### **Recommendations Widget**
- `/recommendations/{user_id}/generate` - Get recommendations
- `/recommendations/acknowledge/{recommendation_id}` - Track user actions

### **Feedback Page**
- `/feedback/{user_id}/{topic_id}` - Get personalized feedback
- `/feedback/performance-gap/{user_id}` - Show improvement gaps
- `/feedback/strengths-weaknesses/{user_id}` - Strengths & weaknesses

### **Notifications/Alerts**
- `/proactive/progress-based-nudges/{user_id}` - Push notifications
- `/proactive/smart-reminders/{user_id}` - Reminder alerts
- `/proactive/motivational-nudge/{user_id}` - Encouragement messages

### **Document Upload**
- `/documents/upload` - File upload
- `/documents/list/{session_id}` - Show uploaded docs
- `/documents/{doc_id}/ask` - Q&A on documents

### **Voice Chat**
- `/voice/transcribe` - Convert audio to text
- `/voice/chat-and-speak` - Full voice interaction
- `/voice/text-to-speech` - Convert response to audio

---

## ⚡ Performance Tips

1. **Session Management**
   - Create session once and reuse the `session_id`
   - Store session_id in localStorage or state management
   - Don't create new sessions for every request

2. **Caching**
   - Cache `/progress/{user_id}` responses (refresh on update)
   - Cache `/progress/stats/{user_id}` (refresh every 5-10 mins)
   - Don't cache `/ai/chat` responses

3. **Streaming**
   - Use `/ai/chat/stream` for better UX on long responses
   - Display chunks as they arrive for real-time feel

4. **Loading States**
   - Show loading indicators for POST requests
   - Use skeleton loaders for data fetching
   - Handle errors gracefully

---

## 🔒 Security Considerations

1. **API Keys:** Currently no authentication. Add before production.
2. **Rate Limiting:** Implement rate limiting on frontend.
3. **Data Validation:** Validate all inputs before sending.
4. **Error Handling:** Handle network errors, timeouts, invalid responses.

---

## 🐛 Error Handling

**Expected Error Responses:**
```json
{
  "detail": "Error message here",
  "status_code": 400
}
```

**Common Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad request (invalid data)
- `404` - Not found
- `500` - Server error

**Implementation:**
```javascript
try {
  const response = await fetch(url);
  if (!response.ok) {
    const error = await response.json();
    console.error('API Error:', error.detail);
    // Show user-friendly error message
  }
  const data = await response.json();
  // Process data
} catch (error) {
  console.error('Network Error:', error);
  // Show connection error
}
```

---

## 📚 Documentation Links

- **Full API Reference:** See `COMPLETE_API_REFERENCE.md` for all 40 endpoints with examples
- **Quick JSON Bodies:** See `ENDPOINT_JSON_BODIES.md` for copy-paste ready requests
- **Postman Testing:** Import endpoints into Postman and test before integration

---

## 🎬 Quick Start for Frontend

1. **Read** `COMPLETE_API_REFERENCE.md` - Understand all endpoints
2. **Test** in Postman - Verify endpoints work
3. **Implement** session flow - Create session → Use endpoints
4. **Build** UI components - Use endpoint guides above
5. **Handle** errors - Implement error handling
6. **Optimize** - Cache where needed, use streaming for chat

---

## 📞 Key Endpoints to Implement First

**Priority 1 (Core):**
- `/session/create` - Session management
- `/ai/chat` - Chat interface
- `/progress/update` - Progress tracking

**Priority 2 (Features):**
- `/ai/chat/history/{session_id}` - Conversation history
- `/progress/{user_id}` - Progress display
- `/feedback/{user_id}/{topic_id}` - Feedback display

**Priority 3 (Enhancement):**
- `/recommendations/{user_id}/generate` - Recommendations
- `/proactive/progress-based-nudges/{user_id}` - Nudges
- `/documents/upload` - Document upload

**Priority 4 (Advanced):**
- `/voice/*` - Voice features
- `/learning-path/generate` - Learning paths
- `/analytics/*` - Analytics dashboard

---

## 📋 Implementation Checklist

- [ ] Read COMPLETE_API_REFERENCE.md
- [ ] Test endpoints in Postman
- [ ] Set up API client (Axios/Fetch wrapper)
- [ ] Implement session management
- [ ] Build chat interface
- [ ] Add progress tracking
- [ ] Implement error handling
- [ ] Add loading states
- [ ] Implement recommendations
- [ ] Add voice features (optional)
- [ ] Build analytics dashboard (optional)

---

## 🚀 Next Steps

1. **Share this document** with your frontend team
2. **Share COMPLETE_API_REFERENCE.md** for detailed specs
3. **Set up Postman** and test endpoints together
4. **Plan sprint** using Priority 1, 2, 3, 4 above
5. **Assign tasks** based on UI components needed

---

**Questions? Check COMPLETE_API_REFERENCE.md for detailed endpoint documentation! 📚**
