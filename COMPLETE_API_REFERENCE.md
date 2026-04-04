# Complete API Reference with Feature Explanation, Endpoints, JSON Bodies & Responses

---

## Chat Endpoints

### 1. **Send Message to AI Tutor**

**Feature:** Send a message to the AI tutor and receive contextual learning responses.

**Endpoint:** `POST /ai/chat`

**Request Body:**
```json
{
  "session_id": "sess-123",
  "message": "Your question here",
  "mode": "normal"
}
```

**Response Format:**
```json
{
  "session_id": "sess-123",
  "user_message": "Your question here",
  "ai_response": "Here is the answer...",
  "mode": "normal",
  "timestamp": "2024-04-04T10:30:00Z",
  "tokens_used": 125
}
```

---

### 2. **Stream Chat Response**

**Feature:** Get real-time streaming responses from AI tutor for interactive conversations.

**Endpoint:** `POST /ai/chat/stream`

**Request Body:**
```json
{
  "session_id": "sess-123",
  "message": "Your question here",
  "mode": "teaching"
}
```

**Response Format:**
```json
{
  "session_id": "sess-123",
  "stream_id": "stream-abc",
  "chunks": [
    "Here ",
    "is ",
    "the ",
    "streaming ",
    "response..."
  ],
  "mode": "teaching",
  "total_tokens": 145
}
```

---

### 3. **Get Chat History**

**Feature:** Retrieve all previous messages and responses in a learning session.

**Endpoint:** `GET /ai/chat/history/{session_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "session_id": "sess-123",
  "messages": [
    {
      "role": "student",
      "content": "What is photosynthesis?",
      "timestamp": "2024-04-04T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Photosynthesis is the process...",
      "timestamp": "2024-04-04T10:01:00Z"
    }
  ],
  "total_messages": 12,
  "session_duration_minutes": 45
}
```

---

### 4. **Quick AI Suggestions**

**Feature:** Get AI-powered quick suggestions for a specific concept without full conversation.

**Endpoint:** `POST /ai/quick-suggestions`

**Request Body:**
```json
{
  "session_id": "sess-123",
  "concept": "Photosynthesis",
  "topic_id": "biology-101"
}
```

**Response Format:**
```json
{
  "concept": "Photosynthesis",
  "suggestions": [
    "Try breaking down the light-dependent and light-independent reactions",
    "Remember the role of chlorophyll in absorbing light energy",
    "Don't forget to include the importance of stomata"
  ],
  "difficulty_level": "intermediate",
  "estimated_read_time_minutes": 5
}
```

---

### 5. **Contextual Learning Chat**

**Feature:** Get AI responses with context awareness from lessons, quizzes, or documents.

**Endpoint:** `POST /ai/contextual`

**Request Body:**
```json
{
  "session_id": "sess-123",
  "message": "I dont understand this",
  "lesson_id": "lesson-456",
  "quiz_id": null,
  "context_type": "lesson"
}
```

**Response Format:**
```json
{
  "session_id": "sess-123",
  "message": "I dont understand this",
  "contextual_response": "Based on the lesson content, here's a simpler explanation...",
  "context_type": "lesson",
  "related_concepts": ["concept1", "concept2"],
  "recommendation": "Review the fundamentals section before proceeding"
}
```

---

## Session Endpoints

### 6. **Create Learning Session**

**Feature:** Initialize a new learning session for a student.

**Endpoint:** `POST /session/create`

**Request Body:** No body required

**Response Format:**
```json
{
  "session_id": "sess-abc123xyz",
  "user_id": "student-001",
  "created_at": "2024-04-04T09:00:00Z",
  "status": "active",
  "expiry_time": "2024-04-05T09:00:00Z"
}
```

---

### 7. **Get Session Details**

**Feature:** Retrieve information about a specific learning session.

**Endpoint:** `GET /session/{session_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "session_id": "sess-123",
  "user_id": "student-001",
  "created_at": "2024-04-04T09:00:00Z",
  "last_activity": "2024-04-04T10:45:00Z",
  "status": "active",
  "duration_minutes": 105,
  "messages_count": 23,
  "topics_covered": ["algebra", "geometry"]
}
```

---

### 8. **Get User Sessions**

**Feature:** Retrieve all active and past learning sessions for a user.

