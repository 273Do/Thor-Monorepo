from pydantic import BaseModel, Field

from src.schemas.extract_steps import StepCountRecord


class EstimateSleepRequest(BaseModel):
    """睡眠状態を推定するリクエストボディ"""

    id: str = Field(examples=["0123456789abcdef_20260101000000"], min_length=1)
    """データ識別用のID"""

    questions: "Questions" = Field(
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

    step_data: list[StepCountRecord] = Field(
        description="睡眠推定に使用する歩数データ",
        examples=[
            [
                {
                    "startDate": "2024-01-01 00:00:00",
                    "endDate": "2024-01-01 00:15:00",
                    "value": 120,
                },
                {
                    "startDate": "2024-01-01 00:15:00",
                    "endDate": "2024-01-01 00:30:00",
                    "value": 0,
                },
            ]
        ],
    )
    """睡眠推定に使用する歩数データ"""


class Questions(BaseModel):
    """睡眠状態を推定するためのアンケートの回答"""

    charging_before_bed_answer: int = Field(
        description="就寝何時間前にスマホを充電するかの回答（0 ~ 4）",
        examples=[2],
        ge=0,
        le=4,
    )
    """就寝何時間前にスマホを充電するかの回答（0 ~ 4）"""

    carrying_a_smartphone_answer: int = Field(
        description="家の中でスマホを持ち歩くかの回答（0 ~ 2）",
        examples=[1],
        ge=0,
        le=2,
    )
    """家の中でスマホを持ち歩くかの回答（0 ~ 2）"""

    bedtime_answer: int = Field(
        description="就寝時間の回答（0 or 1）",
        examples=[1],
        ge=0,
        le=1,
    )
    """就寝時間の回答（0 or 1）"""
