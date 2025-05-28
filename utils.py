"""
Simplified Utility functions for Social Media AI Agent
"""

import json
import re
import streamlit as st
from datetime import datetime
from typing import Dict, List, Tuple, Any
import hashlib

def validate_input(topic: str, platform: str, tone: str) -> Tuple[bool, str]:
    """
    Validate user input for content generation
    
    Args:
        topic: The content topic
        platform: Selected platform
        tone: Selected tone
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not topic or not topic.strip():
        return False, "Topic cannot be empty"
    
    if len(topic.strip()) < 3:
        return False, "Topic must be at least 3 characters long"
    
    if len(topic.strip()) > 500:
        return False, "Topic must be less than 500 characters"
    
    valid_platforms = ["Instagram", "Twitter/X", "LinkedIn", "Facebook", "TikTok", "YouTube", "General"]
    if platform not in valid_platforms:
        return False, "Invalid platform selected"
    
    valid_tones = ["Professional", "Casual", "Inspiring", "Educational", "Humorous", "Urgent", "Friendly"]
    if tone not in valid_tones:
        return False, "Invalid tone selected"
    
    return True, ""

def clean_text(text: str) -> str:
    """
    Clean and normalize text input
    
    Args:
        text: Raw text input
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-.,!?@#$%&*()+=\[\]{}:;"\'<>/\\|`~]', '', text)
    
    return text

def format_hashtags(hashtags: str) -> List[str]:
    """
    Format and validate hashtags
    
    Args:
        hashtags: Raw hashtag string
        
    Returns:
        List of formatted hashtags
    """
    if not hashtags:
        return []
    
    # Extract hashtags using regex
    hashtag_pattern = r'#\w+'
    found_hashtags = re.findall(hashtag_pattern, hashtags)
    
    # Clean and format
    formatted = []
    for tag in found_hashtags:
        # Remove # if present, clean, and add back
        clean_tag = re.sub(r'[^a-zA-Z0-9_]', '', tag.replace('#', ''))
        if clean_tag and len(clean_tag) > 1:
            formatted.append(f"#{clean_tag}")
    
    return list(set(formatted))  # Remove duplicates

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)].strip() + suffix

