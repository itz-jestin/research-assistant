import json

from state import ResearchState
from tools.llm import llm
from schemas.critic import CriticResult


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
Return ONLY valid JSON.

{{
    "approved": true,
    "score": 90,
    "coverage": 9,
    "clarity": 9,
    "structure": 9,
    "source_quality": 9,
    "feedback": "Excellent report."
}}
"""

    response = llm.invoke(prompt)

    content = response.content.strip()
    
    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()
    print("===== RAW LLM RESPONSE =====")
    print(content)
    print("============================")
    data = json.loads(content)
    
    critique = CriticResult(**data)
    
    state["critique"] = critique.model_dump()
    
    state["feedback"] = critique.feedback
    
    if not critique.approved:
        state["retries"] += 1

    return state