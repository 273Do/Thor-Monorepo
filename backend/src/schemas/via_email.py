from pydantic import EmailStr, Field

from src.schemas.estimate_sleep import Answers
from src.schemas.llm_feedback import LLMFeedbackParams


class ViaEmailRequest(LLMFeedbackParams):
    """Email経由で解析を実行するリクエストボディ"""

    answers: Answers = Field(
        description="睡眠状態を推定するためのアンケートの回答",
        examples=[
            {
                "charging_before_bed_answer": 2,
                "carrying_a_smartphone_answer": 1,
                "bedtime_answer": 1,
            }
        ],
    )
    """睡眠状態を推定するためのアンケートの回答"""

    email_to: EmailStr = Field(
        description="結果を送信するメールアドレス", examples=["user@example.com"]
    )
    """結果を送信するメールアドレス"""
