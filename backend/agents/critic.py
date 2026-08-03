from utils.logger import logger
from state import ResearchState
from tools.llm import llm
from schemas.critic import CriticResult

APPROVAL_SCORE_THRESHOLD = 85

INACCURACY_SIGNALS = (
    "inaccura", "incorrect", "error", "mistak", "wrong", "misleading",
    "not accurate", "factual issue", "false claim",
)


def _feedback_flags_inaccuracy(feedback: str) -> bool:
    lowered = feedback.lower()
    return any(signal in lowered for signal in INACCURACY_SIGNALS)


def critic(state: ResearchState):
    logger.info("Critic started")

    report = state["final_report"]
    sub_questions = state["sub_questions"]

    prompt = f"""
You are a senior research reviewer.

Review the following report.

{report}

The report was built to answer these specific sub-questions:
{chr(10).join(f"- {q}" for q in sub_questions)}

Return your response as valid JSON.

Evaluate:

1. Accuracy
2. Coverage
3. Clarity
4. Structure
5. Source quality

IMPORTANT: Write your "feedback" text FIRST in your reasoning, then set
accuracy_issue_found based on what you actually wrote. If your feedback
mentions ANY inaccuracy, error, wrong date, wrong fact, or misleading
claim -- no matter how minor -- accuracy_issue_found MUST be true. A report
cannot have accuracy_issue_found=false if the feedback text names a specific
factual problem. Consistency between feedback and accuracy_issue_found is
mandatory.

If any issue is specific to ONE of the sub-questions above (e.g. a factual
error in the answer to one particular question, or missing depth on one
particular question), add an entry to question_issues with that exact
sub-question text and a description of the issue. Do not add an entry for
sub-questions that were handled well. Leave question_issues empty if all
issues are general/report-wide rather than tied to a specific question.

Return:

{{
    "score": 95,
    "coverage": 9,
    "clarity": 9,
    "structure": 9,
    "source_quality": 9,
    "accuracy_issue_found": false,
    "feedback": "...",
    "question_issues": [
        {{"question": "exact sub-question text", "issue": "what's wrong with the answer to this one"}}
    ]
}}
"""

    logger.info("Sending report to critic LLM")

    response = llm.with_structured_output(CriticResult).invoke(prompt)

    logger.info("Critic response received")

    critique = response.model_dump()

    if _feedback_flags_inaccuracy(critique["feedback"]):
        if not critique["accuracy_issue_found"]:
            logger.warning(
                "Critic feedback mentions an inaccuracy but "
                "accuracy_issue_found was false — overriding to true."
            )
        critique["accuracy_issue_found"] = True

    approved = (
        critique["score"] >= APPROVAL_SCORE_THRESHOLD
        and not critique["accuracy_issue_found"]
    )
    critique["approved"] = approved

    state["critique"] = critique
    state["feedback"] = critique["feedback"]

    if approved:
        logger.info(f"Report approved with score {critique['score']}")
    else:
        logger.warning("Report rejected. Incrementing retry count.")
        state["retries"] += 1

    logger.info("Critic completed")

    return state