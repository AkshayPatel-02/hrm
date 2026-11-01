import google.generativeai as genai
from typing import Dict, List, Any, Optional
from models import Candidate, JobRole, Decision, CandidateResult
from hrm_engine import HRMEngine
from llm_service import LLMService
import uuid


class ChatHandler:
    """
    Manages conversational flow for HRM candidate screening
    States: awaiting_job -> awaiting_candidates -> complete
    """

    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.sessions: Dict[str, Dict] = {}

    def create_session(self) -> str:
        """Create a new conversation session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "state": "awaiting_job",
            "job_role": None,
            "candidates": [],
            "messages": []
        }
        return session_id

    def handle_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """Handle incoming user message and return formatted response"""
        
        if session_id not in self.sessions:
            session_id = self.create_session()
        
        session = self.sessions[session_id]
        session["messages"].append({"role": "user", "content": user_message})
        
        # Route based on current state
        if session["state"] == "awaiting_job":
            return self._handle_job_description(session_id, user_message)
        
        elif session["state"] == "awaiting_candidates":
            return self._handle_candidates(session_id, user_message)
        
        else:
            return self._start_new_screening(session_id)

    def _handle_job_description(self, session_id: str, job_text: str) -> Dict[str, Any]:
        """Parse job description and ask for candidates"""
        session = self.sessions[session_id]
        
        # Parse job description using LLM
        job_role = self.llm_service.parse_job_role(job_text, f"job_{session_id[:8]}")
        session["job_role"] = job_role
        session["state"] = "awaiting_candidates"
        
        # Format confirmation message
        response_message = f"""✅ **Got it! Here's what I understood:**

📋 **Position**: {job_role.title}
🎯 **Required Skills**: {', '.join(job_role.required_skills)}
⏱️ **Minimum Experience**: {job_role.min_experience} years
🎓 **Education**: {job_role.education_required.title()}

**Now, please describe your candidates.** You can:
- Describe one candidate at a time
- Describe multiple candidates in one message
- Include: name, skills, years of experience, education, any employment gaps"""

        session["messages"].append({"role": "assistant", "content": response_message})
        
        return {
            "session_id": session_id,
            "message": response_message,
            "state": "awaiting_candidates",
            "next_action": "provide_candidates"
        }

    def _handle_candidates(self, session_id: str, candidates_text: str) -> Dict[str, Any]:
        """Parse candidates and run HRM screening"""
        session = self.sessions[session_id]
        
        # Use LLM to parse candidates from natural language
        parsed_candidates = self._parse_multiple_candidates(candidates_text, session_id)
        
        if not parsed_candidates:
            return {
                "session_id": session_id,
                "message": "❌ I couldn't parse any candidates from your input. Please describe at least one candidate with their name, skills, and experience.",
                "state": "awaiting_candidates",
                "next_action": "provide_candidates"
            }
        
        session["candidates"].extend(parsed_candidates)
        
        # Run HRM screening
        results = self._run_screening(session["job_role"], session["candidates"])
        
        # Format results with LLM help
        formatted_results = self._format_results_with_llm(results, session["job_role"])
        
        session["state"] = "complete"
        session["results"] = results
        
        response_message = f"""📊 **Screening Complete!**

I've evaluated **{len(results)}** candidate(s) using the HRM system.
Here are the results:"""

        session["messages"].append({"role": "assistant", "content": response_message})
        
        return {
            "session_id": session_id,
            "message": response_message,
            "state": "complete",
            "results": formatted_results,
            "next_action": "show_results"
        }

    def _parse_multiple_candidates(self, candidates_text: str, session_id: str) -> List[Candidate]:
        """Use LLM to parse one or more candidates from natural language"""
        prompt = f"""
Parse the following text into one or more candidate profiles. Extract:
- name: candidate's full name
- skills: list of skills
- experience_years: years of experience (number)
- education_level: one of (high school, associate, bachelors, masters, phd)
- certifications: list of certifications (if any)
- employment_gaps: list of gaps with months and reason_provided (true/false)

Text: {candidates_text}

Return as a JSON array of candidates, even if there's only one candidate.
Example: [{{"name": "John", "skills": ["Python"], "experience_years": 3, "education_level": "bachelors", "certifications": [], "employment_gaps": []}}]

