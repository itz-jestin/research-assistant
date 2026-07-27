from langgraph.graph import StateGraph, END

from state import ResearchState
from agents.planner import planner
from agents.researcher import researcher
from agents.writer import writer
from agents.critic import critic


def route_after_critic(state):

    if state["critique"]["approved"]:
        return END

    if state["retries"] >= 2:
        return END

    return "writer"


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
    route_after_critic,
    {
        "writer": "writer",
        END: END
    }
)

graph = builder.compile()