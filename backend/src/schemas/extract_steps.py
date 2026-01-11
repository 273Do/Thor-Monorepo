from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel


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


class DataRecord(BaseModel):
    """推定に使用するレコードのスキーマ"""

    startDate: str
    """記録開始日時"""

    endDate: str
    """記録終了日時"""

    value: int
    """値"""


class ExtractedSteps(BaseModel):
    """解析に使用する基本となる歩数データのスキーマ"""

    id: str
    """データ識別用のID"""

    stepData: list[DataRecord]
    """抽出された歩数データのリスト"""

    sleepData: Optional[list[DataRecord]] = None
    """抽出された睡眠データのリスト（存在する場合）"""


class ExtractedStepsResponse(BaseModel):
    """歩数データ抽出APIのレスポンススキーマ"""

    data: ExtractedSteps
    """抽出された歩数データ"""