**Endpoint:** `GET /session/user/{user_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "user_id": "student-001",
  "sessions": [
    {
      "session_id": "sess-123",
      "created_at": "2024-04-04T09:00:00Z",
      "status": "active",
      "duration_minutes": 105
    },
    {
      "session_id": "sess-456",
      "created_at": "2024-04-03T10:00:00Z",
      "status": "closed",
      "duration_minutes": 45
    }
  ],
  "total_sessions": 15
}
```

---

## Progress Endpoints

### 9. **Update Progress**

**Feature:** Log student progress data including scores, attempts, and time spent on topics.

**Endpoint:** `POST /progress/update`

**Request Body:**
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

**Response Format:**
```json
{
  "user_id": "student-123",
  "topic_id": "algebra",
  "score": 85.5,
  "progress_percentage": 75,
  "updated_at": "2024-04-04T10:30:00Z",
  "next_milestone": 90,
  "milestone_progress": "5.5 points away"
}
```

---

### 10. **Get User Progress**

**Feature:** Retrieve comprehensive progress data across all topics for a student.

**Endpoint:** `GET /progress/{user_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "user_id": "student-123",
  "overall_progress": 72.5,
  "topics": [
    {
      "topic_id": "algebra",
      "score": 85.5,
      "progress": 75,
      "last_updated": "2024-04-04T10:30:00Z"
    },
    {
      "topic_id": "geometry",
      "score": 72.0,
      "progress": 60,
      "last_updated": "2024-04-03T15:20:00Z"
    }
  ],
  "total_topics": 8,
  "topics_completed": 3
}
```

---

### 11. **Get Progress Statistics**

**Feature:** Get detailed progress statistics including trends, performance metrics, and learning velocity.

**Endpoint:** `GET /progress/stats/{user_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "user_id": "student-123",
  "average_score": 78.3,
  "highest_score": 92.5,
  "lowest_score": 55.0,
  "total_time_spent_hours": 45.5,
  "learning_velocity": "20% improvement in last 7 days",
  "performance_trend": "improving",
  "completion_rate": "62.5%",
  "estimated_completion_date": "2024-05-15"
}
```

---

## Adaptive Learning Endpoints

### 12. **Get Next Topic**

**Feature:** Recommend the next optimal topic based on current progress and learning patterns.

**Endpoint:** `POST /adaptive/next-topic`

**Request Body:**
```json
{
  "user_id": "student-123",
  "current_topic": "algebra"
}
```

**Response Format:**
```json
{
  "user_id": "student-123",
  "current_topic": "algebra",
  "next_topic": "quadratic_equations",
  "difficulty": "intermediate",
  "readiness_score": 82,
  "why_this_topic": "Strong foundation in linear algebra makes you ready for quadratic equations",
  "estimated_duration_minutes": 120
}
```

---

### 13. **Assess Topic Mastery**

**Feature:** Evaluate student's mastery level for a topic based on performance metrics.

**Endpoint:** `POST /adaptive/assess`

**Request Body:**
```json
{
  "topic_id": "algebra",
  "score": 75.0,
  "time_spent_seconds": 1200
}
```

**Response Format:**
```json
{
  "topic_id": "algebra",
  "score": 75.0,
  "mastery_level": "intermediate",
  "confidence_score": 78,
  "assessment": {
    "strengths": ["Solves linear equations", "Understands variables"],
    "weaknesses": ["Struggles with complex factoring", "Needs practice with word problems"],
    "recommendation": "Practice factoring before moving to quadratics"
  },
  "next_action": "remedial_exercises"
}
```

---

### 14. **Adjust Difficulty Level**

**Feature:** Dynamically adjust learning difficulty based on student performance.

**Endpoint:** `POST /adaptive/adjust-difficulty`

**Request Body:**
```json
{
  "current_difficulty": "intermediate",
  "last_score": 65.5
}
```

**Response Format:**
```json
{
  "previous_difficulty": "intermediate",
  "new_difficulty": "beginner",
  "adjustment_reason": "Score below 70% - reducing difficulty to build confidence",
  "effective_from": "2024-04-04T11:00:00Z",
  "encouragement": "Take your time to strengthen the fundamentals!"
}
```

---

## Feedback Endpoints

### 15. **Get Personalized Feedback**

**Feature:** Generate AI-powered, personalized feedback on student performance for a specific topic.

