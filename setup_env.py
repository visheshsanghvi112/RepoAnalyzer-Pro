#!/usr/bin/env python3
"""
Setup script for RepoAnalyzer-Pro
Creates .env file with API keys

Created with ❤️ by Vishesh Sanghvi
Website: http://visheshsanghvi.me/
GitHub: https://github.com/visheshsanghvi112
"""

import os

def create_env_file():
    """Create .env file with API keys"""
    
    env_content = """# RepoAnalyzer-Pro Environment Configuration
# =========================================
#
# Created with ❤️ by Vishesh Sanghvi
# Website: http://visheshsanghvi.me/
# GitHub: https://github.com/visheshsanghvi112

# Multiple Specialized API Keys for optimal performance
GEMINI_API_KEY_ARCHITECTURE=AIzaSyDEv3121msA2VHJewPcro81mokCGGf95E4
GEMINI_API_KEY_MINDMAP=AIzaSyAh6m4JhelFmBEmROkUuXM0w4jj1roJWfg
GEMINI_API_KEY_QUALITY=AIzaSyASLMKap45M58cA4tD33qmRlxcwVbtdDHI
GEMINI_API_KEY_SECURITY=AIzaSyDdKX6TK9JXMbMWFzDJ92XemU-JbUa_KU4
GEMINI_API_KEY_PERFORMANCE=AIzaSyARDiJ0B2jIGeTm9-L4ay0mPNu3PTO1G7A

# Fallback single API key (using the first one)
GEMINI_API_KEY=AIzaSyDEv3121msA2VHJewPcro81mokCGGf95E4
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print("🔑 API keys configured for all 5 analysis types")
    print("🚀 Ready to run RepoAnalyzer-Pro!")

if __name__ == "__main__":
    create_env_file() 