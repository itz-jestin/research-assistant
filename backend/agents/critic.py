import json

from state import ResearchState
from tools.llm import llm
from schemas.critic import CriticResult
from pydantic import BaseModel, Field


class CriticResult(BaseModel):
    approved: bool = Field(description="Whether the report meets quality standards.")
    score: int = Field(ge=0, le=100, description="Overall quality score from 0 to 100.")
    coverage: int = Field(ge=0, le=10)
    clarity: int = Field(ge=0, le=10)
    structure: int = Field(ge=0, le=10)
    source_quality: int = Field(ge=0, le=10)
    feedback: str

def critic(state: ResearchState):

    report = state["final_report"]

    prompt = f"""
You are a senior research reviewer.

Evaluate the following report.

{report}

Evaluate it on the following criteria:

1. Coverage
2. Clarity
3. Structure
4. Source Quality
5. Accuracy

Scoring Rules

Coverage:
0 = Poor
10 = Excellent

Clarity:
0 = Poor
10 = Excellent

Structure:
0 = Poor
10 = Excellent

Source Quality:
0 = Poor
10 = Excellent

Overall Score:
0-100

Approve the report only if

- Overall score >= 85
- Coverage >= 8
- Clarity >= 8
- Structure >= 8
- Source Quality >= 8

Provide concise feedback describing what should be improved.
"""

    structured_llm = llm.with_structured_output(CriticResult)

    critique = structured_llm.invoke(prompt)

    # Save complete critique
    state["critique"] = critique.model_dump()

    # Save only feedback separately
    state["feedback"] = critique.feedback

    # Increase retry count only if rejected
    if not critique.approved:
        state["retries"] += 1

    return state