Return ONLY the JSON array, no other text.
"""
        
        try:
            response = self.llm_service.model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean up response
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            import json
            candidates_data = json.loads(text)
            
            # Convert to Candidate objects
            candidates = []
            for idx, data in enumerate(candidates_data):
                from models import EmploymentGap
                
                gaps = []
                for gap in data.get("employment_gaps", []):
                    gaps.append(EmploymentGap(
                        months=gap.get("months", 0),
                        reason_provided=gap.get("reason_provided", False)
                    ))
                
                candidate = Candidate(
                    candidate_id=f"cand_{session_id[:8]}_{idx+1}",
                    name=data.get("name", f"Candidate {idx+1}"),
                    skills=data.get("skills", []),
                    experience_years=float(data.get("experience_years", 0)),
                    education_level=data.get("education_level", "bachelors"),
                    certifications=data.get("certifications", []),
                    employment_gaps=gaps
                )
                candidates.append(candidate)
            
            return candidates
        
        except Exception as e:
            print(f"Error parsing candidates: {e}")
            return []

    def _run_screening(self, job_role: JobRole, candidates: List[Candidate]) -> List[CandidateResult]:
        """Run HRM screening on all candidates"""
        results = []
        
        for candidate in candidates:
            # HRM screening
            hrm_engine = HRMEngine()
            hrm_decision = hrm_engine.evaluate(candidate, job_role)
            
            # LLM-only for comparison (optional - can remove if not needed)
            llm_only = self.llm_service.llm_only_screening(candidate, job_role)
            
            results.append(CandidateResult(
                candidate_id=candidate.candidate_id,
                candidate_name=candidate.name,
                llm_only=llm_only,
                hrm_decision=hrm_decision
            ))
        
        return results

    def _format_results_with_llm(self, results: List[CandidateResult], job_role: JobRole) -> List[Dict[str, Any]]:
        """Use LLM to format HRM reasoning traces into human-friendly explanations"""
        formatted = []
        
        for result in results:
            # Get HRM reasoning trace
            reasoning_trace = result.hrm_decision.reasoning_trace
            decision = result.hrm_decision.decision.value
            
            # Ask LLM to create a friendly explanation
            trace_text = "\n".join([
                f"- {step.layer}: {step.rule} → {step.result.value}: {step.explanation}"
                for step in reasoning_trace
            ])
            
            prompt = f"""
Based on this HRM screening decision, create a clear, conversational explanation for why this candidate was {decision.upper()}.

Candidate: {result.candidate_name}
Job: {job_role.title}
Decision: {decision}

HRM Reasoning Trace:
{trace_text}

Write a brief (2-3 sentences) explanation that:
1. States the decision clearly
2. Explains the key reasons in simple terms
3. Mentions specific rules that triggered the decision

Be conversational and human-friendly. No technical jargon.
Return ONLY the explanation text, nothing else.
"""
            
            try:
                response = self.llm_service.model.generate_content(prompt)
                friendly_explanation = response.text.strip()
            except:
                # Fallback if LLM fails
                friendly_explanation = f"{decision}: Based on HRM evaluation of {len(reasoning_trace)} criteria."
            
            formatted.append({
                "name": result.candidate_name,
                "decision": decision,
                "explanation": friendly_explanation,
                "reasoning_trace": [
                    {
                        "layer": step.layer,
                        "rule": step.rule,
                        "result": step.result.value,
                        "explanation": step.explanation
                    }
                    for step in reasoning_trace
                ]
            })
        
        return formatted

    def _start_new_screening(self, session_id: str) -> Dict[str, Any]:
        """Start a new screening session"""
        new_session_id = self.create_session()
        
        return {
            "session_id": new_session_id,
            "message": "👋 **Let's start a new screening!**\n\nPlease describe the job role you're hiring for.",
            "state": "awaiting_job",
            "next_action": "provide_job_description"
        }

    def get_welcome_message(self) -> Dict[str, Any]:
        """Get initial welcome message"""
        session_id = self.create_session()
        
        message = """👋 **Welcome to HRM Candidate Screening!**

I'll help you screen candidates using our structured HRM system with explainable decisions.

**Let's start:** Please describe the job role you're hiring for.

Example: "I need a Senior Python Developer with 3+ years experience, FastAPI skills, and a Bachelor's degree."
"""
        
        self.sessions[session_id]["messages"].append({"role": "assistant", "content": message})
        
        return {
            "session_id": session_id,
            "message": message,
            "state": "awaiting_job",
            "next_action": "provide_job_description"
        }
