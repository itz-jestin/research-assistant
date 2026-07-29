from utils.logger import logger
from state import ResearchState
from tools.llm import llm
from schemas.critic import CriticResult


def critic(state: ResearchState):

    logger.info("Critic started")

    report = state["final_report"]

    prompt = f"""
You are a senior research reviewer.

Review the following report.

{report}

Return your response as valid JSON.

Evaluate:

1. Accuracy
2. Coverage
3. Clarity
4. Structure
5. Source quality

Return:

{{
    "approved": true,
    "score": 95,
    "coverage": 9,
    "clarity": 9,
    "structure": 9,
    "source_quality": 9,
    "feedback": "..."
}}
"""

    logger.info("Sending report to critic LLM")

    response = llm.with_structured_output(CriticResult).invoke(prompt)

    logger.info("Critic response received")

    critique = response.model_dump()

    state["critique"] = critique
    state["feedback"] = critique["feedback"]

    if critique["approved"]:
        logger.info(f"Report approved with score {critique['score']}")
    else:
        logger.warning("Report rejected. Incrementing retry count.")
        state["retries"] += 1

    logger.info("Critic completed")

    return state