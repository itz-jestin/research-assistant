from state import ResearchState
from tools.llm import llm


def writer(state: ResearchState):

    research_text = ""
        
    
    for item in state["research_results"]:
        research_text += f"""
    Question:
    {item['question']}
    
    Answer:
    {item['answer']}
    
    Sources:
    {chr(10).join(item['sources'])}
    
    ----------------------------------------
    """
    feedback = state["feedback"]

    feedback_text = ""

    if feedback:
        feedback_text = f"""
Previous reviewer feedback:

{feedback}

Improve the report according to this feedback.
"""
    all_sources = []

    for item in state["research_results"]:
        all_sources.extend(item["sources"])
    
    all_sources = list(dict.fromkeys(all_sources))
    
    references = "\n".join(all_sources)
    
    prompt = f"""
You are a senior research analyst.

Write a professional research report using ONLY the information below.

Research Material:

{research_text}

{feedback_text}

The report MUST follow this structure.

# Title

A descriptive title.

# Executive Summary

A short summary of the report.

# Introduction

Introduce the topic and explain why it is important.

# Background

Provide context before discussing the findings.

# Key Findings

Explain each major finding under separate headings.

# Conclusion

Summarize the report.

# References

List every source URL used in the research.

Requirements

- Professional writing
- Clear headings
- No markdown tables
- Do not invent facts
- Do not omit important findings
- Use only the supplied research
- Keep references at the end

Reference URLs:

{references}

Return ONLY the report.
"""
    response = llm.invoke(prompt)

    state["final_report"] = response.content

    return state