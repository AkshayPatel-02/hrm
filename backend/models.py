from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum


class DecisionType(str, Enum):
    HIRE = "HIRE"
    REVIEW = "REVIEW"
    REJECT = "REJECT"


class RuleResult(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    FLAGGED = "FLAGGED"
    APPLIED = "APPLIED"


class EmploymentGap(BaseModel):
    months: int
    reason_provided: bool


class Candidate(BaseModel):
    candidate_id: str
    name: str = Field(default="")
    skills: List[str]
    experience_years: float
    education_level: str
    certifications: List[str] = Field(default_factory=list)
    employment_gaps: List[EmploymentGap] = Field(default_factory=list)


class JobRole(BaseModel):
    job_id: str
    title: str = Field(default="")
    required_skills: List[str]
    preferred_skills: List[str] = Field(default_factory=list)
    min_experience: float
    education_required: str


class ReasoningStep(BaseModel):
    layer: str
    rule: str
    result: RuleResult
    explanation: str


class Decision(BaseModel):
    decision: DecisionType
    reasoning_trace: List[ReasoningStep]


class LLMOnlyDecision(BaseModel):
    decision: DecisionType
    explanation: str


class CandidateResult(BaseModel):
    candidate_id: str
    candidate_name: str
    llm_only: LLMOnlyDecision
    hrm_decision: Decision


class ScreeningRequest(BaseModel):
    job_role: JobRole
    candidates: List[Candidate]


class ScreeningResponse(BaseModel):
    results: List[CandidateResult]
