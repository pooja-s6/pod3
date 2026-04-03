# Summary Service - Generates summaries and notes from lessons
from .ai_service import generate_ai_reply
from .prompt_builder import get_summary_prompt
from datetime import datetime

def generate_summary(content: str, summary_type: str = "short", context: dict = None) -> dict:
    """
    Generate a summary/notes from content using AI.
    
    Args:
        content: Content to summarize (lesson, explanation, etc.)
        summary_type: Type of summary (short, detailed, bullet-points)
        context: User context for personalization
        
    Returns:
        Generated summary
    """
    
    prompt = get_summary_prompt(content, summary_type, context)
    
    summary_text, tokens = generate_ai_reply(prompt)
    
    result = {
        "original_length": len(content.split()),
        "summary_type": summary_type,
        "summary": summary_text,
        "key_points": extract_key_points(summary_text),
        "tokens_used": tokens,
        "generated_at": datetime.utcnow().isoformat()
    }
    
    return result


def extract_key_points(summary: str) -> list:
    """Extract bullet points from summary."""
    
    lines = summary.split("\n")
    key_points = [line.strip() for line in lines if line.strip() and 
                  (line.strip().startswith(("•", "-", "*")) or 
                   (len(line.strip()) > 0 and line.strip()[0].isdigit()))]
    
    return key_points[:10]  # Top 10 points


def create_study_notes(topic: str, depth: str = "medium", context: dict = None) -> dict:
    """
    Create comprehensive study notes for a topic.
    
    Args:
        topic: Topic to create notes for
        depth: Depth of notes (light, medium, detailed)
        context: User context for personalization
        
    Returns:
        Generated notes
    """
    
    prompt = get_summary_prompt(topic, f"detailed_notes_{depth}", context)
    
    notes_text, tokens = generate_ai_reply(prompt)
    
    return {
        "topic": topic,
        "depth": depth,
        "notes": notes_text,
        "sections": extract_sections(notes_text),
        "tokens_used": tokens,
        "created_at": datetime.utcnow().isoformat()
    }


def extract_sections(notes: str) -> list:
    """Extract sections from notes."""
    lines = notes.split("\n")
    sections = []
    current_section = None
    
    for line in lines:
        if line.startswith("#"):
            current_section = line.replace("#", "").strip()
            sections.append({"title": current_section, "content": []})
        elif sections and line.strip():
            sections[-1]["content"].append(line.strip())
    
    return sections
