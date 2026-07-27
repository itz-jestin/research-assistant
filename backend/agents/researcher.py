import json

from tools.search import search_web
from tools.llm import llm

from schemas.researcher import ResearchResult
from state import ResearchState


def researcher(state: ResearchState):

    results = []

    feedback = state["feedback"]

    for question in state["sub_questions"]:

        search_results = search_web(question)

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
        structured_llm = llm.with_structured_output(ResearchResult)

        validated = structured_llm.invoke(prompt)

        results.append(validated.model_dump())

    state["research_results"] = results

    return state