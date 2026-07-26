from pydantic import BaseModel, Field


class PlannerOutput(BaseModel):
    sub_questions: list[str] = Field(
        description="List of 2-4 research sub-questions."
    )