**Endpoint:** `POST /feedback/{user_id}/{topic_id}`

**Request Body:** No body required (IDs in path)

**Response Format:**
```json
{
  "user_id": "student-123",
  "topic_id": "algebra",
  "feedback": "Great job on linear equations! Your approach is systematic and logical.",
  "areas_of_excellence": ["Problem-solving methodology", "Accuracy"],
  "areas_for_improvement": ["Speed of calculations", "Handling edge cases"],
  "actionable_steps": [
    "Practice mental math exercises",
    "Try timed quizzes to improve speed",
    "Review edge cases in algebra"
  ],
  "encouragement_level": "positive",
  "next_focus": "quadratic_equations"
}
```

---

### 16. **Get All Feedback for User**

**Feature:** Retrieve all feedback history provided to a student across topics.

**Endpoint:** `GET /feedback/{user_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "user_id": "student-123",
  "total_feedback_items": 8,
  "feedback_history": [
    {
      "topic_id": "algebra",
      "date": "2024-04-04T10:30:00Z",
      "summary": "Strong performance on linear equations",
      "sentiment": "positive"
    },
    {
      "topic_id": "geometry",
      "date": "2024-04-02T14:15:00Z",
      "summary": "Need improvement in spatial reasoning",
      "sentiment": "constructive"
    }
  ]
}
```

---

### 17. **Get Performance Gap Analysis**

**Feature:** Identify and analyze performance gaps between current and target scores for improvement planning.

**Endpoint:** `POST /feedback/performance-gap/{user_id}`

**Request Body:**
```json
{
  "topic_id": "algebra",
  "current_score": 65,
  "target_score": 85
}
```

**Response Format:**
```json
{
  "user_id": "student-123",
  "topic_id": "algebra",
  "current_score": 65,
  "target_score": 85,
  "gap": 20,
  "gap_percentage": "19%",
  "estimated_effort_hours": 12,
  "gap_analysis": {
    "weak_areas": ["Factoring polynomials", "Complex word problems"],
    "strength_areas": ["Basic operations", "Linear equations"]
  },
  "closure_strategy": [
    "Focus on factoring for 3 hours daily",
    "Solve 10 word problems daily",
    "Weekly practice tests"
  ],
  "timeline": "2-3 weeks with consistent effort"
}
```

---

### 18. **Get Strengths and Weaknesses**

**Feature:** Generate a detailed analysis of student strengths and weaknesses for a topic.

**Endpoint:** `POST /feedback/strengths-weaknesses/{user_id}`

**Request Body:**
```json
{
  "topic_id": "biology"
}
```

**Response Format:**
```json
{
  "user_id": "student-123",
  "topic_id": "biology",
  "overall_analysis": {
    "strengths": [
      "Excellent understanding of cell structure",
      "Strong grasp of photosynthesis",
      "Good memorization skills for biological terms"
    ],
    "weaknesses": [
      "Struggles with ecology concepts",
      "Difficulty connecting macro and micro concepts",
      "Weak on genetics problems"
    ]
  },
  "strength_score": 78,
  "weakness_score": 45,
  "balanced_assessment": "Your foundational knowledge is solid; focus on integrative concepts",
  "recommended_next_steps": [
    "Begin ecology unit with visual diagrams",
    "Practice interconnected concept maps",
    "Work through genetics step-by-step"
  ]
}
```

---

## Proactive Learning Endpoints

### 19. **Get Progress-Based Nudges**

**Feature:** Send intelligent, timely nudges to students based on their learning progress and engagement patterns.

**Endpoint:** `POST /proactive/progress-based-nudges/{user_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "user_id": "student-123",
  "nudges": [
    {
      "type": "milestone",
      "message": "You're 5 points away from mastering Algebra! One more practice session should do it.",
      "urgency": "high",
      "action": "Take a practice quiz"
    },
    {
      "type": "encouragement",
      "message": "Great progress this week! Your learning velocity is improving.",
      "urgency": "low",
      "action": null
    }
  ],
  "total_nudges": 3,
  "generated_at": "2024-04-04T11:00:00Z"
}
```

---

### 20. **Get Smart Reminders**

**Feature:** Provide contextual reminders based on learning streaks, pending work, and practice recommendations.

**Endpoint:** `POST /proactive/smart-reminders/{user_id}`

