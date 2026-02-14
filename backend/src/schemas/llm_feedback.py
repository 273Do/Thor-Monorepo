from typing import Literal

from pydantic import BaseModel, Field


class LLMFeedbackRequest(BaseModel):
    id: str = Field(
        description="データ識別用のID",
        examples=["0123456789abcdef_20260101000000"],
        min_length=1,
    )
    """データ識別用のID"""

    llm: str = Field(description="使用するLLM", examples=["thor-gemma3:latest"])
    """使用するLLM"""

    lang: Literal["ja", "en"] = Field(
        description="LLM のフィードバック言語", examples=["en"]
    )
    """LLM のフィードバック言語"""
