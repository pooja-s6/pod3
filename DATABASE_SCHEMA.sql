-- AI-TUTOR Database Schema
-- PostgreSQL DBMS Code for ER Diagram

-- ============================================
-- 1. USER TABLE (Users Table)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 2. TOPIC TABLE (Topics/Subjects Table)
-- ============================================
CREATE TABLE IF NOT EXISTS topics (
    topic_id VARCHAR(255) PRIMARY KEY,
    topic_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 3. AI_MODEL TABLE (AI Models Table)
-- ============================================
CREATE TABLE IF NOT EXISTS ai_models (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    provider VARCHAR(100) NOT NULL,
    base_cost DOUBLE PRECISION NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 4. CHAT TABLE (Main Chat/Interaction Table)
-- ============================================
CREATE TABLE IF NOT EXISTS chats (
    chat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    topic_id VARCHAR(255) NOT NULL,
    model_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    reply TEXT NOT NULL,
    tokens_used INTEGER NOT NULL,
    cost DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE,
    FOREIGN KEY (model_id) REFERENCES ai_models(model_id) ON DELETE CASCADE
);

-- ============================================
-- 5. USER_USAGE TABLE (Aggregated Usage Statistics)
-- ============================================
CREATE TABLE IF NOT EXISTS user_usage (
    usage_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    total_messages INTEGER DEFAULT 0,
    total_tokens_used INTEGER DEFAULT 0,
    total_cost DOUBLE PRECISION DEFAULT 0.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(user_id)
);

-- ============================================
-- 6. MODEL_USAGE TABLE (Model Usage Tracking)
-- ============================================
CREATE TABLE IF NOT EXISTS model_usage (
    model_usage_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    model_id INTEGER NOT NULL,
    usage_count INTEGER DEFAULT 0,
    total_tokens_used INTEGER DEFAULT 0,
    total_cost DOUBLE PRECISION DEFAULT 0.0,
    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (model_id) REFERENCES ai_models(model_id) ON DELETE CASCADE,
    UNIQUE(user_id, model_id)
);

-- ============================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================

-- Index on chat table for faster queries by user
CREATE INDEX idx_chats_user_id ON chats(user_id);

-- Index on chat table for faster queries by topic
CREATE INDEX idx_chats_topic_id ON chats(topic_id);

-- Index on chat table for faster queries by model
CREATE INDEX idx_chats_model_id ON chats(model_id);

-- Index on chat table for time-based queries
CREATE INDEX idx_chats_timestamp ON chats(timestamp);

-- Composite index for common queries (user + timestamp)
CREATE INDEX idx_chats_user_timestamp ON chats(user_id, timestamp DESC);

-- Index on user_usage table
CREATE INDEX idx_user_usage_user_id ON user_usage(user_id);

-- Index on model_usage table
CREATE INDEX idx_model_usage_user_id ON model_usage(user_id);
CREATE INDEX idx_model_usage_model_id ON model_usage(model_id);

-- ============================================
-- SAMPLE DATA FOR AI MODELS
-- ============================================

INSERT INTO ai_models (model_name, provider, base_cost, description) 
VALUES 
    ('gpt-4', 'openai', 0.00003, 'OpenAI GPT-4 model'),
    ('gpt-3.5-turbo', 'openai', 0.0000015, 'OpenAI GPT-3.5 Turbo model'),
    ('gemini-pro', 'google', 0.00005, 'Google Generative AI Gemini Pro'),
    ('llama-2-70b', 'meta', 0.0001, 'Meta LLaMA 2 70B model')
ON CONFLICT DO NOTHING;

-- ============================================
-- ER DIAGRAM REPRESENTATION
-- ============================================
/*
┌─────────────────┐         ┌──────────────────┐
│    USERS        │         │     TOPICS       │
├─────────────────┤         ├──────────────────┤
│ user_id (PK)    │         │ topic_id (PK)    │
│ username        │         │ topic_name       │
│ email           │         │ description      │
│ created_at      │         │ created_at       │
│ updated_at      │         └──────────────────┘
└────────┬────────┘                  ▲
         │                           │
         │ 1:N                       │ 1:N
         │                           │
         ├───────────────────────────┤
         │                           │
         └──────────────┬────────────┘
                        │
                   ┌────▼─────────────┐
                   │      CHATS       │
                   ├──────────────────┤
                   │ chat_id (PK,UUID)│
                   │ user_id (FK)     │ ◄─────┐
                   │ topic_id (FK)    │ ◄─────┤ 1:N
                   │ model_id (FK)    │ ◄──┐  │
                   │ message          │    │  │
                   │ reply            │    │  │
                   │ tokens_used      │    │  │
                   │ cost             │    │  │
                   │ timestamp        │    │  │
                   └─────────────────┘     │  │
                                           │  │
                   ┌──────────────────┐    │  │
                   │   AI_MODELS      │◄───┘  │
                   ├──────────────────┤       │
                   │ model_id (PK)    │       │
                   │ model_name       │       │
                   │ provider         │       │
                   │ base_cost        │       │
                   │ description      │       │
                   └──────────────────┘       │
                                             │
                   ┌──────────────────┐       │
                   │  USER_USAGE      │◄──────┘
                   ├──────────────────┤
                   │ usage_id (PK)    │
                   │ user_id (FK)     │
                   │ total_messages   │
                   │ total_tokens_used│
                   │ total_cost       │
                   │ last_updated     │
                   └──────────────────┘

                   ┌──────────────────┐
                   │  MODEL_USAGE     │
                   ├──────────────────┤
                   │ model_usage_id (PK)
                   │ user_id (FK)     │
                   │ model_id (FK)    │
                   │ usage_count      │
                   │ total_tokens_used│
                   │ total_cost       │
                   │ last_used        │
                   └──────────────────┘
*/

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- View: User Chat History
CREATE OR REPLACE VIEW user_chat_history AS
SELECT 
    c.chat_id,
    u.user_id,
    u.username,
    t.topic_id,
    t.topic_name,
    am.model_name,
    c.message,
    c.reply,
    c.tokens_used,
    c.cost,
    c.timestamp
FROM chats c
JOIN users u ON c.user_id = u.user_id
JOIN topics t ON c.topic_id = t.topic_id
JOIN ai_models am ON c.model_id = am.model_id
ORDER BY c.timestamp DESC;

-- View: User Spending by Model
CREATE OR REPLACE VIEW user_spending_by_model AS
SELECT 
    u.user_id,
    u.username,
    am.model_name,
    COUNT(c.chat_id) AS total_interactions,
    SUM(c.tokens_used) AS total_tokens,
    SUM(c.cost) AS total_spent
FROM chats c
JOIN users u ON c.user_id = u.user_id
JOIN ai_models am ON c.model_id = am.model_id
GROUP BY u.user_id, u.username, am.model_name
ORDER BY u.user_id, total_spent DESC;

-- View: User Statistics Summary
CREATE OR REPLACE VIEW user_statistics AS
SELECT 
    u.user_id,
    u.username,
    COUNT(c.chat_id) AS total_messages,
    SUM(c.tokens_used) AS total_tokens,
    SUM(c.cost) AS total_cost,
    ROUND(AVG(c.tokens_used)::NUMERIC, 2) AS avg_tokens_per_message,
    ROUND(AVG(c.cost)::NUMERIC, 6) AS avg_cost_per_message,
    MAX(c.timestamp) AS last_activity
FROM users u
LEFT JOIN chats c ON u.user_id = c.user_id
GROUP BY u.user_id, u.username;

-- ============================================
-- RELATIONSHIPS SUMMARY
-- ============================================
/*
RELATIONSHIPS:
1. USERS (1) ──────────────── (N) CHATS
   - One user can have many chats

2. TOPICS (1) ──────────────── (N) CHATS
   - One topic can have many chats

3. AI_MODELS (1) ──────────────── (N) CHATS
   - One AI model can be used in many chats

4. USERS (1) ──────────────── (1) USER_USAGE
   - One user has one usage record

5. USERS (1) ──────────────── (N) MODEL_USAGE
   - One user can have usage records for multiple models

6. AI_MODELS (1) ──────────────── (N) MODEL_USAGE
   - One model can have usage records for multiple users

CONSTRAINTS:
- ON DELETE CASCADE: If a user is deleted, all related chats and usage records are deleted
- UNIQUE constraints ensure data integrity
- Foreign keys maintain referential integrity
*/

-- ============================================
-- USEFUL QUERIES FOR ANALYTICS
-- ============================================

-- Query 1: Get user's total usage and spending
/*
SELECT user_id, 
       total_messages, 
       total_tokens_used, 
       total_cost 
FROM user_usage 
WHERE user_id = 'user_123';
*/

-- Query 2: Get chat history for a user
/*
SELECT * FROM user_chat_history 
WHERE user_id = 'user_123' 
ORDER BY timestamp DESC;
*/

-- Query 3: Get user's spending by model
/*
SELECT * FROM user_spending_by_model 
WHERE user_id = 'user_123';
*/

-- Query 4: Top 10 most expensive interactions
/*
SELECT chat_id, user_id, model_name, tokens_used, cost, timestamp
FROM user_chat_history
ORDER BY cost DESC
LIMIT 10;
*/

-- Query 5: Average cost per user per topic
/*
SELECT u.username, t.topic_name, 
       COUNT(*) as interactions,
       AVG(c.cost) as avg_cost,
       SUM(c.cost) as total_cost
FROM chats c
JOIN users u ON c.user_id = u.user_id
JOIN topics t ON c.topic_id = t.topic_id
GROUP BY u.user_id, u.username, t.topic_id, t.topic_name
ORDER BY u.username, total_cost DESC;
*/