**Request Body:**
```json
{
  "include_streak": true,
  "include_pending": true
}
```

**Response Format:**
```json
{
  "user_id": "student-123",
  "reminders": {
    "streak_reminder": {
      "current_streak": 7,
      "message": "Keep your 7-day learning streak alive! Just 15 minutes of practice today.",
      "motivational_message": "You're on fire! 🔥"
    },
    "pending_reminder": {
      "pending_items": 3,
      "message": "You have 3 incomplete exercises from yesterday",
      "topics": ["algebra", "geometry"]
    },
    "recommended_practice": {
      "suggested_activity": "Quadratic equations practice",
      "estimated_time": 30,
      "reasoning": "Based on your recent struggles with this topic"
    }
  },
  "reminder_sent_at": "2024-04-04T08:00:00Z"
}
```

---

### 21. **Get Engagement Level**

**Feature:** Assess and retrieve current student engagement level and provide recommendations.

**Endpoint:** `GET /proactive/engagement-level/{user_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "user_id": "student-123",
  "engagement_score": 78,
  "engagement_level": "high",
  "metrics": {
    "sessions_this_week": 5,
    "daily_active_minutes": 45,
    "completion_rate": 85,
    "session_consistency": 0.8
  },
  "trend": "slightly increasing",
  "insights": "Your engagement has been consistently high. Keep up the excellent work!",
  "low_engagement_warning": false,
  "recommendation": "You're on track! Consider exploring advanced topics to maintain momentum."
}
```

---

### 22. **Get Motivational Nudge**

**Feature:** Generate context-aware motivational messages and achievement recognition.

**Endpoint:** `POST /proactive/motivational-nudge/{user_id}`

**Request Body:**
```json
{
  "include_achievements": true
}
```

**Response Format:**
```json
{
  "user_id": "student-123",
  "motivational_message": "You've made incredible progress this month! From 45% to 78% in Algebra shows real dedication.",
  "achievements": [
    {
      "name": "Algebra Master",
      "description": "Reached 80+ in Algebra",
      "date_earned": "2024-04-04"
    },
    {
      "name": "Perfect Week",
      "description": "7-day learning streak completed",
      "date_earned": "2024-04-03"
    }
  ],
  "milestone_progress": {
    "next_milestone": "Complete 10 topics",
    "current_progress": 7,
    "progress_percentage": 70
  },
  "encouragement": "You're inspiring others with your commitment. Keep going!"
}
```

---

## Learning Path Endpoints

### 23. **Generate Learning Path**

**Feature:** Create a personalized learning path based on student goals and available time.

**Endpoint:** `POST /learning-path/generate`

**Request Body:**
```json
{
  "goal": "Master Data Structures",
  "duration_days": 30
}
```

**Response Format:**
```json
{
  "goal": "Master Data Structures",
  "duration_days": 30,
  "learning_path": [
    {
      "week": 1,
      "topics": ["Arrays", "Lists"],
      "daily_time_commitment": 45,
      "estimated_completion_date": "2024-04-14"
    },
    {
      "week": 2,
      "topics": ["Stacks", "Queues"],
      "daily_time_commitment": 45,
      "estimated_completion_date": "2024-04-21"
    },
    {
      "week": 3,
      "topics": ["Trees", "Binary Trees"],
      "daily_time_commitment": 45,
      "estimated_completion_date": "2024-04-28"
    },
    {
      "week": 4,
      "topics": ["Graphs", "Hash Tables"],
      "daily_time_commitment": 45,
      "estimated_completion_date": "2024-05-04"
    }
  ],
  "total_topics": 8,
  "expected_completion_date": "2024-05-04",
  "difficulty_distribution": "progressive"
}
```

---

## Recommendation Endpoints

### 24. **Generate Recommendations**

**Feature:** Generate AI-powered personalized learning recommendations based on student profile and performance.

**Endpoint:** `POST /recommendations/{user_id}/generate`

**Request Body:** No body required

