from utils.logger import logger
from state import ResearchState
from tools.llm import llm


def writer(state: ResearchState):

    logger.info("Writer started")

    research = state["research_results"]

    prompt = f"""
You are a professional research report writer.

Using the research below, write a detailed report.

Research:

{research}

The report should contain:

# Introduction

# Main Findings

# Conclusion

Return only the report.
"""

    logger.info("Sending report generation request to LLM")

    response = llm.invoke(prompt)

    logger.info("Report generated successfully")

    state["final_report"] = response.content

    logger.info("Writer completed")

    return state