"""
RepoAnalyzer-Pro API Handlers
============================

Specialized AI analysis functions for repository analysis using multiple Gemini APIs.
Each analysis type uses dedicated API keys for optimal performance and reliability.

Created with ❤️ by Vishesh Sanghvi
Website: http://visheshsanghvi.me/
GitHub: https://github.com/visheshsanghvi112

Analysis Types:
- Architecture Flow Analysis
- Mind Map Generation  
- Security Analysis
- Code Quality Assessment
- Performance Insights
"""

import google.generativeai as genai
import json
import logging
import time
from typing import Dict, Any, Optional
import asyncio
import concurrent.futures
from config import get_api_key, validate_api_keys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIAnalyzer:
    def __init__(self):
        self.max_retries = 2  # Reduced retries to avoid quota issues
        self.retry_delay = 1  # Reduced delay
    
    def analyze_with_retry(self, analysis_type: str, prompt: str) -> Dict[str, Any]:
        """Analyze with retry logic and proper error handling"""
        api_key = get_api_key(analysis_type)
        if not api_key:
            logger.error(f"No API key found for {analysis_type}")
            return self._get_fallback_response(analysis_type, "NO_API_KEY")
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempting {analysis_type} analysis (attempt {attempt + 1})")
                result = self._call_gemini_api(prompt, api_key)
                
                if result and "error" not in result:
                    logger.info(f"✅ {analysis_type} analysis completed successfully")
                    return result
                else:
                    error_msg = result.get("error", "Unknown error") if result else "No response"
                    logger.warning(f"⚠️ {analysis_type} analysis returned error: {error_msg}")
                    
                    # Check if it's a quota error and don't retry
                    if "429" in str(error_msg) or "quota" in str(error_msg).lower():
                        logger.error(f"❌ {analysis_type} analysis failed due to quota limits - skipping retries")
                        return self._get_fallback_response(analysis_type, "QUOTA_EXCEEDED")
                    
            except Exception as e:
                logger.error(f"❌ {analysis_type} analysis failed (attempt {attempt + 1}): {str(e)}")
                
                # Check if it's a quota error and don't retry
                if "429" in str(e) or "quota" in str(e).lower():
                    logger.error(f"❌ {analysis_type} analysis failed due to quota limits - skipping retries")
                    return self._get_fallback_response(analysis_type, "QUOTA_EXCEEDED")
                
            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
        
        # If all retries failed, return a structured error response
        return self._get_fallback_response(analysis_type, "API_FAILED")
    
    def _call_gemini_api(self, prompt: str, api_key: str) -> Dict[str, Any]:
        """Make the actual API call to Gemini"""
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("models/gemini-2.5-pro")
            response = model.generate_content(prompt)
            
            # Try to extract JSON from the response
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                # Fallback: try to extract JSON substring
                import re
                match = re.search(r'\{[\s\S]*\}', response.text)
                if match:
                    try:
                        return json.loads(match.group(0))
                    except Exception as e:
                        logger.error(f"Failed to parse JSON substring: {e}")
                
                logger.error('Could not parse Gemini response as JSON')
                return {"error": "Could not parse response as JSON", "raw_response": response.text}
                
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return {"error": str(e)}
    
    def _get_fallback_response(self, analysis_type: str, error_type: str = "GENERAL") -> Dict[str, Any]:
        """Provide structured fallback responses when API fails"""
        
        if error_type == "QUOTA_EXCEEDED":
            error_message = "API quota exceeded. Please check your Gemini API billing and quota limits."
            action_message = "Upgrade your Gemini API plan or wait for quota reset"
        elif error_type == "NO_API_KEY":
            error_message = "No API key configured. Please set up your Gemini API keys in the .env file."
            action_message = "Configure API keys in .env file"
        else:
            error_message = "API analysis failed due to technical issues."
            action_message = "Check your internet connection and API key validity"
        
        fallbacks = {
            "architecture_flow": {
                "architecture_summary": f"Unable to analyze architecture: {error_message}",
                "execution_flow": [
                    {
                        "step": 1,
                        "description": "Analysis unavailable due to API issues",
                        "files_involved": ["N/A"],
                        "purpose": "Please check API configuration"
                    }
                ],
                "main_components": [
                    {
                        "name": "API Configuration",
                        "purpose": "Ensure proper API key setup",
                        "location": ".env file",
                        "dependencies": ["Valid Gemini API key"]
                    }
                ],
                "entry_points": [action_message],
                "data_flow": "Analysis unavailable - check API setup",
                "key_insights": [f"Action required: {action_message}"],
                "complexity_level": "UNKNOWN"
            },
            "mind_map": {
                "mind_map_overview": f"Unable to generate mind map: {error_message}",
                "main_categories": [
                    {
                        "category": "Setup Required",
                        "description": "API configuration needed",
                        "subcategories": [
                            {
                                "name": "API Keys",
                                "files": [".env"],
                                "purpose": "Configure Gemini API keys"
                            }
                        ],
                        "importance": "HIGH"
                    }
                ],
                "core_features": ["API Key Management"],
                "file_relationships": [
                    {
                        "from": "User",
                        "to": "API Configuration",
                        "relationship": "Setup required"
                    }
                ],
                "visual_structure": "Configure API keys to enable analysis",
                "key_insights": [f"Next step: {action_message}"]
            },
            "code_quality": {
                "quality_overview": f"Unable to analyze code quality: {error_message}",
                "quality_score": "0/10 - API configuration required",
                "strengths": ["Error handling is working correctly"],
                "areas_for_improvement": [
                    {
                        "area": "API Configuration",
                        "current_state": "API keys not configured or quota exceeded",
                        "recommendation": action_message,
                        "priority": "HIGH"
                    }
                ],
                "code_organization": "Analysis unavailable",
                "readability": "Analysis unavailable",
                "documentation_status": "Analysis unavailable",
                "testing_coverage": "Analysis unavailable",
                "maintainability": "Analysis unavailable",
                "immediate_improvements": [action_message]
            },
            "security": {
                "security_overview": f"Unable to perform security analysis: {error_message}",
                "critical_issues": [
                    {
                        "issue": "API Configuration Issue",
                        "severity": "HIGH",
                        "impact": "Security analysis unavailable",
                        "fix": action_message
                    }
                ],
                "security_strengths": ["Error handling prevents crashes"],
                "authentication_status": "Analysis unavailable",
                "data_protection": "Analysis unavailable",
                "immediate_actions": [action_message],
                "overall_risk": "UNKNOWN",
                "security_score": "0/10 - API setup required"
            },
            "performance": {
                "performance_overview": f"Unable to analyze performance: {error_message}",
                "performance_score": "0/10 - API configuration required",
                "bottlenecks": [
                    {
                        "issue": "API Configuration",
                        "impact": "Performance analysis unavailable",
                        "location": "API setup",
                        "solution": action_message
                    }
                ],
                "optimization_opportunities": [
                    {
                        "area": "API Setup",
                        "potential_gain": "Enable all analysis features",
                        "effort": "LOW",
                        "recommendation": action_message
                    }
                ],
                "scalability": "Analysis unavailable",
                "resource_efficiency": "Analysis unavailable",
                "caching_strategies": "Analysis unavailable",
                "database_performance": "Analysis unavailable",
                "monitoring_suggestions": [action_message],
                "quick_wins": [action_message]
            }
        }
        
        return fallbacks.get(analysis_type, {"error": f"Unknown analysis type: {analysis_type}"})

