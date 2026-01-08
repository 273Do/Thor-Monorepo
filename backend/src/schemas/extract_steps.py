from datetime import datetime
from typing import Optional

from fastapi import Query


class ExtractStepsQueryParams:
    """歩数の抽出範囲を設定するクエリパラメータ"""

    def __init__(
        self,
        start_date: Optional[datetime] = Query(
            description="解析開始日 (ISO 8601形式)",
            examples=["2025-11-01T00:00:00Z"],
        ),
        end_date: Optional[datetime] = Query(
            description="解析終了日 (ISO 8601形式)",
            examples=["2026-01-01T00:00:00Z"],
        ),
        months_of_extract: Optional[int] = Query(
            description="最新の日付から遡って抽出する歩数データの月数",
            examples=[1],
        ),
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.months_of_extract = months_of_extract

    def __iter__(self):
        """アンパック可能にする"""
        return iter([self.start_date, self.end_date, self.months_of_extract])
