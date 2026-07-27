from pydantic import BaseModel, Field


class CriticResult(BaseModel):
    approved: bool = Field(
        description="Whether the report is approved."
    )

    score: int = Field(
        ge=0,
        le=100,
        description="Overall quality score."
    )

    coverage: int = Field(
        ge=0,
        le=10
    )

    clarity: int = Field(
        ge=0,
        le=10
    )

    structure: int = Field(
        ge=0,
        le=10
    )

    source_quality: int = Field(
        ge=0,
        le=10
    )

    feedback: str