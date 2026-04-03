"""Prompt builder for different chat modes."""


class PromptBuilder:
    """Build prompts based on chat modes and context."""
    
    # System prompts for different modes
    TEACHING_MODE_SYSTEM = """You are an AI tutor in a learning platform. Your role is to:
- Provide detailed, comprehensive explanations
- Include step-by-step breakdowns
- Give practical examples
- Encourage learning and understanding
- Be patient and supportive

Always ensure your responses are educational and help the student learn effectively."""

    GUIDING_MODE_SYSTEM = """You are a Socratic tutor in a learning platform. Your role is to:
- Ask thought-provoking questions
- Guide students to discover answers themselves
- Provide hints instead of direct answers
- Encourage critical thinking
- Help students develop problem-solving skills

Never give direct answers. Instead, guide the student to find their own solutions."""

    NORMAL_MODE_SYSTEM = """You are a helpful AI assistant in a learning platform. Your role is to:
- Answer questions clearly and accurately
- Provide relevant information
- Be concise and direct
- Help with learning-related queries
- Maintain a friendly and supportive tone."""

    QUIZ_MODE_SYSTEM = """You are assisting a student during a quiz. IMPORTANT RULES:
- DO NOT provide direct answers to quiz questions
- Provide hints and guidance only
- Ask clarifying questions about what the student understands
- Guide them to think through the problem
- Never reveal the answer, even if asked directly"""

    def __init__(self):
        self.mode_systems = {
            "teaching": self.TEACHING_MODE_SYSTEM,
            "guiding": self.GUIDING_MODE_SYSTEM,
            "normal": self.NORMAL_MODE_SYSTEM,
            "quiz": self.QUIZ_MODE_SYSTEM
        }
    
    def build_system_prompt(self, mode: str = "normal", lesson_context: str = None, quiz_context: str = None) -> str:
        """Build system prompt based on mode and context."""
        system_prompt = self.mode_systems.get(mode, self.NORMAL_MODE_SYSTEM)
        
        # Add context if provided
        if lesson_context:
            system_prompt += f"\n\nLESSSON CONTEXT:\n{lesson_context}"
        
        if quiz_context:
            system_prompt += f"\n\nQUIZ CONTEXT:\n{quiz_context}"
        
        return system_prompt
    
    def build_conversation_messages(self, system_prompt: str, context_messages: list, user_message: str) -> list:
        """Build the messages list for OpenAI API."""
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add context messages (conversation history)
        for msg in context_messages:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
    def build_rag_prompt(self, mode: str, user_message: str, retrieved_context: str = None) -> str:
        """Build prompt with RAG context injection."""
        base_prompt = f"{user_message}"
        
        if retrieved_context:
            base_prompt = f"Context from documents:\n{retrieved_context}\n\nUser question: {user_message}"
        
        return base_prompt


# Global prompt builder instance
prompt_builder = PromptBuilder()
