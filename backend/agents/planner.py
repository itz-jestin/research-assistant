import json

from state import ResearchState
from prompts.planner_prompt import PLANNER_PROMPT
from schemas.planner import PlannerOutput
from tools.llm import llm


def planner(state: ResearchState):
    query = state["query"]

    prompt = f"""
{PLANNER_PROMPT}

User Query:
{query}
"""

    response = llm.invoke(prompt)

    # Get the response text
    content = response.content.strip()

    # Remove markdown if the model returns ```json ... ```
    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    # Convert JSON string to Python dictionary
    data = json.loads(content)

    # Validate using Pydantic
    validated = PlannerOutput(**data)

    # Update the LangGraph state
    state["sub_questions"] = validated.sub_questions

    return state