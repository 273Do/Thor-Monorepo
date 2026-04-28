from typing import Literal

from pydantic import BaseModel, Field


class LLMFeedbackParams(BaseModel):
    """LLM による睡眠フィードバックを取得する基底スキーマ"""

    llm: str = Field(description="使用するLLM", examples=["thor-gemma3:latest"])
    """使用するLLM"""

    lang: Literal["ja", "en"] = Field(
        description="LLM のフィードバック言語", examples=["en"]
    )
    """LLM のフィードバック言語"""

    is_specialized: bool = Field(
        description="専門的なフィードバックを返すかどうかのグラグ", examples=[True]
    )
    """専門的なフィードバックを返すかどうかのグラグ"""


class LLMFeedbackRequest(LLMFeedbackParams):
    """LLM による睡眠フィードバックを取得するリクエストボディ"""

    id: str = Field(
        description="データ識別用のID",
        examples=["0123456789abcdef_20260101000000"],
        min_length=1,
    )
    """データ識別用のID"""


class LLMFeedbackResponse(BaseModel):
    """LLM による睡眠フィードバックを取得するレスポンススキーマ"""

    data: str = Field(
        description="LLMからのフィードバック",
        examples=["LLMのフィードバック。マークダウン形式。"],
        min_length=1,
    )
    """LLMからのフィードバック"""
