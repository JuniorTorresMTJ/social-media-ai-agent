"""
Social Media AI Agent - Run Script
Utility script to run the Streamlit application with proper configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import streamlit
        import google.adk
        import dotenv
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("Please copy .env.example to .env and configure your API keys")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        print("Please add your Google API key to the .env file")
        return False
    
    print("✅ Environment configuration is valid")
    return True

def run_streamlit():
    """Run the Streamlit application"""
    try:
        print("🚀 Starting Social Media AI Agent...")
        print("📱 Open your browser and go to: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main function"""
    print("=" * 60)
    print("🚀 Social Media AI Agent - Startup Check")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    print("=" * 60)
    print("✅ All checks passed! Starting application...")
    print("=" * 60)
    
    # Run the application
    run_streamlit()

if __name__ == "__main__":
    main()
