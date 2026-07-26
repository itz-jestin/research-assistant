from state import ResearchState
from tools.llm import llm


def writer(state: ResearchState):

    research = state["research_results"]
    feedback = state["feedback"]

    feedback_text = ""

    if feedback:
        feedback_text = f"""
Previous reviewer feedback:

{feedback}

Improve the report according to this feedback.
"""

    prompt = f"""
You are a professional research report writer.

Using the research below, write a detailed report.

Research:

{research}

{feedback_text}

The report should contain:

# Introduction

# Main Findings

# Conclusion

Requirements:

- Well structured
- Professional language
- Comprehensive explanation
- Include important facts
- Do not invent information
- Use only the provided research

Return ONLY the report.
"""

    response = llm.invoke(prompt)

    state["final_report"] = response.content

    return state