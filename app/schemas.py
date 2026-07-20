from typing import List, Literal, Optional

from pydantic import BaseModel, Field

Department = Literal["hr", "it", "finance", "legal"]


class ClassificationResult(BaseModel):

    department: Department = Field(
        description="The single best-matching department for this query."
    )
    confidence: float = Field(
        ge=0, le=1, description="Confidence in this classification, from 0 to 1."
    )
    reasoning: str = Field(
        description="One or two sentences explaining why this department was chosen."
    )


class EvaluationScores(BaseModel):

    relevance: int = Field(
        ge=1, le=5, description="Does the answer address what the user actually asked?"
    )
    completeness: int = Field(
        ge=1, le=5, description="Does the answer cover everything the question needs?"
    )
    accuracy: int = Field(
        ge=1,
        le=5,
        description="Is the answer faithful to the retrieved context, with no invented facts?",
    )
    rationale: str = Field(description="Brief justification for the three scores.")


class RoutingResult(BaseModel):

    query: str
    department: Department
    confidence: float
    reasoning: str
    answer: str
    sources: List[str]
    trace_id: Optional[str] = None
    trace_url: Optional[str] = None
    scores: Optional[EvaluationScores] = None
