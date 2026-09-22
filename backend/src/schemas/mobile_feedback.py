import json
import re
from datetime import datetime
from typing import Any, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MobileSleepContent(BaseModel):
    """モバイルアプリから受け取る睡眠記録の content

    CSV ダンプでは JSON 文字列として格納されているカラム。
    """

    model_config = ConfigDict(populate_by_name=True)

    data_source: str = Field(
        alias="dataSource",
        description="睡眠記録の取得元（sleepApp / intervalEstimation / hourlyEstimation など）",
        examples=["sleepApp"],
    )
    """睡眠記録の取得元"""

    date_from: datetime = Field(
        alias="dateFrom",
        description="就寝日時（UTC）",
        examples=["2026-07-05T14:33:00.000Z"],
    )
    """就寝日時（UTC）"""

    date_from_edit: Optional[datetime] = Field(
        None,
        alias="dateFromEdit",
        description="ユーザーが編集した就寝日時（UTC）",
        examples=["2026-07-05T14:33:00.000Z"],
    )
    """ユーザーが編集した就寝日時（UTC）"""

    date_to: datetime = Field(
        alias="dateTo",
        description="起床日時（UTC）",
        examples=["2026-07-05T22:03:00.000Z"],
    )
    """起床日時（UTC）"""

    date_to_edit: Optional[datetime] = Field(
        None,
        alias="dateToEdit",
        description="ユーザーが編集した起床日時（UTC）",
        examples=["2026-07-05T22:03:00.000Z"],
    )
    """ユーザーが編集した起床日時（UTC）"""

    os: Literal["ios", "android"] = Field(description="記録元の OS", examples=["ios"])
    """記録元の OS"""


class MobileSleepRecord(BaseModel):
    """モバイルアプリ（iOS / Android）から受け取る睡眠記録のレコード"""

    time: datetime = Field(
        description="レコードが記録された日時",
        examples=["2026-07-06 07:13:00+09:00"],
    )
    """レコードが記録された日時"""

    user_id: str = Field(
        description="ユーザーの識別子", examples=["synthetic_ios_stable_01"]
    )
    """ユーザーの識別子"""

    type: str = Field(description="レコードの種別", examples=["sleep"])
    """レコードの種別"""

    content: MobileSleepContent = Field(
        description="睡眠記録の内容（JSON 文字列でも受け付ける）"
    )
    """睡眠記録の内容"""

    affiliation_id: Optional[int] = Field(
        None, description="所属の識別子", examples=[8970]
    )
    """所属の識別子"""

    affiliation_name: Optional[str] = Field(
        None, description="所属の名称", examples=["Synthetic University"]
    )
    """所属の名称"""

    @field_validator("time", mode="before")
    @classmethod
    def _normalize_time(cls, value: Any) -> Any:
        """`+09` のような分を省略した UTC オフセットを `+09:00` に補完する"""

        if isinstance(value, str) and re.search(r"[+-]\d{2}$", value):
            return f"{value}:00"
        return value

    @field_validator("content", mode="before")
    @classmethod
    def _parse_content(cls, value: Any) -> Any:
        """CSV ダンプ由来の JSON 文字列の content をパースする"""

        if isinstance(value, str):
            return json.loads(value)
        return value


class MobileFeedbackRequest(BaseModel):
    """モバイルアプリの睡眠記録からフィードバックを取得するリクエストボディ"""

    records: List[MobileSleepRecord] = Field(
        description="モバイルアプリから取得した睡眠記録のリスト",
        examples=[
            [
                {
                    "time": "2026-07-06 07:40:00+09:00",
                    "user_id": "synthetic_ios_stable_01",
                    "type": "sleep",
                    "content": {
                        "dataSource": "sleepApp",
                        "dateFrom": "2026-07-05T14:36:00.000Z",
                        "dateFromEdit": "2026-07-05T14:36:00.000Z",
                        "dateTo": "2026-07-05T22:30:00.000Z",
                        "dateToEdit": "2026-07-05T22:30:00.000Z",
                        "os": "ios",
                    },
                    "affiliation_id": 8970,
                    "affiliation_name": "Synthetic University",
                }
            ]
        ],
    )
    """モバイルアプリから取得した睡眠記録のリスト"""
