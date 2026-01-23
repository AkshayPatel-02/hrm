from models import (
    Candidate, JobRole, Decision, ReasoningStep,
    DecisionType, RuleResult
)
from typing import List


class HRMEngine:
    """
    Hierarchical Reasoning Model Engine
    3-Layer Architecture:
    - Layer 1: Eligibility Gate (hard filters)
    - Layer 2: Risk & Gap Evaluation
    - Layer 3: Policy Decision
    """

    def __init__(self):
        self.reasoning_trace: List[ReasoningStep] = []

    def evaluate(self, candidate: Candidate, job_role: JobRole) -> Decision:
        """Main evaluation method that processes all layers"""
        self.reasoning_trace = []

        # Layer 1: Eligibility Gate
        eligibility_pass = self._layer1_eligibility(candidate, job_role)
        if not eligibility_pass:
            return Decision(
                decision=DecisionType.REJECT,
                reasoning_trace=self.reasoning_trace
            )

        # Layer 2: Risk & Gap Evaluation
        risk_level = self._layer2_risk_evaluation(candidate, job_role)

        # Layer 3: Policy Decision
        final_decision = self._layer3_policy_decision(risk_level)

        return Decision(
            decision=final_decision,
            reasoning_trace=self.reasoning_trace
        )

    def _layer1_eligibility(self, candidate: Candidate, job_role: JobRole) -> bool:
        """Layer 1: Hard eligibility filters"""
        
        # R1: Minimum Experience
        if candidate.experience_years < job_role.min_experience:
            self.reasoning_trace.append(ReasoningStep(
                layer="Eligibility Gate",
                rule="R1_MIN_EXPERIENCE",
                result=RuleResult.FAIL,
                explanation=f"Candidate has {candidate.experience_years} years experience (minimum required: {job_role.min_experience})"
            ))
            return False
        else:
            self.reasoning_trace.append(ReasoningStep(
                layer="Eligibility Gate",
                rule="R1_MIN_EXPERIENCE",
                result=RuleResult.PASS,
                explanation=f"Candidate has {candidate.experience_years} years experience (minimum required: {job_role.min_experience})"
            ))

        # R2: Mandatory Skills
        missing_skills = [skill for skill in job_role.required_skills 
                         if skill.lower() not in [s.lower() for s in candidate.skills]]
        if missing_skills:
            self.reasoning_trace.append(ReasoningStep(
                layer="Eligibility Gate",
                rule="R2_MANDATORY_SKILLS",
                result=RuleResult.FAIL,
                explanation=f"Missing mandatory skills: {', '.join(missing_skills)}"
            ))
            return False
        else:
            self.reasoning_trace.append(ReasoningStep(
                layer="Eligibility Gate",
                rule="R2_MANDATORY_SKILLS",
                result=RuleResult.PASS,
                explanation=f"All mandatory skills present: {', '.join(job_role.required_skills)}"
            ))

        # R3: Education Requirement
        education_levels = {
            "high school": 1,
            "associate": 2,
            "bachelors": 3,
            "masters": 4,
            "phd": 5
        }
        
        candidate_edu_level = education_levels.get(candidate.education_level.lower(), 0)
        required_edu_level = education_levels.get(job_role.education_required.lower(), 0)
        
        if candidate_edu_level < required_edu_level:
            self.reasoning_trace.append(ReasoningStep(
                layer="Eligibility Gate",
                rule="R3_EDUCATION_REQUIREMENT",
                result=RuleResult.FAIL,
                explanation=f"Education level '{candidate.education_level}' does not meet requirement '{job_role.education_required}'"
            ))
            return False
        else:
            self.reasoning_trace.append(ReasoningStep(
                layer="Eligibility Gate",
                rule="R3_EDUCATION_REQUIREMENT",
                result=RuleResult.PASS,
                explanation=f"Education level '{candidate.education_level}' meets requirement '{job_role.education_required}'"
            ))

        return True

    def _layer2_risk_evaluation(self, candidate: Candidate, job_role: JobRole) -> str:
        """Layer 2: Risk and gap evaluation. Returns risk level: LOW, MEDIUM, HIGH"""
        risk_flags = 0

        # R4: Skill Gap Threshold (preferred skills)
        preferred_skills_present = [skill for skill in job_role.preferred_skills 
                                   if skill.lower() in [s.lower() for s in candidate.skills]]
        skill_gap_percentage = 0
        if job_role.preferred_skills:
            skill_gap_percentage = (len(job_role.preferred_skills) - len(preferred_skills_present)) / len(job_role.preferred_skills) * 100
        
        if skill_gap_percentage > 50:
            risk_flags += 1
            self.reasoning_trace.append(ReasoningStep(
                layer="Risk & Gap Evaluation",
                rule="R4_SKILL_GAP_THRESHOLD",
                result=RuleResult.FLAGGED,
                explanation=f"Missing {skill_gap_percentage:.0f}% of preferred skills"
            ))
        else:
            self.reasoning_trace.append(ReasoningStep(
                layer="Risk & Gap Evaluation",
                rule="R4_SKILL_GAP_THRESHOLD",
                result=RuleResult.PASS,
                explanation=f"Has {100-skill_gap_percentage:.0f}% of preferred skills"
            ))

        # R5: Employment Gap
        significant_gaps = [gap for gap in candidate.employment_gaps if gap.months >= 6]
        if significant_gaps:
            gaps_with_reason = [gap for gap in significant_gaps if gap.reason_provided]
            if len(gaps_with_reason) < len(significant_gaps):
                risk_flags += 2  # Unexplained gap is higher risk
                self.reasoning_trace.append(ReasoningStep(
                    layer="Risk & Gap Evaluation",
                    rule="R5_EMPLOYMENT_GAP",
                    result=RuleResult.FLAGGED,
                    explanation=f"{len(significant_gaps) - len(gaps_with_reason)} employment gap(s) ≥6 months without explanation"
                ))
            else:
                risk_flags += 1  # Explained gap is lower risk
                self.reasoning_trace.append(ReasoningStep(
                    layer="Risk & Gap Evaluation",
                    rule="R5_EMPLOYMENT_GAP",
                    result=RuleResult.FLAGGED,
                    explanation=f"{len(significant_gaps)} employment gap(s) ≥6 months with explanation provided"
                ))
        else:
            self.reasoning_trace.append(ReasoningStep(
                layer="Risk & Gap Evaluation",
                rule="R5_EMPLOYMENT_GAP",
                result=RuleResult.PASS,
                explanation="No significant employment gaps"
            ))

        # R6: Certification Missing
        # For this demo, we'll check if experience is low but no certifications
        if candidate.experience_years < job_role.min_experience + 2 and not candidate.certifications:
            risk_flags += 1
            self.reasoning_trace.append(ReasoningStep(
                layer="Risk & Gap Evaluation",
                rule="R6_CERTIFICATION_MISSING",
                result=RuleResult.FLAGGED,
                explanation="Limited experience with no certifications to compensate"
            ))
        else:
            self.reasoning_trace.append(ReasoningStep(
                layer="Risk & Gap Evaluation",
                rule="R6_CERTIFICATION_MISSING",
                result=RuleResult.PASS,
                explanation=f"Has {len(candidate.certifications)} certification(s) or sufficient experience"
            ))

        # Determine overall risk level
        if risk_flags == 0:
            return "LOW"
        elif risk_flags <= 2:
            return "MEDIUM"
        else:
            return "HIGH"

    def _layer3_policy_decision(self, risk_level: str) -> DecisionType:
        """Layer 3: Final policy decision based on risk level"""
        
        if risk_level == "LOW":
            # R7: Hire Policy
            self.reasoning_trace.append(ReasoningStep(
                layer="Policy Decision",
                rule="R7_HIRE_POLICY",
                result=RuleResult.APPLIED,
                explanation="Low risk profile → Recommended for hire"
            ))
            return DecisionType.HIRE
        
        elif risk_level == "MEDIUM":
            # R8: Review Policy
            self.reasoning_trace.append(ReasoningStep(
                layer="Policy Decision",
                rule="R8_REVIEW_POLICY",
                result=RuleResult.APPLIED,
                explanation="Medium risk profile → Manual review required"
            ))
            return DecisionType.REVIEW
        
        else:  # HIGH
            # R9: Reject Policy
            self.reasoning_trace.append(ReasoningStep(
                layer="Policy Decision",
                rule="R9_REJECT_POLICY",
                result=RuleResult.APPLIED,
                explanation="High risk profile → Not recommended"
            ))
            return DecisionType.REJECT
