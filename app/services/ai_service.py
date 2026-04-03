"""AI Service for OpenAI integration."""

from openai import OpenAI, AsyncOpenAI
from app.core.config import settings
from app.services.prompt_builder import prompt_builder
import json


class AIService:
    """Service for AI interactions with OpenAI API."""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.async_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
        self.max_tokens = settings.OPENAI_MAX_TOKENS
    
    def chat(self, system_prompt: str, messages: list, user_message: str = None) -> str:
        """Send a chat request to OpenAI and get response."""
        try:
            # Build messages if user_message is provided
            if user_message:
                conversation_messages = prompt_builder.build_conversation_messages(
                    system_prompt, messages, user_message
                )
            else:
                conversation_messages = [{"role": "system", "content": system_prompt}] + messages
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=conversation_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def chat_stream(self, system_prompt: str, messages: list, user_message: str = None):
        """Stream chat response from OpenAI."""
        try:
            # Build messages if user_message is provided
            if user_message:
                conversation_messages = prompt_builder.build_conversation_messages(
                    system_prompt, messages, user_message
                )
            else:
                conversation_messages = [{"role": "system", "content": system_prompt}] + messages
            
            stream = await self.async_client.chat.completions.create(
                model=self.model,
                messages=conversation_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def get_embedding(self, text: str) -> list:
        """Get embeddings for text (for RAG use cases)."""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None
    
    def validate_api_key(self) -> bool:
        """Validate that OpenAI API key is valid."""
        try:
            self.client.models.list()
            return True
        except Exception as e:
            print(f"API Key validation failed: {e}")
            return False
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio file to text using OpenAI Whisper."""
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            print(f"Transcription error: {e}")
            return f"Error transcribing audio: {str(e)}"
    
    def text_to_speech(self, text: str, voice: str = "alloy") -> bytes:
        """Convert text to speech using OpenAI TTS."""
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            return response.content
        except Exception as e:
            print(f"TTS error: {e}")
            return None


# Global AI service instance
ai_service = AIService()
