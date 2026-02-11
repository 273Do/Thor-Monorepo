from pydantic import BaseModel, Field


class LLMFeedbackRequest(BaseModel):
    id: str = Field(examples=["0123456789abcdef_20260101000000"], min_length=1)
    """データ識別用のID"""
