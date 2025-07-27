from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
import os
from dotenv import load_dotenv
import asyncio
import concurrent.futures
import logging

# Load environment variables from .env file
load_dotenv()

from repo_cloner import clone_repo
from tree_parser import parse_repo
from api_handlers import (
    run_architecture_analysis,
    run_mind_map_analysis,
    run_code_quality_analysis,
    run_security_analysis,
    run_performance_analysis
)
from config import validate_api_keys, get_api_key, GEMINI_APIS, DEFAULT_API_KEY
from uuid import uuid4
import subprocess
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory job store
jobs = {}

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    repo_url: str

class SummarizeRequest(BaseModel):
    repo_url: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "RepoAnalyzer-Pro is running"}

@app.get("/api-status")
async def api_status():
    """Check API key configuration status"""
    try:
        has_keys = validate_api_keys()
        key_status = {}
        
        # Check individual API keys
        for analysis_type, api_key in GEMINI_APIS.items():
            key_status[analysis_type] = {
                "configured": bool(api_key),
                "key_preview": f"{api_key[:8]}..." if api_key else "Not set"
            }
        
        # Check default API key
        key_status["default"] = {
            "configured": bool(DEFAULT_API_KEY),
            "key_preview": f"{DEFAULT_API_KEY[:8]}..." if DEFAULT_API_KEY else "Not set"
        }
        
        return {
            "status": "configured" if has_keys else "not_configured",
            "message": "API keys are configured" if has_keys else "No API keys found. Please configure your .env file.",
            "keys": key_status,
            "recommendation": "Configure API keys in .env file" if not has_keys else "Ready to analyze repositories"
        }
    except Exception as e:
        logger.error(f"Error checking API status: {e}")
        return {
            "status": "error",
            "message": f"Error checking API configuration: {str(e)}",
            "keys": {},
            "recommendation": "Check your configuration and try again"
        }

@app.post("/analyze")
async def analyze_repo(request: AnalyzeRequest) -> Any:
    try:
        repo_path = clone_repo(request.repo_url)
        file_tree, file_contents, readme = parse_repo(repo_path)
        result = analyze_with_gemini(file_tree, file_contents, readme)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize-repo")
async def summarize_repo(request: SummarizeRequest, background_tasks: BackgroundTasks):
    # Check if API keys are configured
    if not validate_api_keys():
        raise HTTPException(
            status_code=400, 
            detail="API keys not configured. Please set up your Gemini API keys in the .env file. See /api-status for details."
        )
    
    job_id = str(uuid4())
    jobs[job_id] = {
        "status": "queued", 
        "progress": 0, 
        "results": {
            "architecture_flow": None,
            "mind_map": None,
            "code_quality": None,
            "security": None,
            "performance": None
        },
        "error": None
    }
    background_tasks.add_task(process_repo_job_multi_api, job_id, request.repo_url)
    return {"job_id": job_id, "status": "queued"}

@app.get("/summary-status")
async def summary_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": job["status"], "progress": job["progress"], "error": job["error"]}

@app.get("/get-summary")
async def get_summary(job_id: str, analysis_type: str = None):
    job = jobs.get(job_id)
    if not job or job["status"] != "done":
        raise HTTPException(status_code=404, detail="Summary not available")
    
    if analysis_type:
        if analysis_type in job["results"]:
            return {"summary": job["results"][analysis_type]}
        else:
            raise HTTPException(status_code=404, detail="Analysis type not found")
    
    return {"summary": job["results"]}

def process_repo_job_multi_api(job_id, repo_url):
    """Process repository analysis with multiple specialized APIs"""
    try:
        logger.info(f"🚀 Starting analysis for job {job_id}")
        jobs[job_id]["status"] = "cloning"
        jobs[job_id]["progress"] = 10
        
        # Clone repository
        repo_path = clone_repo(repo_url)
        logger.info(f"✅ Repository cloned successfully")
        
        # Parse repository
        jobs[job_id]["status"] = "parsing"
        jobs[job_id]["progress"] = 20
        file_tree, file_contents, readme = parse_repo(repo_path)
        logger.info(f"✅ Repository parsed successfully")
        
        # Run multiple specialized analyses in parallel
        jobs[job_id]["status"] = "analyzing"
        jobs[job_id]["progress"] = 30
        
        logger.info(f"🔄 Starting parallel AI analysis...")
        
        # Run all analyses in parallel with proper error handling
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(run_architecture_analysis, file_tree, file_contents, readme): "architecture_flow",
                executor.submit(run_mind_map_analysis, file_tree, file_contents, readme): "mind_map",
                executor.submit(run_code_quality_analysis, file_tree, file_contents, readme): "code_quality",
                executor.submit(run_security_analysis, file_tree, file_contents, readme): "security",
                executor.submit(run_performance_analysis, file_tree, file_contents, readme): "performance"
            }
            
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                analysis_type = futures[future]
                try:
                    result = future.result()
                    jobs[job_id]["results"][analysis_type] = result
                    completed += 1
                    progress = 30 + (completed * 14)  # 30-100% progress
                    jobs[job_id]["progress"] = progress
                    logger.info(f"✅ {analysis_type} analysis completed ({completed}/5)")
                    
                except Exception as e:
                    logger.error(f"❌ {analysis_type} analysis failed: {str(e)}")
                    jobs[job_id]["results"][analysis_type] = {"error": f"Analysis failed: {str(e)}"}
                    completed += 1
                    progress = 30 + (completed * 14)
                    jobs[job_id]["progress"] = progress
        
        # Mark as complete
        jobs[job_id]["status"] = "done"
        jobs[job_id]["progress"] = 100
        logger.info(f"🎉 All analyses completed for job {job_id}")
        
    except Exception as e:
        logger.error(f"❌ Job {job_id} failed: {str(e)}")
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)

# Legacy function for backward compatibility
def analyze_with_gemini(file_tree, file_contents, readme):
    """Legacy function - now delegates to the new API handlers"""
    try:
        # Run a quick overview analysis using the architecture API
        result = run_architecture_analysis(file_tree, file_contents, readme)
        return result
    except Exception as e:
        logger.error(f"Legacy analysis failed: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 