# Create global analyzer instance
api_analyzer = APIAnalyzer()

def run_architecture_analysis(file_tree: str, file_contents: str, readme: str) -> Dict[str, Any]:
    """Analyze architecture and execution flow with robust error handling"""
    prompt = f"""
    Analyze the architecture and execution flow of this repository. Provide a CLEAN, EASY-TO-UNDERSTAND explanation.
    
    Focus on:
    1. How the application starts and runs
    2. Main components and their relationships
    3. Data flow between different parts
    4. Entry points and key functions
    5. Dependencies and external integrations
    
    File Tree: {file_tree}
    Key Files: {str(file_contents)[:3000]}
    README: {readme or "(none)"}
    
    Return a CLEAN, STRUCTURED JSON response:
    {{
        "architecture_summary": "Brief overview of how the system works",
        "execution_flow": [
            {{
                "step": "Step number",
                "description": "What happens in this step",
                "files_involved": ["relevant files"],
                "purpose": "Why this step is important"
            }}
        ],
        "main_components": [
            {{
                "name": "Component name",
                "purpose": "What it does",
                "location": "Where it's located",
                "dependencies": ["what it depends on"]
            }}
        ],
        "entry_points": ["How to start/run the application"],
        "data_flow": "How data moves through the system",
        "key_insights": ["Important architectural observations"],
        "complexity_level": "SIMPLE/MODERATE/COMPLEX"
    }}
    
    IMPORTANT: Make this EASY TO UNDERSTAND for developers. Focus on clarity, not technical jargon.
    """
    
    return api_analyzer.analyze_with_retry("architecture_flow", prompt)

