from langgraph.graph import StateGraph, END

from state import ResearchState
from agents.planner import planner
from agents.researcher import researcher
from agents.writer import writer
from agents.critic import critic

def should_retry(state):
    print("Retries:",state["retries"])
    print("Approved:",state["critique"]["approved"])
    critique = state["critique"]
    retries = state["retries"]

    if critique["approved"]:
        return "approved"

    if retries >= 2:
        return "approved"

    return "retry"




builder = StateGraph(ResearchState)

builder.add_node("planner", planner)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("critic", critic)

builder.set_entry_point("planner")

builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", "critic")

builder.add_conditional_edges(
    "critic",
    should_retry,
    {
        "approved": END,
        "retry": "researcher",
    },
)

graph = builder.compile()