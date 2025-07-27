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

@app.post("/analyze")
async def analyze_repo(request: AnalyzeRequest) -> Any:
    try:
        repo_path = clone_repo(request.repo_url)
        file_tree, file_contents, readme = parse_repo(repo_path)
        result = analyze_with_gemini(file_tree, file_contents, readme)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SummarizeRequest(BaseModel):
    repo_url: str

@app.post("/summarize-repo")
async def summarize_repo(request: SummarizeRequest, background_tasks: BackgroundTasks):
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