**Response Format:**
```json
{
  "user_id": "student-123",
  "recommendations": [
    {
      "recommendation_id": "rec-001",
      "type": "next_topic",
      "title": "Quadratic Equations",
      "reason": "You've mastered linear equations and are ready for the next challenge",
      "estimated_duration_hours": 8,
      "difficulty": "intermediate",
      "success_probability": 0.85
    },
    {
      "recommendation_id": "rec-002",
      "type": "remedial",
      "title": "Review Polynomial Factoring",
      "reason": "You scored 62% on factoring problems. Revisiting this will help with quadratics",
      "estimated_duration_hours": 3,
      "difficulty": "beginner",
      "success_probability": 0.92
    }
  ],
  "total_recommendations": 2,
  "generated_at": "2024-04-04T11:30:00Z"
}
```

---

### 25. **Get User Recommendations**

**Feature:** Retrieve all current recommendations for a student.

**Endpoint:** `GET /recommendations/{user_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "user_id": "student-123",
  "recommendations": [
    {
      "recommendation_id": "rec-001",
      "title": "Quadratic Equations",
      "type": "next_topic",
      "status": "pending",
      "created_at": "2024-04-04T11:30:00Z",
      "priority": "high"
    },
    {
      "recommendation_id": "rec-002",
      "title": "Review Polynomial Factoring",
      "type": "remedial",
      "status": "in_progress",
      "created_at": "2024-04-02T14:00:00Z",
      "priority": "high"
    }
  ],
  "pending_count": 1,
  "in_progress_count": 1,
  "completed_count": 0
}
```

---

### 26. **Acknowledge Recommendation**

**Feature:** Allow students to confirm they have started working on a recommendation.

**Endpoint:** `POST /recommendations/acknowledge/{recommendation_id}`

**Request Body:**
```json
{
  "user_id": "student-123"
}
```

**Response Format:**
```json
{
  "recommendation_id": "rec-001",
  "user_id": "student-123",
  "status": "acknowledged",
  "acknowledged_at": "2024-04-04T12:00:00Z",
  "message": "Great! We'll track your progress on this topic.",
  "expected_completion_date": "2024-04-07"
}
```

---

## Document Endpoints

### 27. **Upload Document**

**Feature:** Upload learning documents (PDF, Word, Images) for AI analysis and chat.

**Endpoint:** `POST /documents/upload`

**Request Body:** Form data (Multipart)
```
file: <document_file> (PDF, DOCX, JPG, PNG, TXT)
session_id: "sess-123"
```

**Response Format:**
```json
{
  "document_id": "doc-abc123",
  "filename": "Biology_Chapter_5.pdf",
  "file_type": "pdf",
  "session_id": "sess-123",
  "upload_time": "2024-04-04T11:45:00Z",
  "file_size_kb": 2450,
  "status": "processed",
  "page_count": 18,
  "processing_status": "completed"
}
```

---

### 28. **Get Document**

**Feature:** Retrieve details and metadata of an uploaded document.

**Endpoint:** `GET /documents/{doc_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "document_id": "doc-abc123",
  "filename": "Biology_Chapter_5.pdf",
  "session_id": "sess-123",
  "upload_time": "2024-04-04T11:45:00Z",
  "file_size_kb": 2450,
  "page_count": 18,
  "content_summary": "Chapter covers photosynthesis, cellular respiration, and energy conversion...",
  "key_topics": ["photosynthesis", "ATP", "mitochondria"],
  "status": "ready_for_analysis"
}
```

---

### 29. **Ask Question About Document**

**Feature:** Ask AI questions about an uploaded document's content for deep understanding.

**Endpoint:** `POST /documents/{doc_id}/ask`

**Request Body:**
```json
{
  "session_id": "sess-123",
  "question": "Summarize the photosynthesis process",
  "context_length": 5
}
```

**Response Format:**
```json
{
  "document_id": "doc-abc123",
  "question": "Summarize the photosynthesis process",
  "answer": "Photosynthesis is a biochemical process where plants use sunlight to convert carbon dioxide and water into glucose and oxygen. It occurs in two stages: light-dependent reactions in the thylakoids and light-independent reactions (Calvin cycle) in the stroma. This process is fundamental to life on Earth as it produces oxygen and glucose needed by most organisms.",
  "source_pages": [5, 6, 7],
  "confidence_score": 0.92,
  "related_concepts": ["cellular_respiration", "ATP", "chlorophyll"]
}
```

---

### 30. **List Documents in Session**

**Feature:** Get all documents uploaded in a learning session.