def run_mind_map_analysis(file_tree: str, file_contents: str, readme: str) -> Dict[str, Any]:
    """Generate a visual mind map structure with robust error handling"""
    prompt = f"""
    Create a visual mind map structure of this repository. Provide a CLEAN, ORGANIZED breakdown.
    
    Focus on:
    1. Main categories and subcategories
    2. File relationships and hierarchies
    3. Functional groupings
    4. Core features and modules
    5. Visual organization structure
    
    File Tree: {file_tree}
    Key Files: {str(file_contents)[:3000]}
    README: {readme or "(none)"}
    
    Return a CLEAN, STRUCTURED JSON response:
    {{
        "mind_map_overview": "Brief description of the repository structure",
        "main_categories": [
            {{
                "category": "Category name",
                "description": "What this category contains",
                "subcategories": [
                    {{
                        "name": "Subcategory name",
                        "files": ["list of files"],
                        "purpose": "What these files do"
                    }}
                ],
                "importance": "HIGH/MEDIUM/LOW"
            }}
        ],
        "core_features": ["Main features of the application"],
        "file_relationships": [
            {{
                "from": "Source file/component",
                "to": "Target file/component",
                "relationship": "How they're connected"
            }}
        ],
        "visual_structure": "How to visualize this repository",
        "key_insights": ["Important structural observations"]
    }}
    
    IMPORTANT: Make this VISUAL and EASY TO UNDERSTAND. Focus on clear organization.
    """
    
    return api_analyzer.analyze_with_retry("mind_map", prompt)

def run_code_quality_analysis(file_tree: str, file_contents: str, readme: str) -> Dict[str, Any]:
    """Analyze code quality and best practices with robust error handling"""
    prompt = f"""
    Analyze the code quality and best practices of this repository. Provide CLEAN, ACTIONABLE feedback.
    
    Focus on:
    1. Code organization and structure
    2. Naming conventions and readability
    3. Error handling and robustness
    4. Documentation quality
    5. Testing coverage and practices
    6. Maintainability and scalability
    
    File Tree: {file_tree}
    Key Files: {str(file_contents)[:3000]}
    README: {readme or "(none)"}
    
    Return a CLEAN, STRUCTURED JSON response:
    {{
        "quality_overview": "Brief summary of overall code quality",
        "quality_score": "1-10 rating with explanation",
        "strengths": ["What's done well"],
        "areas_for_improvement": [
            {{
                "area": "Area to improve",
                "current_state": "What's happening now",
                "recommendation": "How to improve it",
                "priority": "HIGH/MEDIUM/LOW"
            }}
        ],
        "code_organization": "How well the code is structured",
        "readability": "How easy the code is to understand",
        "documentation_status": "Quality of documentation",
        "testing_coverage": "How well the code is tested",
        "maintainability": "How easy it is to maintain",
        "immediate_improvements": ["Top 3 quick wins"]
    }}
    
    IMPORTANT: Make this PRACTICAL and ACTIONABLE. Focus on specific improvements, not just criticism.
    """
    
    return api_analyzer.analyze_with_retry("code_quality", prompt)

