from datetime import datetime
from typing import Optional

from fastapi import Query


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
    ):
        self.start_date_of_extract = start_date_of_extract
        self.end_date_of_extract = end_date_of_extract
        self.months_of_extract = months_of_extract

    def __iter__(self):
        """アンパック可能にする"""
        return iter(
            [
                self.start_date_of_extract,
                self.end_date_of_extract,
                self.months_of_extract,
            ]
        )