**Endpoint:** `GET /documents/list/{session_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "session_id": "sess-123",
  "documents": [
    {
      "document_id": "doc-abc123",
      "filename": "Biology_Chapter_5.pdf",
      "upload_time": "2024-04-04T11:45:00Z",
      "file_size_kb": 2450
    },
    {
      "document_id": "doc-xyz789",
      "filename": "Study_Guide.docx",
      "upload_time": "2024-04-04T10:30:00Z",
      "file_size_kb": 340
    }
  ],
  "total_documents": 2,
  "total_size_kb": 2790
}
```

---

### 31. **Delete Document**

**Feature:** Remove an uploaded document from the learning session.

**Endpoint:** `DELETE /documents/{doc_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "document_id": "doc-abc123",
  "status": "deleted",
  "message": "Document successfully deleted",
  "deleted_at": "2024-04-04T12:15:00Z"
}
```

---

## Voice Endpoints

### 32. **Transcribe Audio**

**Feature:** Convert spoken audio to text using AI speech recognition.

**Endpoint:** `POST /voice/transcribe`

**Request Body:** Form data (Multipart)
```
file: <audio_file> (MP3, WAV, M4A, OGG, FLAC, PCM)
```

**Response Format:**
```json
{
  "transcription_id": "trans-123",
  "transcript": "What is the capital of France?",
  "confidence_score": 0.96,
  "duration_seconds": 3.5,
  "language": "en",
  "processing_time_ms": 450
}
```

---

### 33. **Chat with Voice Input & Output**

**Feature:** Send voice messages and receive spoken responses from the AI tutor.

**Endpoint:** `POST /voice/chat-and-speak`

**Request Body:** Form data (Multipart)
```
file: <audio_file> (MP3, WAV, M4A, OGG, FLAC, PCM)
session_id: "sess-123"
mode: "normal"
include_speech: true
voice: "alloy"
```

**Response Format:**
```json
{
  "session_id": "sess-123",
  "transcribed_question": "What is the capital of France?",
  "ai_response": "The capital of France is Paris. It's located in the north-central part of the country and is known for its historical landmarks and cultural significance.",
  "audio_response": {
    "url": "https://api.example.com/audio/response-123.mp3",
    "duration_seconds": 8.5,
    "voice": "alloy"
  },
  "confidence_score": 0.94
}
```

---

### 34. **Text to Speech**

**Feature:** Convert AI responses or any text into natural-sounding speech.

**Endpoint:** `POST /voice/text-to-speech`

**Request Body:**
```json
{
  "text": "The capital of France is Paris",
  "voice": "alloy"
}
```

**Response Format:**
```json
{
  "text": "The capital of France is Paris",
  "audio_url": "https://api.example.com/audio/tts-123.mp3",
  "duration_seconds": 4.2,
  "voice": "alloy",
  "format": "mp3",
  "file_size_kb": 89
}
```

---

## Analytics Endpoints

### 35. **Get Session Analytics**

**Feature:** Retrieve detailed analytics data for a specific learning session.

**Endpoint:** `GET /analytics/session/{session_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "session_id": "sess-123",
  "user_id": "student-001",
  "analytics": {
    "duration_minutes": 105,
    "messages_count": 23,
    "topics_covered": ["algebra", "geometry"],
    "average_response_time_seconds": 2.5,
    "ai_response_quality_score": 0.89,
    "student_satisfaction": 0.92,
    "questions_asked": 15,
    "clarifications_needed": 3
  },
  "session_insights": "Good engagement with 2 topics covered. Student showed strong understanding.",
  "recorded_at": "2024-04-04T11:00:00Z"
}
```

---

### 36. **Get User Analytics**

**Feature:** Retrieve aggregated analytics across all sessions for a user.

**Endpoint:** `GET /analytics/user/{user_id}`

**Request Body:** No body required

**Response Format:**
```json
{
  "user_id": "student-123",
  "analytics": {
    "total_sessions": 14,
    "total_learning_hours": 42.5,
    "average_session_duration": 45.5,
    "topics_explored": 8,
    "questions_asked": 156,
    "average_satisfaction": 0.88,
    "growth_rate": "12% weekly improvement"
  },
  "trends": {
    "session_frequency": "daily",
    "engagement_trend": "improving",
    "performance_trend": "steadily increasing"
  },
  "recommendations": "Maintain current learning pace and explore advanced topics"
}
```

---

