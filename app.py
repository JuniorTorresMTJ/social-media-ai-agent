import streamlit as st
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

# Import our simplified modules
try:
    from config import Config
    from agents import get_agent_manager, AgentManager
    from utils import (
        validate_input, clean_text, format_hashtags, truncate_text,
        generate_content_id, format_timestamp, export_content_json,
        parse_agent_response, create_metrics_display, display_agent_status,
        create_download_filename, get_platform_limits, validate_content_length
    )
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please make sure all required files are in the same directory as app.py")
    st.stop()

# Page configuration
config = Config()
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state="expanded"
)

class SocialMediaApp:
    """
    Main application class for Social Media AI Agent
    """
    
    def __init__(self):
        self.config = Config()
        self.agent_manager: Optional[AgentManager] = None
        self._initialize_session_state()
        
    def _initialize_session_state(self):
        """Initialize Streamlit session state"""
        if 'generated_content' not in st.session_state:
            st.session_state.generated_content = []
        
        if 'agent_manager' not in st.session_state:
            st.session_state.agent_manager = None
            
        if 'current_content' not in st.session_state:
            st.session_state.current_content = None
            
        if 'show_history' not in st.session_state:
            st.session_state.show_history = False
    
    def initialize_agents(self) -> bool:
        """Initialize the agent manager"""
        try:
            if st.session_state.agent_manager is None:
                with st.spinner("🤖 Initializing AI agents..."):
                    st.session_state.agent_manager = get_agent_manager()
                    self.agent_manager = st.session_state.agent_manager
                    return True
            else:
                self.agent_manager = st.session_state.agent_manager
                return True
        except Exception as e:
            st.error(f"Failed to initialize agents: {str(e)}")
            return False
    
    def validate_configuration(self) -> bool:
        """Validate application configuration"""
        validation = self.config.validate_config()
        missing = self.config.get_missing_config()
        
        if missing:
            st.error(f"⚠️ Missing configuration: {', '.join(missing)}")
            return False
        
        return all(validation.values())
    
    def render_sidebar(self):
        """Render the application sidebar"""
        with st.sidebar:
            st.markdown("### ⚙️ Configuration")
            
            # API Key status
            if self.config.GOOGLE_API_KEY:
                st.success("✅ Google API Key configured")
                
                # Test API connection
                if st.button("🔍 Test Gemini API"):
                    from agents import test_gemini_connection
                    
                    with st.spinner("Testing API connection..."):
                        api_status = test_gemini_connection()
                    
                    if api_status["status"] == "success":
                        st.success(f"✅ {api_status['message']}")
                        st.info(f"Model: {api_status['model']}")
                    elif api_status["status"] == "warning":
                        st.warning(f"⚠️ {api_status['message']}")
                    else:
                        st.error(f"❌ {api_status['message']}")
                        if "suggestion" in api_status:
                            st.info(f"💡 {api_status['suggestion']}")
            else:
                st.error("❌ Google API Key not found")
                st.info("Add your Google API key to the .env file")
                st.markdown("""
                **Setup Instructions:**
                1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
                2. Create a new API key
                3. Add it to your .env file as:
                   ```
                   GOOGLE_API_KEY=your_key_here
                   ```
                4. Restart the application
                """)
            
            st.markdown("---")
            
            # Agent System Info
            st.markdown("### 🤖 Agent System")
            if self.agent_manager:
                agents = self.agent_manager.list_agents()
                st.markdown("**Active Agents:**")
                for agent in agents:
                    icon = "🎯" if agent == "coordinator" else "🤖"
                    st.markdown(f"- {icon} {agent.replace('_', ' ').title()}")
                
                # Agent status
                if st.button("🔍 Check Agent Status"):
                    agent_info = self.agent_manager.get_agent_info()
                    validation = self.agent_manager.validate_agents()
                    
                    st.markdown("**Agent Validation:**")
                    for name, status in validation.items():
                        icon = "✅" if status else "❌"
                        st.markdown(f"- {icon} {name.replace('_', ' ').title()}")
                        
                        # Show API status for each agent
                        if name in agent_info and agent_info[name].get('api_available'):
                            st.markdown(f"  └ 🌐 API Ready")
                        else:
                            st.markdown(f"  └ ⚠️ API Not Available")
            else:
                st.warning("Agents not initialized")
            
            st.markdown("---")
            
            # Model Information
            st.markdown("### 🧠 AI Models")
            st.markdown("""
            **All Agents**: Gemini 1.5 Flash (Free)
            
            **Features**:
            - Real-time content generation
            - Context-aware responses
            - Platform optimization
            - Trend analysis
            - No cost for usage (within free limits)
            """)
            
            st.markdown("---")
            
            # Free tier info
            st.markdown("### 🆓 Free Tier Limits")
            st.markdown("""
            **Gemini 1.5 Flash (Free)**:
            - 15 requests per minute
            - 1,500 requests per day
            - Perfect for social media content
            
            **Tip**: Space out your generations to stay within limits
            """)
            
            st.markdown("---")
            
            # Platform limits info
            st.markdown("### 📊 Platform Limits")
            platform_info = st.selectbox(
                "View limits for:",
                self.config.SUPPORTED_PLATFORMS,
                key="platform_limits_select"
            )
            
            limits = get_platform_limits(platform_info)
            st.markdown(f"**{platform_info} Limits:**")
            for content_type, limit in limits.items():
                st.markdown(f"- {content_type.title()}: {limit:,} chars")
            
            st.markdown("---")
            
            # Tips and help
            st.markdown("### 💡 Tips")
            st.markdown("""
            **Best Practices:**
            - Be specific with your topic
            - Consider your target audience
            - Use relevant additional context
            - Choose appropriate tone and platform
            - Review generated content before posting
            
            **Trending Topics:**
            - Current events and news
            - Seasonal content
            - Industry insights
            - Behind-the-scenes content
            - User-generated content
            """)
            
            st.markdown("---")
            
            # API Usage Info
            if self.config.GOOGLE_API_KEY:
                st.markdown("### 📈 API Usage")
                st.info("""
                **Free Tier**: No charges for Gemini 1.5 Flash!
                
                **Limits**:
                - 15 requests per minute
                - 1,500 requests per day
                
                **Monitor usage**: Check Google AI Studio for usage stats
                """)
            
            st.markdown("---")
            
            st.markdown("### 🔧 Troubleshooting")
            if st.button("🩺 Run Diagnostics", use_container_width=True):
                st.markdown("**System Check:**")
                
                # Check API key
                if self.config.GOOGLE_API_KEY:
                    st.success("✅ API Key present")
                else:
                    st.error("❌ API Key missing")
                
                # Check agents
                if self.agent_manager:
                    st.success("✅ Agents initialized")
                else:
                    st.error("❌ Agents not initialized")
                
                # Check internet (basic)
                try:
                    import requests
                    response = requests.get("https://www.google.com", timeout=5)
                    if response.status_code == 200:
                        st.success("✅ Internet connection")
                    else:
                        st.warning("⚠️ Internet connection issues")
                except:
                    st.error("❌ No internet connection")
    
    def render_header(self):
        """Render the application header"""
        st.markdown('<h1 class="main-header">🚀 Social Media AI Agent</h1>', unsafe_allow_html=True)
        st.markdown("**Create engaging social media content with Google Gemini-powered multi-agent system**")
        
        # Quick stats
        if self.agent_manager:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Active Agents", len(self.agent_manager.list_agents()))
            
            with col2:
                st.metric("Supported Platforms", len(self.config.SUPPORTED_PLATFORMS))
            
            with col3:
                st.metric("Content Generated", len(st.session_state.generated_content))
            
            with col4:
                st.metric("Tone Options", len(self.config.TONE_OPTIONS))
    
    def render_content_form(self):
        """Render the content generation form"""
        st.markdown("## 📝 Content Creation")
        
        with st.form(key="content_form", clear_on_submit=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                topic = st.text_input(
                    "🎯 Topic/Subject",
                    placeholder="e.g., Sustainable fashion trends, AI in healthcare, Travel photography...",
                    help="What do you want to create content about?",
                    key="topic_input"
                )
                
                additional_context = st.text_area(
                    "📋 Additional Context (Optional)",
                    placeholder="Add any specific requirements, target audience details, brand guidelines, or special instructions...",
                    height=120,
                    help="Provide more context to help generate better content",
                    key="context_input"
                )
            
            with col2:
                platform = st.selectbox(
                    "📱 Platform",
                    self.config.SUPPORTED_PLATFORMS,
                    help="Choose the target social media platform",
                    key="platform_select"
                )
                
                tone = st.selectbox(
                    "🎵 Tone",
                    self.config.TONE_OPTIONS,
                    help="Select the tone for your content",
                    key="tone_select"
                )
                
                # Advanced options
                with st.expander("⚙️ Advanced Options"):
                    include_hashtags = st.checkbox(
                        "Include hashtag strategy",
                        value=True,
                        help="Generate comprehensive hashtag recommendations"
                    )
                    
                    include_visuals = st.checkbox(
                        "Include visual concepts",
                        value=True,
                        help="Generate visual design suggestions"
                    )
                    
                    include_analytics = st.checkbox(
                        "Include analytics insights",
                        value=True,
                        help="Provide performance predictions and optimization tips"
                    )
                    
                    content_length = st.selectbox(
                        "Content Length",
                        ["Short", "Medium", "Long"],
                        index=1,
                        help="Preferred content length"
                    )
            
            # Submit button
            submitted = st.form_submit_button(
                "🚀 Generate Content",
                type="primary",
                use_container_width=True
            )
            
            if submitted:
                return self.process_content_generation(
                    topic=topic,
                    platform=platform,
                    tone=tone,
                    additional_context=additional_context,
                    include_hashtags=include_hashtags,
                    include_visuals=include_visuals,
                    include_analytics=include_analytics,
                    content_length=content_length
                )
        
        return False
    
    def process_content_generation(self, topic: str, platform: str, tone: str, 
                                 additional_context: str, include_hashtags: bool,
                                 include_visuals: bool, include_analytics: bool,
                                 content_length: str) -> bool:
        """Process content generation request"""
        
        # Validate input
        is_valid, error_msg = validate_input(topic, platform, tone)
        if not is_valid:
            st.error(f"❌ Input validation failed: {error_msg}")
            return False
        
        # Clean input
        topic = clean_text(topic)
        additional_context = clean_text(additional_context)
        
        # Clear previous content to ensure fresh generation
        if 'current_content' in st.session_state:
            st.session_state.current_content = None
        
        # Check platform limits
        limits = get_platform_limits(platform)
        
        # Generate content
        try:
            with st.spinner("🤖 AI agents are working on your content..."):
                result = self.generate_content(
                    topic=topic,
                    platform=platform,
                    tone=tone,
                    additional_context=additional_context,
                    include_hashtags=include_hashtags,
                    include_visuals=include_visuals,
                    include_analytics=include_analytics,
                    content_length=content_length
                )
                
                if result.get("success"):
                    # Store in session state
                    content_data = {
                        "id": generate_content_id(topic, platform),
                        "topic": topic,
                        "platform": platform,
                        "tone": tone,
                        "additional_context": additional_context,
                        "content": result["content"],
                        "timestamp": result["timestamp"],
                        "options": {
                            "include_hashtags": include_hashtags,
                            "include_visuals": include_visuals,
                            "include_analytics": include_analytics,
                            "content_length": content_length
                        }
                    }
                    
                    st.session_state.generated_content.append(content_data)
                    st.session_state.current_content = content_data
                    
                    st.success("✅ Content generated successfully!")
                    return True
                else:
                    st.error(f"❌ Content generation failed: {result.get('error', 'Unknown error')}")
                    return False
                    
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            return False
    
    def generate_content(self, topic: str, platform: str, tone: str,
                        additional_context: str, include_hashtags: bool,
                        include_visuals: bool, include_analytics: bool,
                        content_length: str) -> Dict:
        """Generate content using the agent system"""
        
        if not self.agent_manager:
            return {"success": False, "error": "Agent manager not initialized"}
        
        # Build comprehensive prompt
        prompt_parts = [
            f"Create a comprehensive social media content package for:",
            f"",
            f"**Topic**: {topic}",
            f"**Platform**: {platform}",
            f"**Tone**: {tone}",
            f"**Content Length**: {content_length}",
        ]
        
        if additional_context:
            prompt_parts.append(f"**Additional Context**: {additional_context}")
        
        prompt_parts.extend([
            f"",
            f"**Requirements:**"
        ])
        
        if include_hashtags:
            prompt_parts.append("- Include comprehensive hashtag strategy")
        
        if include_visuals:
            prompt_parts.append("- Provide creative visual concept suggestions")
        
        if include_analytics:
            prompt_parts.append("- Include performance insights and optimization tips")
        
        prompt_parts.extend([
            f"",
            f"Please ensure the content is:",
            f"- Optimized for {platform}",
            f"- Written in a {tone.lower()} tone",
            f"- Engaging and ready to post",
            f"- Compliant with platform best practices",
            f"- Includes current trends and insights"
        ])
        
        prompt = "\n".join(prompt_parts)
        
        try:
            # Get coordinator agent
            coordinator = self.agent_manager.get_coordinator()
            if not coordinator:
                return {"success": False, "error": "Coordinator agent not available"}
            
            # Generate content
            response = coordinator.run(prompt)
            
            return {
                "success": True,
                "content": response,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def render_content_display(self):
        """Render the generated content display"""
        
        if not st.session_state.current_content:
            st.info("👆 Generate content using the form above to see results here.")
            return
        
        content_data = st.session_state.current_content
        
        st.markdown("## 📊 Generated Content")
        
        # Content metadata
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**📱 Platform**: {content_data['platform']}")
            st.markdown(f"**🎵 Tone**: {content_data['tone']}")
        
        with col2:
            st.markdown(f"**🎯 Topic**: {truncate_text(content_data['topic'], 50)}")
            st.markdown(f"**⏰ Generated**: {format_timestamp(content_data['timestamp'])}")
        
        with col3:
            st.markdown(f"**🆔 ID**: {content_data['id']}")
            
            # Validation status
            is_valid, validation_msg = validate_content_length(
                content_data['content'], 
                content_data['platform']
            )
            
            if is_valid:
                st.success(f"✅ {validation_msg}")
            else:
                st.warning(f"⚠️ {validation_msg}")
        
        # Main content display with tabs instead of nested expanders
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Complete Content Package")
        
        # Parse content
        parsed_content = parse_agent_response(content_data['content'])
        
        # Use tabs instead of expanders to avoid nesting issues
        tab_names = []
        tab_contents = []
        
        if parsed_content['summary']:
            tab_names.append("📊 Summary")
            tab_contents.append(parsed_content['summary'])
        
        if parsed_content['content']:
            tab_names.append("📝 Content")
            tab_contents.append(parsed_content['content'])
        
        if parsed_content['hashtags']:
            tab_names.append("🏷️ Hashtags")
            tab_contents.append(parsed_content['hashtags'])
        
        if parsed_content['visual_concepts']:
            tab_names.append("🎨 Visuals")
            tab_contents.append(parsed_content['visual_concepts'])
        
        if parsed_content['analytics']:
            tab_names.append("📈 Analytics")
            tab_contents.append(parsed_content['analytics'])
        
        if parsed_content['trends']:
            tab_names.append("🔥 Trends")
            tab_contents.append(parsed_content['trends'])
        
        # Create tabs if we have parsed content
        if tab_names:
            tabs = st.tabs(tab_names)
            
            for i, (tab, content) in enumerate(zip(tabs, tab_contents)):
                with tab:
                    st.markdown(content)
                    
                    # Add metrics for content tab
                    if i == 1 and parsed_content['content']:  # Content tab
                        word_count = len(parsed_content['content'].split())
                        char_count = len(parsed_content['content'])
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Words", word_count)
                        with col2:
                            st.metric("Characters", char_count)
                        with col3:
                            reading_time = max(1, word_count // 200)
                            st.metric("Reading Time", f"{reading_time} min")
        else:
            # Fallback: show raw content
            st.markdown("### 📄 Generated Content")
            st.markdown(content_data['content'])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download JSON
            filename = create_download_filename(
                content_data['topic'], 
                content_data['platform'], 
                "json"
            )
            
            st.download_button(
                label="📥 Download as JSON",
                data=export_content_json(content_data),
                file_name=filename,
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # Copy to clipboard - improved and simplified version
            if st.button("📋 Copy Content", use_container_width=True):
                # Extract just the content part for copying
                parsed_content = parse_agent_response(content_data['content'])
                
                # Create clean content for copying
                if parsed_content['content']:
                    copy_content = parsed_content['content']
                else:
                    # Fallback: extract content manually
                    lines = content_data['content'].split('\n')
                    content_lines = []
                    in_content_section = False
                    
                    for line in lines:
                        line = line.strip()
                        if '📝 CONTENT' in line.upper() or '## 📝' in line:
                            in_content_section = True
                            continue
                        elif line.startswith('##') and in_content_section:
                            break  # End of content section
                        elif in_content_section and line:
                            content_lines.append(line)
                    
                    copy_content = '\n'.join(content_lines).strip()
                
                # Store in session state
                st.session_state.copy_content = copy_content
                
                st.success("📋 Content ready to copy!")
                st.info("💡 The content below is selected. Use Ctrl+C to copy it:")
                
                # Display content in a text area that's easy to select and copy
                st.text_area(
                    "📄 Click in the box below and press Ctrl+A to select all, then Ctrl+C to copy:",
                    copy_content,
                    height=200,
                    help="This is the clean post content ready for social media"
                )
        
        with col3:
            # Regenerate content
            if st.button("🔄 Regenerate", use_container_width=True):
                st.session_state.current_content = None
                st.rerun()
    
    def render_history(self):
        """Render content generation history"""
        if not st.session_state.generated_content:
            st.info("No content generated yet. Create some content to see your history here!")
            return
        
        st.markdown("## 🗂️ Generation History")
        
        # History controls
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**Total Generated**: {len(st.session_state.generated_content)} items")
        
        with col2:
            if st.button("🗑️ Clear History"):
                st.session_state.generated_content = []
                st.session_state.current_content = None
                st.success("History cleared!")
                st.rerun()
        
        # Display history items in a simple list format
        st.markdown("### Recent Content")
        
        for i, content in enumerate(reversed(st.session_state.generated_content[-5:])):  # Show last 5
            # Create a card-like display for each item
            with st.container():
                st.markdown("---")
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**🎯 Topic**: {content['topic']}")
                    st.markdown(f"**📱 Platform**: {content['platform']} | **🎵 Tone**: {content['tone']}")
                    st.markdown(f"**⏰ Generated**: {format_timestamp(content['timestamp'])}")
                    
                    if content.get('additional_context'):
                        st.markdown(f"**📋 Context**: {truncate_text(content['additional_context'], 100)}")
                
                with col2:
                    if st.button(f"📖 View", key=f"view_{content['id']}", use_container_width=True):
                        st.session_state.current_content = content
                        st.rerun()
        
        # Show more button if there are more items
        if len(st.session_state.generated_content) > 5:
            if st.button(f"📜 Show All {len(st.session_state.generated_content)} Items"):
                st.markdown("### All Generated Content")
                
                for i, content in enumerate(reversed(st.session_state.generated_content)):
                    with st.container():
                        st.markdown("---")
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.markdown(f"**{i+1}.** {truncate_text(content['topic'], 60)} ({content['platform']})")
                            st.markdown(f"*{format_timestamp(content['timestamp'])}*")
                        
                        with col2:
                            if st.button(f"View", key=f"view_all_{content['id']}", use_container_width=True):
                                st.session_state.current_content = content
                                st.rerun()
    
    def run(self):
        """Run the main application"""
        
        # Custom CSS
        st.markdown("""
        <style>
            .main-header {
                font-size: 3rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 2rem;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .agent-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 15px;
                color: white;
                margin: 1rem 0;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }
            
            .result-card {
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                border-left: 4px solid #667eea;
                margin: 1rem 0;
            }
            
            .metrics-container {
                display: flex;
                justify-content: space-around;
                margin: 2rem 0;
            }
            
            .metric-item {
                text-align: center;
                padding: 1rem;
            }
            
            .stAlert > div {
                padding: 1rem;
                border-radius: 8px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Validate configuration
        if not self.validate_configuration():
            st.warning("⚠️ Please configure your Google API key in the .env file to use this application.")
            st.code('GOOGLE_API_KEY=your_api_key_here', language='bash')
            return
        
        # Initialize agents
        if not self.initialize_agents():
            st.error("Failed to initialize AI agents. Please check your configuration.")
            return
        
        # Render UI components
        self.render_sidebar()
        self.render_header()
        
        # Main content area
        content_generated = self.render_content_form()
        
        # Display generated content
        self.render_content_display()
        
        # History section - render directly without nesting in expander
        st.markdown("---")
        if st.button("🗂️ Show/Hide Generation History"):
            if 'show_history' not in st.session_state:
                st.session_state.show_history = True
            else:
                st.session_state.show_history = not st.session_state.show_history
        
        if st.session_state.get('show_history', False):
            self.render_history()
        
        # Footer
        st.markdown("---")
        st.markdown(f"""
        <div style='text-align: center; color: #666; margin-top: 2rem;'>
            <p><strong>Social Media AI Agent</strong> - Built with Google Gemini API and Streamlit</p>
            <p>Powered by {self.config.DEFAULT_MODEL} • Version 1.0.0</p>
            <p>🤖 Multi-Agent System • 📱 Platform Optimized • 🎯 Engagement Focused</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application entry point"""
    app = SocialMediaApp()
    app.run()


if __name__ == "__main__":
    main()