def generate_content_id(topic: str, platform: str, timestamp: datetime = None) -> str:
    """
    Generate unique content ID
    
    Args:
        topic: Content topic
        platform: Platform name
        timestamp: Optional timestamp
        
    Returns:
        Unique content ID
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    content_string = f"{topic}_{platform}_{timestamp.isoformat()}"
    return hashlib.md5(content_string.encode()).hexdigest()[:12]

def format_timestamp(timestamp: str) -> str:
    """
    Format timestamp for display
    
    Args:
        timestamp: ISO format timestamp
        
    Returns:
        Formatted timestamp string
    """
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp

def export_content_json(content_data: Dict[str, Any]) -> str:
    """
    Export content data as formatted JSON
    
    Args:
        content_data: Content data dictionary
        
    Returns:
        Formatted JSON string
    """
    try:
        return json.dumps(content_data, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error exporting content: {str(e)}")
        return "{}"

def parse_agent_response(response: str) -> Dict[str, str]:
    """
    Parse agent response into structured sections
    
    Args:
        response: Raw agent response
        
    Returns:
        Dictionary with parsed sections
    """
    sections = {
        "summary": "",
        "content": "",
        "hashtags": "",
        "visual_concepts": "",
        "analytics": "",
        "trends": ""
    }
    
    # Split response by lines
    lines = response.split('\n')
    current_section = "summary"
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Check for section headers (more comprehensive)
        line_lower = line.lower()
        
        if any(header in line_lower for header in ["📊 content package", "content package summary", "## 📊"]):
            current_section = "summary"
            continue
        elif any(header in line_lower for header in ["📝 content", "## 📝", "post content"]):
            current_section = "content"
            continue
        elif any(header in line_lower for header in ["🏷️ hashtag", "hashtag strategy", "## 🏷️"]):
            current_section = "hashtags"
            continue
        elif any(header in line_lower for header in ["🎨 visual", "visual concept", "## 🎨"]):
            current_section = "visual_concepts"
            continue
        elif any(header in line_lower for header in ["📈 performance", "analytics", "insights", "## 📈"]):
            current_section = "analytics"
            continue
        elif any(header in line_lower for header in ["🔥 trend", "trending element", "## 🔥"]):
            current_section = "trends"
            continue
        else:
            # Add content to current section, skip section headers
            if not line.startswith('##') and not line.startswith('**') or current_section == "content":
                # For content section, include everything except clear headers
                if current_section == "content" and line.startswith('##'):
                    continue
                sections[current_section] += line + "\n"
    
    # Clean up sections
    for key in sections:
        sections[key] = sections[key].strip()
        
        # Special cleaning for content section
        if key == "content" and sections[key]:
            # Remove any remaining headers that slipped through
            content_lines = []
            for line in sections[key].split('\n'):
                line = line.strip()
                if not line.startswith('##') and not (line.startswith('**') and line.endswith('**') and len(line.split()) <= 3):
                    content_lines.append(line)
            sections[key] = '\n'.join(content_lines).strip()
    
    return sections

def create_metrics_display(metrics: Dict[str, Any]) -> None:
    """
    Create metrics display in Streamlit
    
    Args:
        metrics: Dictionary of metrics to display
    """
    if not metrics:
        return
    
    cols = st.columns(len(metrics))
    
    for i, (key, value) in enumerate(metrics.items()):
        with cols[i]:
            st.metric(
                label=key.replace('_', ' ').title(),
                value=value
            )

def display_agent_status(agent_info: Dict[str, Dict[str, Any]]) -> None:
    """
    Display agent status information
    
    Args:
        agent_info: Agent information dictionary
    """
    st.markdown("### 🤖 Agent Status")
    
    for name, info in agent_info.items():
        with st.expander(f"📋 {info['name'].replace('_', ' ').title()}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Description:** {info['description']}")
                st.write(f"**Model:** {info['model']}")
            
            with col2:
                st.write(f"**Has Tools:** {'✅' if info['has_tools'] else '❌'}")
                st.write(f"**Has Sub-agents:** {'✅' if info['has_sub_agents'] else '❌'}")

def create_download_filename(topic: str, platform: str, file_type: str = "json") -> str:
    """
    Create a safe filename for downloads
    
    Args:
        topic: Content topic
        platform: Platform name
        file_type: File extension
        
    Returns:
        Safe filename
    """
    # Clean topic for filename
    safe_topic = re.sub(r'[^\w\s-]', '', topic).strip()
    safe_topic = re.sub(r'[-\s]+', '-', safe_topic)[:30]
    
    # Clean platform name
    safe_platform = platform.replace('/', '_').lower()
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return f"social_media_{safe_topic}_{safe_platform}_{timestamp}.{file_type}"

def get_platform_limits(platform: str) -> Dict[str, int]:
    """
    Get character limits for different platforms
    
    Args:
        platform: Platform name
        
    Returns:
        Dictionary with character limits
    """
    limits = {
        "Instagram": {
            "caption": 2200,
            "bio": 150,
            "hashtags": 30
        },
        "Twitter/X": {
            "post": 280,
            "bio": 160,
            "hashtags": 2
        },
        "LinkedIn": {
            "post": 3000,
            "headline": 220,
            "hashtags": 5
        },
        "Facebook": {
            "post": 63206,
            "bio": 101,
            "hashtags": 30
        },
        "TikTok": {
            "caption": 2200,
            "bio": 80,
            "hashtags": 5
        },
        "YouTube": {
            "description": 5000,
            "title": 100,
            "hashtags": 15
        },
        "General": {
            "post": 2000,
            "bio": 150,
            "hashtags": 10
        }
    }
    
    return limits.get(platform, limits["General"])

def validate_content_length(content: str, platform: str, content_type: str = "post") -> Tuple[bool, str]:
    """
    Validate content length against platform limits
    
    Args:
        content: Content to validate
        platform: Target platform
        content_type: Type of content (post, bio, etc.)
        
    Returns:
        Tuple of (is_valid, message)
    """
    limits = get_platform_limits(platform)
    limit = limits.get(content_type, 2000)
    
    content_length = len(content)
    
    if content_length > limit:
        return False, f"Content exceeds {platform} {content_type} limit of {limit} characters ({content_length}/{limit})"
    
    return True, f"Content length OK ({content_length}/{limit} characters)"

def word_count(text: str) -> int:
    """
    Count words in text
    
    Args:
        text: Text to count
        
    Returns:
        Word count
    """
    if not text:
        return 0
    
    return len(text.split())

def character_count(text: str, include_spaces: bool = True) -> int:
    """
    Count characters in text
    
    Args:
        text: Text to count
        include_spaces: Whether to include spaces
        
    Returns:
        Character count
    """
    if not text:
        return 0
    
    if include_spaces:
        return len(text)
    else:
        return len(text.replace(' ', ''))