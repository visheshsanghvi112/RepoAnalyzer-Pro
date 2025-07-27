"""
RepoAnalyzer-Pro Configuration
=============================

Secure API key management and configuration for the RepoAnalyzer-Pro tool.
Handles environment-based API key loading with fallback mechanisms.

Created with ❤️ by Vishesh Sanghvi
Website: http://visheshsanghvi.me/
GitHub: https://github.com/visheshsanghvi112

Features:
- Environment-based API key loading
- Multiple API key support for different analysis types
- Fallback to single API key if multiple keys not provided
- API key validation and status checking
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Keys - Load from environment variables
GEMINI_APIS = {
    "architecture_flow": os.getenv("GEMINI_API_KEY_ARCHITECTURE", ""),
    "mind_map": os.getenv("GEMINI_API_KEY_MINDMAP", ""),
    "code_quality": os.getenv("GEMINI_API_KEY_QUALITY", ""),
    "security": os.getenv("GEMINI_API_KEY_SECURITY", ""),
    "performance": os.getenv("GEMINI_API_KEY_PERFORMANCE", "")
}

# Fallback to single API key if individual keys are not set
DEFAULT_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Validate API keys
def validate_api_keys():
    """Validate that at least one API key is available"""
    if DEFAULT_API_KEY:
        return True
    
    for key_name, api_key in GEMINI_APIS.items():
        if api_key:
            return True
    
    return False

# Get API key for specific analysis type
def get_api_key(analysis_type: str) -> str:
    """Get API key for specific analysis type with fallback"""
    # Try to get specific API key
    api_key = GEMINI_APIS.get(analysis_type, "")
    if api_key:
        return api_key
    
    # Fallback to default API key
    if DEFAULT_API_KEY:
        return DEFAULT_API_KEY
    
    # If no keys available, return empty string (will be handled by error handling)
    return "" 