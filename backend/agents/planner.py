import json

from utils.logger import logger
from state import ResearchState
from prompts.planner_prompt import PLANNER_PROMPT
from schemas.planner import PlannerOutput
from tools.llm import llm


def planner(state: ResearchState):
    logger.info("Planner started")

    query = state["query"]

    prompt = f"""
{PLANNER_PROMPT}

User Query:
{query}
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    logger.info("Raw planner response received")

    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    data = json.loads(content)

    validated = PlannerOutput(**data)

    state["sub_questions"] = validated.sub_questions

    logger.info(f"Planner generated {len(validated.sub_questions)} sub-questions")
    logger.info("Planner completed")

    return state