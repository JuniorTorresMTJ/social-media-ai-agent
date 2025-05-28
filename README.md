# 🚀 Social Media AI Agent - Streamlit Application

A powerful social media content creation system built with Google Gemini API and Streamlit. This application uses AI-powered agents to create comprehensive social media content packages including engaging posts, trending hashtags, visual concepts, and performance insights.

## ✨ Features

- **Multi-Agent System**: Specialized agents for different aspects of social media content creation
- **Platform Optimization**: Content tailored for Instagram, Twitter/X, LinkedIn, Facebook, TikTok, and YouTube
- **Google Gemini Integration**: Real AI content generation using Google's latest language models
- **Dynamic Content**: Unique, contextual content generated for each request
- **Modern UI**: Clean, responsive Streamlit interface with custom styling
- **Export Options**: Download generated content as JSON files
- **Content History**: Track and revisit previously generated content

## 🤖 Agent Architecture

The system consists of five specialized agents powered by Google Gemini:

1. **🔍 Trend Finder Agent**: Discovers trending hashtags and current topics (Gemini 1.5 Flash)
2. **✍️ Content Writer Agent**: Creates engaging, platform-optimized posts (Gemini 1.5 Flash)
3. **🎨 Visual Concept Agent**: Suggests creative visual ideas and concepts (Gemini 1.5 Flash)
4. **📊 Analytics Agent**: Provides performance insights and optimization tips (Gemini 1.5 Flash)
5. **🎯 Coordinator Agent**: Orchestrates all agents to deliver comprehensive content packages (Gemini 1.5 Pro)

## 🚀 Quick Start

### Method 1: Simple Start (Recommended)

1. **Download/Clone the project**
   ```bash
   # Download all files to a folder
   # Make sure you have: app.py, config.py, agents.py, utils.py, requirements.txt
   ```

2. **Get your Google Gemini API key**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy the key

3. **Run the start script**
   ```bash
   python start.py
   ```
   
   This will:
   - Check all requirements
   - Install missing packages
   - Run setup tests
   - Start the application

