from datetime import datetime
from typing import List, Optional

import pandera as pa
from fastapi import Query
from pandera.typing import Series
from pydantic import BaseModel, Field

from src.core.constants import SLEEP_ANALYSIS_IN_BED


class ExtractStepsQueryParams:
    """歩数の抽出範囲を設定するクエリパラメータ"""

    def __init__(
        self,
        start_date_of_extract: Optional[datetime] = Query(
            None,
            description="解析開始日 (ISO 8601形式)",
            examples=["2025-11-01T00:00:00Z"],
        ),
        end_date_of_extract: Optional[datetime] = Query(
            None,
            description="解析終了日 (ISO 8601形式)",
            examples=["2026-01-01T00:00:00Z"],
        ),
        months_of_extract: Optional[int] = Query(
            None,
            description="最新の日付から遡って抽出する歩数データの月数",
            examples=[1],
        ),
        include_recorded_sleep: Optional[bool] = Query(
            False,
            description="記録された睡眠データを含めるかどうか",
            examples=[False],
        ),
    ):
        self.start_date_of_extract = start_date_of_extract
        self.end_date_of_extract = end_date_of_extract
        self.months_of_extract = months_of_extract
        self.include_recorded_sleep = include_recorded_sleep

    def __iter__(self):
        """アンパック可能にする"""
        return iter(
            [
                self.start_date_of_extract,
                self.end_date_of_extract,
                self.months_of_extract,
                self.include_recorded_sleep,
            ]
        )


class StepCountRecord(BaseModel):
    """睡眠推定に使用する歩数レコードのスキーマ"""

    start_date: str = Field(
        description="記録開始日時",
        examples=["2025-11-01T00:00:00Z"],
    )
    """記録開始日時"""

    end_date: str = Field(
        description="記録終了日時",
        examples=["2026-01-01T00:00:00Z"],
    )
    """記録終了日時"""

    value: int = Field(
        description="歩数の値",
        examples=[273],
    )
    """値"""


class SleepAnalysisRecord(BaseModel):
    """睡眠レコードのスキーマ"""

    start_date: str = Field(
        description="記録開始日時",
        examples=["2025-11-01T00:00:00Z"],
    )
    """記録開始日時"""

    end_date: str = Field(
        description="記録終了日時",
        examples=["2026-01-01T00:00:00Z"],
    )
    """記録終了日時"""

    value: str = Field(
        description="睡眠状態の値",
        examples=[SLEEP_ANALYSIS_IN_BED],
    )
    """値"""


class BaseTimeRangeValueDFSchema(pa.DataFrameModel):
    """StepCount / SleepAnalysis の共通 DataFrame スキーマ"""

    start_date: Series[str] = pa.Field(nullable=False)
    """記録開始日時"""

    end_date: Series[str] = pa.Field(nullable=False)
    """記録終了日時"""

    value: Series[str] = pa.Field(nullable=False)
    """値"""

    class Config:  # type: ignore
        coerce = False
        strict = True


class StepCountDFSchema(BaseTimeRangeValueDFSchema):
    """歩数データのDataFrameスキーマ"""

    pass


class SleepAnalysisDFSchema(BaseTimeRangeValueDFSchema):
    """睡眠分析データのDataFrameスキーマ"""

    pass


class ExtractedSteps(BaseModel):
    """抽出された歩数データと睡眠データのスキーマ"""

    id: str = Field(
        description="データ識別用のID", examples=["0123456789abcdef_20260101000000"]
    )
    """データ識別用のID"""

    step_data: List[StepCountRecord] = Field(description="抽出された歩数データのリスト")
    """抽出された歩数データのリスト"""

    sleep_data: Optional[List[SleepAnalysisRecord]] = Field(
        None, description="抽出された睡眠データのリスト"
    )
    """抽出された睡眠データのリスト（存在する場合）"""


class ExtractedStepsResponse(BaseModel):
    """歩数データ抽出APIのレスポンススキーマ"""

    data: ExtractedSteps = Field(
        description="抽出された歩数データと睡眠データのスキーマ"
    )
    """抽出された歩数データと睡眠データのスキーマ"""
