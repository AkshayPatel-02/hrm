from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import List

from models import (
    ScreeningRequest, ScreeningResponse, CandidateResult,
    Candidate, JobRole
)
from hrm_engine import HRMEngine
from llm_service import LLMService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="HRM Candidate Screening API",
    description="Explainable candidate screening with rule-based HRM",
    version="1.0.0"
)

# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and CRA defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not set in environment variables")

llm_service = LLMService(api_key=GEMINI_API_KEY, model_name=GEMINI_MODEL) if GEMINI_API_KEY else None


@app.get("/")
def root():
    return {
        "message": "HRM Candidate Screening API",
        "status": "running",
        "gemini_configured": llm_service is not None
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "gemini_api": "configured" if llm_service else "not_configured"
    }


@app.post("/api/screen", response_model=ScreeningResponse)
async def screen_candidates(request: ScreeningRequest):
    """
    Screen candidates using both LLM-only and HRM approaches
    Returns side-by-side comparison results
    """
    if not llm_service:
        raise HTTPException(
            status_code=500,
            detail="LLM service not configured. Please set GEMINI_API_KEY in .env file"
        )
    
    results = []
    
    for candidate in request.candidates:
        # LLM-only screening (baseline)
        llm_only_decision = llm_service.llm_only_screening(candidate, request.job_role)
        
        # HRM screening (structured)
        hrm_engine = HRMEngine()
        hrm_decision = hrm_engine.evaluate(candidate, request.job_role)
        
        results.append(CandidateResult(
            candidate_id=candidate.candidate_id,
            candidate_name=candidate.name,
            llm_only=llm_only_decision,
            hrm_decision=hrm_decision
        ))
    
    return ScreeningResponse(results=results)


@app.post("/api/parse-job-role", response_model=JobRole)
async def parse_job_role(job_text: str):
    """Parse job description text into structured format"""
    if not llm_service:
        raise HTTPException(
            status_code=500,
            detail="LLM service not configured"
        )
    
    return llm_service.parse_job_role(job_text)


@app.post("/api/parse-candidate", response_model=Candidate)
async def parse_candidate(candidate_text: str, candidate_id: str):
    """Parse candidate profile text into structured format"""
    if not llm_service:
        raise HTTPException(
            status_code=500,
            detail="LLM service not configured"
        )
    
    return llm_service.parse_candidate(candidate_text, candidate_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
