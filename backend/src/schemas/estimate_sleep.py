from datetime import datetime
from typing import List, Tuple

import pandera as pa
from pandera.typing import Series
from pydantic import BaseModel, Field

from src.schemas.extract_steps import BaseTimeRangeValueDFSchema, StepCountRecord


class EstimateSleepRequest(BaseModel):
    """睡眠状態を推定するリクエストボディ"""

    id: str = Field(examples=["0123456789abcdef_20260101000000"], min_length=1)
    """データ識別用のID"""

    answers: "Answers" = Field(
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

    step_data: List[StepCountRecord] = Field(
        description="睡眠推定に使用する歩数データ",
        examples=[
            [
                {
                    "start_date": "2024-01-01 00:00:00",
                    "end_date": "2024-01-01 00:15:00",
                    "value": 120,
                },
                {
                    "start_date": "2024-01-01 00:15:00",
                    "end_date": "2024-01-01 00:30:00",
                    "value": 0,
                },
            ]
        ],
    )
    """睡眠推定に使用する歩数データ"""


class Answers(BaseModel):
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


class StepClusterRecord(BaseModel):
    """歩数データのクラスターレコードのスキーマ"""

    cluster_label: int = Field(
        description="クラスターのラベル（0: 低歩数, 1: 中歩数, 2: 高歩数）",
        examples=[0],
    )
    """クラスターのラベル"""

    centroid: float = Field(description="クラスターのセントロイド", examples=[50.5])
    """クラスターのセントロイド"""


class StepClusters(BaseModel):
    """歩数データのクラスタリング結果"""

    clusters: Tuple[StepClusterRecord, StepClusterRecord, StepClusterRecord] = Field(
        description="3つのクラスター情報（低歩数、中歩数、高歩数の順）"
    )
    """クラスターのタプル（常に3つ固定: 低歩数、中歩数、高歩数）"""


class EstimateSleepDFSchema(BaseTimeRangeValueDFSchema):
    """睡眠状態を推定するためのDataFrameスキーマ"""

    steps_per_minute: Series[int] = pa.Field(nullable=False)
    """歩数 / 分"""

    cluster_label: Series[int] = pa.Field(nullable=False)
    """クラスターラベル"""


class HourlyStats(BaseModel):
    """時間帯ごとの歩数の統計"""

    hour_range: str = Field(description="時間帯", examples=["0to1"])
    """時間帯"""

    total_steps: int = Field(description="合計歩数", examples=[22])
    """合計歩数"""

    records: int = Field(description="レコード数", examples=[3])
    """レコード数"""


class DailyStats(BaseModel):
    """日付ごとの歩数の統計"""

    date: datetime = Field(
        description="日付",
        examples=["2025-11-01"],
    )
    """日付"""

    hourly_statistics: List[HourlyStats] = Field(
        description="時間帯ごとの統計",
        examples=[
            HourlyStats(hour_range="0to1", total_steps=22, records=3),
            HourlyStats(hour_range="1to2", total_steps=45, records=5),
        ],
    )
    """時間帯ごとの統計"""

    bedtime_answer: int = Field(
        description="就寝時間の回答（0 or 1）",
        examples=[1],
        ge=0,
        le=1,
    )
    """就寝時間の回答（0 or 1）"""


class LateNightFeature(BaseModel):
    """歩数データから夜更かしを推定するための特徴量"""

    feature: List[DailyStats] = Field(description="特徴量")
    """特徴量"""