### 37. **Get Global Analytics**

**Feature:** Retrieve platform-wide analytics across all users and sessions.

**Endpoint:** `GET /analytics/global`

**Request Body:** No body required

**Response Format:**
```json
{
  "analytics": {
    "total_users": 1250,
    "active_users_today": 380,
    "total_sessions": 8450,
    "total_learning_hours": 21340,
    "average_session_duration": 45.2,
    "most_popular_topic": "algebra",
    "platform_ai_response_quality": 0.87,
    "user_satisfaction_average": 0.85
  },
  "daily_stats": {
    "new_users": 45,
    "sessions_today": 380,
    "total_questions_answered": 4560,
    "features_used": {
      "chat": 2100,
      "documents": 340,
      "voice": 180,
      "recommendations": 940
    }
  }
}
```

---

### 38. **Analytics Cleanup**

**Feature:** Archive or clean up old analytics data for database optimization.

**Endpoint:** `POST /analytics/cleanup`

**Request Body:** No body required

**Response Format:**
```json
{
  "action": "cleanup",
  "records_archived": 5400,
  "records_deleted": 1200,
  "freed_storage_mb": 450,
  "cleanup_timestamp": "2024-04-04T03:00:00Z",
  "next_cleanup": "2024-04-11T03:00:00Z",
  "status": "completed successfully"
}
```

---

## Health & Info Endpoints

### 39. **Health Check**

**Feature:** Verify the API server and database are healthy and operational.

**Endpoint:** `GET /health`

**Request Body:** No body required

**Response Format:**
```json
{
  "status": "healthy",
  "timestamp": "2024-04-04T12:00:00Z",
  "app": "AI Learning Tutor & Chatbot Backend",
  "version": "2.0.0",
  "database": "connected",
  "openai_api": "operational",
  "uptime_hours": 245.5,
  "response_time_ms": 3
}
```

---

### 40. **Home Endpoint**

**Feature:** Access basic information and API documentation link.

**Endpoint:** `GET /`

**Request Body:** No body required

**Response Format:**
```json
{
  "message": "Welcome to AI Learning Tutor API",
  "version": "2.0.0",
  "status": "running",
  "documentation_url": "http://localhost:8000/docs",
  "health_check": "http://localhost:8000/health",
  "contact": "support@aitutor.com"
}
```

---

## Summary by Category

| Category | Count | Key Endpoints |
|----------|-------|---|
| **Chat** | 5 | `/ai/chat`, `/ai/chat/stream`, `/ai/quick-suggestions`, `/ai/contextual` |
| **Session** | 3 | `/session/create`, `/session/{id}`, `/session/user/{user_id}` |
| **Progress** | 3 | `/progress/update`, `/progress/{user_id}`, `/progress/stats/{user_id}` |
| **Adaptive Learning** | 3 | `/adaptive/next-topic`, `/adaptive/assess`, `/adaptive/adjust-difficulty` |
| **Feedback** | 4 | `/feedback/{user}/{topic}`, `/feedback/performance-gap`, `/feedback/strengths-weaknesses` |
| **Proactive Learning** | 4 | `/proactive/progress-based-nudges`, `/proactive/smart-reminders`, `/proactive/engagement-level`, `/proactive/motivational-nudge` |
| **Learning Path** | 1 | `/learning-path/generate` |
| **Recommendations** | 3 | `/recommendations/{user}/generate`, `/recommendations/{user}`, `/recommendations/acknowledge` |
| **Documents** | 5 | `/documents/upload`, `/documents/{id}`, `/documents/{id}/ask`, `/documents/list`, `/documents/{id}/delete` |
| **Voice** | 3 | `/voice/transcribe`, `/voice/chat-and-speak`, `/voice/text-to-speech` |
| **Analytics** | 4 | `/analytics/session`, `/analytics/user`, `/analytics/global`, `/analytics/cleanup` |
| **Health/Info** | 2 | `/health`, `/` |
| **TOTAL** | **40** | |

---

## Testing Checklist

- [ ] Health check endpoint
- [ ] Create session
- [ ] Send chat message
- [ ] Get chat history
- [ ] Update progress
- [ ] Get recommendations
- [ ] Upload document
- [ ] Ask document question
- [ ] Transcribe audio
- [ ] Check analytics

**Ready to test in Postman! 🚀**
