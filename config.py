"""
Simplified Configuration module for Social Media AI Agent
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # API Keys
    GOOGLE_API_KEY: Optional[str] = os.getenv('GOOGLE_API_KEY')
    GOOGLE_CLOUD_PROJECT: Optional[str] = os.getenv('GOOGLE_CLOUD_PROJECT')
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY: Optional[str] = os.getenv('ANTHROPIC_API_KEY')
    
    # Model Configuration
    DEFAULT_MODEL: str = "gemini-1.5-flash"  # Free model
    FALLBACK_MODEL: str = "gemini-1.5-flash"
    
    # Agent Configuration
    MAX_TOKENS: int = 8192
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.9
    
    # Platform Configuration
    SUPPORTED_PLATFORMS = [
        "Instagram",
        "Twitter/X", 
        "LinkedIn",
        "Facebook",
        "TikTok",
        "YouTube",
        "General"
    ]
    
    TONE_OPTIONS = [
        "Professional",
        "Casual",
        "Inspiring",
        "Educational",
        "Humorous",
        "Urgent",
        "Friendly"
    ]
    
    # Streamlit Configuration
    PAGE_TITLE: str = "Social Media AI Agent"
    PAGE_ICON: str = "🚀"
    LAYOUT: str = "wide"
    
    # UI Configuration
    THEME_COLORS = {
        "primary": "#667eea",
        "secondary": "#764ba2",
        "background": "#f8f9fa",
        "text": "#333333",
        "success": "#28a745",
        "error": "#dc3545",
        "warning": "#ffc107"
    }
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """Validate configuration and return status"""
        validation_results = {
            "google_api_key": bool(cls.GOOGLE_API_KEY),
            "model_config": bool(cls.DEFAULT_MODEL),
            "platforms": len(cls.SUPPORTED_PLATFORMS) > 0,
            "tones": len(cls.TONE_OPTIONS) > 0
        }
        
        return validation_results
    
    @classmethod
    def get_missing_config(cls) -> list:
        """Get list of missing configuration items"""
        missing = []
        
        if not cls.GOOGLE_API_KEY:
            missing.append("GOOGLE_API_KEY")
            
        return missing