### Method 2: Manual Setup

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create .env file**
   ```bash
   cp .env.example .env
   ```
   
   Add your Gemini API key:
   ```bash
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

3. **Test the setup (optional)**
   ```bash
   python test_setup.py
   ```

4. **Start the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - Go to http://localhost:8501

## 🔧 Configuration

### Google Gemini API Setup

1. **Get API Key**:
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key" 
   - Copy the generated key

2. **Configure Environment**:
   ```bash
   GOOGLE_API_KEY=AIzaSy...your_api_key_here
   ```

3. **Test Connection**:
   - Use the "🔍 Test Gemini API" button in the sidebar
   - Should show ✅ if working correctly

### API Usage & Costs

- **Gemini 1.5 Flash**: ~$0.001 per content generation
- **Gemini 1.5 Pro**: ~$0.005 per coordinator request
- **Rate Limits**: 15 requests per minute (free tier)
- **Monitor Usage**: Check [Google AI Studio Console](https://aistudio.google.com/)

## 📱 How to Use

### Basic Content Generation

1. **Enter Topic**: Describe what you want to create content about
   - Example: "Sustainable fashion trends for young professionals"

2. **Select Platform**: Choose your target social media platform
   - Instagram, LinkedIn, Twitter/X, Facebook, TikTok, YouTube

3. **Choose Tone**: Select the appropriate tone for your audience
   - Professional, Casual, Inspiring, Educational, Humorous, etc.

4. **Add Context** (optional): Provide additional requirements
   - Target audience details, brand guidelines, special instructions

5. **Configure Options**: Use advanced settings for specific needs
   - Include hashtag strategy
   - Include visual concepts
   - Include analytics insights
   - Choose content length

6. **Generate**: Click "Generate Content" and wait for AI agents to work

7. **Review Results**: Explore the structured content package
   - Post content ready for publishing
   - Hashtag recommendations
   - Visual design suggestions
   - Performance optimization tips

8. **Export/Save**: Download content as JSON or copy to clipboard

### Advanced Features

- **Content History**: View and revisit previously generated content
- **Platform Validation**: Automatic checking of character limits
- **Agent Status**: Monitor the health and status of AI agents
- **API Testing**: Verify Gemini API connection
- **Regeneration**: Create multiple variations of the same topic

## 🎯 Example Usage Scenarios

### Tech Company LinkedIn Post
```
Topic: "How AI is transforming customer service"
Platform: LinkedIn
Tone: Professional
Context: "B2B audience, include statistics and case studies"
```

### Fashion Brand Instagram Post
```
Topic: "Summer fashion trends 2025"
Platform: Instagram
Tone: Inspiring
Context: "Young female audience, focus on sustainability"
```

### Local Business Facebook Post
```
Topic: "New seasonal menu items"
Platform: Facebook
Tone: Friendly
Context: "Family restaurant, highlight local ingredients"
```

## 📊 Understanding the Output

The AI generates structured content packages including:

### 📝 Post Content
- **Hook**: Attention-grabbing opening
- **Body**: Engaging main content
- **Call-to-Action**: Clear next steps
- **Platform optimization**: Format-specific styling

### 🏷️ Hashtag Strategy
- **Primary hashtags**: High-traffic, relevant tags
- **Niche hashtags**: Specific, targeted tags
- **Community hashtags**: Engagement-building tags
- **Performance rationale**: Why each tag was chosen

### 🎨 Visual Concepts
- **Style suggestions**: Photography, graphics, video concepts
- **Color palettes**: Brand-consistent color recommendations
- **Composition ideas**: Layout and visual hierarchy
- **Mood and aesthetic**: Overall visual feeling

### 📈 Performance Insights
- **Engagement predictions**: Expected likes, comments, shares
- **Optimization tips**: How to improve performance
- **Timing recommendations**: Best posting schedules
- **Audience insights**: Demographics and behavior patterns

## 🔧 Troubleshooting

### Common Issues

1. **API Errors**
   ```bash
   # Check API key in .env file
   GOOGLE_API_KEY=your_key_here
   
   # Test API connection in sidebar
   # Verify quota in Google AI Studio
   ```

2. **Installation Issues**
   ```bash
   # Update pip and reinstall
   pip install --upgrade pip
   pip install -r requirements.txt
   
   # Or use the start script
   python start.py
   ```

3. **Content Generation Fails**
   - Check internet connection
   - Verify API key permissions
   - Check API quotas and billing
   - Try different topics/prompts

4. **Streamlit Issues**
   ```bash
   # Clear cache and restart
   streamlit cache clear
   streamlit run app.py --server.port 8502
   ```

### Getting Help

1. **Run diagnostics**:
   ```bash
   python test_setup.py
   ```

2. **Check the setup**:
   ```bash
   python start.py
   ```

3. **Use built-in diagnostics**: Click "🩺 Run Diagnostics" in sidebar

## 🆚 Real AI vs Fallback Mode

### Real AI Mode (With API Key)
- ✅ **Dynamic content** - Unique for each request
- ✅ **Context-aware** - Understands your specific topic
- ✅ **Platform-optimized** - Tailored for each social platform
- ✅ **Current trends** - AI knowledge of latest trends
- 💰 **Small API costs** - ~$0.001-0.005 per generation

### Fallback Mode (No API Key)
- ⚠️ **Error messages** - Shows API connection issues
- 🔧 **Troubleshooting info** - Helps you set up the API
- 📚 **Setup instructions** - Guides you through configuration
- 🆓 **No costs** - But limited functionality

## 📁 Project Structure

```
social-media-ai-agent/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration and settings
├── agents.py             # AI agent system (Gemini integration)
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── start.py              # Easy startup script
├── test_setup.py         # Setup verification script
├── .env.example          # Environment variables template
├── .env                  # Your environment variables (create this)
└── README.md            # This file
```

## 🚀 Getting Started Checklist

- [ ] Download all project files
- [ ] Get Google Gemini API key from [AI Studio](https://aistudio.google.com/app/apikey)
- [ ] Create .env file with your API key
- [ ] Run `python start.py` OR `python test_setup.py`
- [ ] If tests pass, run `streamlit run app.py`
- [ ] Open http://localhost:8501 in your browser
- [ ] Test API connection using sidebar button
- [ ] Try generating content for different topics and platforms
- [ ] Start creating amazing social media content!

## 🎉 Success!

If everything is working correctly, you should see:

- ✅ Clean, modern web interface
- ✅ Gemini API connection working
- ✅ All 5 AI agents showing as active
- ✅ Content generation working for all platforms
- ✅ Unique, contextual content for each topic
- ✅ Structured output with hashtags, visuals, and analytics
- ✅ Download and history features working

You're now ready to create professional social media content with real AI! 🚀

---

**Built with ❤️ using Google Gemini API and Streamlit**