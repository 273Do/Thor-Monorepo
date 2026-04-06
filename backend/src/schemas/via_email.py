from typing import Literal

from pydantic import BaseModel, EmailStr, Field

from src.schemas.estimate_sleep import Answers


class ViaEmailRequest(BaseModel):
    """Email経由で解析を実行するリクエストボディ"""

    answers: Answers = Field(description="睡眠状態を推定するためのアンケートの回答")
    """睡眠状態を推定するためのアンケートの回答"""

    lang: Literal["ja", "en"] = Field(
        description="LLM のフィードバック言語", examples=["ja"]
    )
    """LLM のフィードバック言語"""

    email_to: EmailStr = Field(
        description="結果を送信するメールアドレス", examples=["user@example.com"]
    )
    """結果を送信するメールアドレス"""
