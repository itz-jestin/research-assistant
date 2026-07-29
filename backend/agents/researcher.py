import json

from utils.logger import logger
from tools.search import search_web
from tools.llm import llm
from schemas.researcher import ResearchResult
from state import ResearchState


def researcher(state: ResearchState):

    logger.info("Researcher started")

    results = []

    feedback = state["feedback"]

    for index, question in enumerate(state["sub_questions"], start=1):

        logger.info(f"Researching question {index}: {question}")

        search_results = search_web(question)

        logger.info(f"Found {len(search_results)} search results")

        context = ""

        for item in search_results:

            context += f"""
Title:
{item['title']}

Content:
{item['content']}

URL:
{item['url']}

"""

        feedback_text = ""

        if feedback:
            feedback_text = f"""
Previous reviewer feedback:

{feedback}

Improve your answer based on this feedback.
"""

        prompt = f"""
You are an AI Research Assistant.

Answer ONLY using the search results below.

Question:
{question}

Search Results:

{context}

{feedback_text}

Return ONLY valid JSON.

{{
    "question": "...",
    "answer": "...",
    "sources": ["url1","url2"]
}}
"""

        logger.info("Sending request to LLM")

        response = llm.with_structured_output(ResearchResult).invoke(prompt)

        logger.info("LLM response received")

        validated = response

        results.append(validated.model_dump())

        logger.info(f"Completed question {index}")

    state["research_results"] = results

    logger.info(f"Researcher completed {len(results)} questions")

    return state