import google.generativeai as genai
import json
import os
from models import (
    Candidate, JobRole, LLMOnlyDecision, 
    DecisionType, EmploymentGap
)
from typing import Dict, Any


class LLMService:
    """
    LLM Service using Google Gemini API
    Responsibilities:
    1. Parse job descriptions into structured data
    2. Parse candidate profiles into structured data  
    3. Provide LLM-only baseline screening (for comparison)
    
    CRITICAL: LLM does NOT make decisions in HRM path - only parses
    """

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def parse_job_role(self, job_text: str, job_id: str = "job_001") -> JobRole:
        """Parse job description text into structured JobRole"""
        prompt = f"""
You are a job description parser. Extract the following information from the job description:
- title: job title
- required_skills: list of mandatory skills
- preferred_skills: list of preferred/nice-to-have skills  
- min_experience: minimum years of experience required (as a number)
- education_required: minimum education level (one of: high school, associate, bachelors, masters, phd)

Job Description:
{job_text}

Return ONLY valid JSON with these exact keys: title, required_skills, preferred_skills, min_experience, education_required
"""
        
        response = self.model.generate_content(prompt)
        try:
            # Extract JSON from response
            text = response.text.strip()
            # Remove markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            data = json.loads(text)
            
            return JobRole(
                job_id=job_id,
                title=data.get("title", ""),
                required_skills=data.get("required_skills", []),
                preferred_skills=data.get("preferred_skills", []),
                min_experience=float(data.get("min_experience", 0)),
                education_required=data.get("education_required", "bachelors")
            )
        except Exception as e:
            print(f"Error parsing job role: {e}")
            # Return a default structure
            return JobRole(
                job_id=job_id,
                title="Unknown",
                required_skills=[],
                preferred_skills=[],
                min_experience=0,
                education_required="bachelors"
            )

    def parse_candidate(self, candidate_text: str, candidate_id: str) -> Candidate:
        """Parse candidate profile text into structured Candidate"""
        prompt = f"""
You are a candidate profile parser. Extract the following information:
- name: candidate's full name
- skills: list of skills mentioned
- experience_years: total years of experience (as a number)
- education_level: highest education (one of: high school, associate, bachelors, masters, phd)
- certifications: list of certifications
- employment_gaps: list of gaps, each with months (number) and reason_provided (true/false)

Candidate Profile:
{candidate_text}

Return ONLY valid JSON with these exact keys: name, skills, experience_years, education_level, certifications, employment_gaps
"""
        
        response = self.model.generate_content(prompt)
        try:
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            data = json.loads(text)
            
            # Parse employment gaps
            gaps = []
            for gap in data.get("employment_gaps", []):
                gaps.append(EmploymentGap(
                    months=gap.get("months", 0),
                    reason_provided=gap.get("reason_provided", False)
                ))
            
            return Candidate(
                candidate_id=candidate_id,
                name=data.get("name", "Unknown"),
                skills=data.get("skills", []),
                experience_years=float(data.get("experience_years", 0)),
                education_level=data.get("education_level", "bachelors"),
                certifications=data.get("certifications", []),
                employment_gaps=gaps
            )
        except Exception as e:
            print(f"Error parsing candidate: {e}")
            return Candidate(
                candidate_id=candidate_id,
                name="Unknown",
                skills=[],
                experience_years=0,
                education_level="bachelors",
                certifications=[],
                employment_gaps=[]
            )

    def llm_only_screening(self, candidate: Candidate, job_role: JobRole) -> LLMOnlyDecision:
        """
        LLM-only baseline screening for comparison
        This demonstrates the INCONSISTENT, OPAQUE nature of pure LLM decisions
        """
        prompt = f"""
You are a hiring manager. Review this candidate for the job role and make a hiring decision.

Job Role: {job_role.title}
Required Skills: {', '.join(job_role.required_skills)}
Minimum Experience: {job_role.min_experience} years
Education Required: {job_role.education_required}

Candidate: {candidate.name}
Skills: {', '.join(candidate.skills)}
Experience: {candidate.experience_years} years
Education: {candidate.education_level}
Certifications: {', '.join(candidate.certifications) if candidate.certifications else 'None'}

Make a decision: HIRE, REVIEW, or REJECT
Provide a brief explanation of your reasoning.

Return ONLY valid JSON with keys: decision (HIRE/REVIEW/REJECT), explanation (string)
"""
        
        response = self.model.generate_content(prompt)
        try:
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            data = json.loads(text)
            
            decision_str = data.get("decision", "REVIEW").upper()
            if decision_str not in ["HIRE", "REVIEW", "REJECT"]:
                decision_str = "REVIEW"
            
            return LLMOnlyDecision(
                decision=DecisionType[decision_str],
                explanation=data.get("explanation", "No explanation provided")
            )
        except Exception as e:
            print(f"Error in LLM screening: {e}")
            return LLMOnlyDecision(
                decision=DecisionType.REVIEW,
                explanation="Error in LLM processing"
            )