def run_security_analysis(file_tree: str, file_contents: str, readme: str) -> Dict[str, Any]:
    """Analyze security aspects with robust error handling"""
    prompt = f"""
    Perform a security analysis of this repository and provide a CLEAN, USER-FRIENDLY summary.
    
    Focus on:
    1. CRITICAL vulnerabilities that need immediate attention
    2. Security best practices being followed
    3. Authentication and authorization mechanisms
    4. Data handling and privacy concerns
    5. Dependencies with known security issues
    
    File Tree: {file_tree}
    Key Files: {str(file_contents)[:3000]}
    README: {readme or "(none)"}
    
    Return a CLEAN, STRUCTURED JSON response:
    {{
        "security_overview": "Brief summary of overall security posture",
        "critical_issues": [
            {{
                "issue": "Description of the vulnerability",
                "severity": "HIGH/MEDIUM/LOW",
                "impact": "What could happen",
                "fix": "How to resolve it"
            }}
        ],
        "security_strengths": ["Good security practices found"],
        "authentication_status": "How authentication is handled",
        "data_protection": "How sensitive data is protected",
        "immediate_actions": ["Top 3 things to fix immediately"],
        "overall_risk": "LOW/MEDIUM/HIGH/CRITICAL",
        "security_score": "1-10 rating with explanation"
    }}
    
    IMPORTANT: Make the output CLEAN and EASY TO READ. Focus on actionable insights, not technical jargon.
    """
    
    return api_analyzer.analyze_with_retry("security", prompt)

def run_performance_analysis(file_tree: str, file_contents: str, readme: str) -> Dict[str, Any]:
    """Analyze performance characteristics with robust error handling"""
    prompt = f"""
    Analyze the performance characteristics of this repository. Provide CLEAN, PRACTICAL insights.
    
    Focus on:
    1. Performance bottlenecks and slow areas
    2. Optimization opportunities
    3. Scalability considerations
    4. Resource usage patterns
    5. Caching and efficiency strategies
    6. Database and query optimization
    
    File Tree: {file_tree}
    Key Files: {str(file_contents)[:3000]}
    README: {readme or "(none)"}
    
    Return a CLEAN, STRUCTURED JSON response:
    {{
        "performance_overview": "Brief summary of performance characteristics",
        "performance_score": "1-10 rating with explanation",
        "bottlenecks": [
            {{
                "issue": "Performance problem",
                "impact": "How it affects performance",
                "location": "Where it occurs",
                "solution": "How to fix it"
            }}
        ],
        "optimization_opportunities": [
            {{
                "area": "Area to optimize",
                "potential_gain": "Expected improvement",
                "effort": "LOW/MEDIUM/HIGH",
                "recommendation": "How to optimize"
            }}
        ],
        "scalability": "How well it handles growth",
        "resource_efficiency": "How efficiently resources are used",
        "caching_strategies": "Current and recommended caching",
        "database_performance": "Database optimization opportunities",
        "monitoring_suggestions": ["What to monitor for performance"],
        "quick_wins": ["Easy performance improvements"]
    }}
    
    IMPORTANT: Make this PRACTICAL and MEASURABLE. Focus on specific improvements with clear benefits.
    """
    
    return api_analyzer.analyze_with_retry("performance", prompt) 