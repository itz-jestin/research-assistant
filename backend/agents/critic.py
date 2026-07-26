import json

from state import ResearchState
from tools.llm import llm


def critic(state: ResearchState):

    report = state["final_report"]

    prompt = f"""
You are an expert research reviewer.

Review the report below.

{report}

Evaluate the report based on:

- Accuracy
- Completeness
- Structure
- Missing information
- Source quality

Reply ONLY in valid JSON.

{{
    "approved": true,
    "feedback": "Short feedback describing improvements if needed."
}}

If the report is excellent,
approved should be true.

Otherwise,
approved should be false.
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    data = json.loads(content)

    # Save complete critique
    state["critique"] = data

    # Save only feedback separately
    state["feedback"] = data["feedback"]

    # Increase retry count only if rejected
    if not data["approved"]:
        state["retries"] += 1

    return state