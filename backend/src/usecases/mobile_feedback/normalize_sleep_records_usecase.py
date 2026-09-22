from datetime import datetime
from typing import Dict, List

from src.core.constants import (
    JST,
    MOBILE_DATA_SOURCE_PRIORITY,
    MOBILE_SLEEP_RECORD_TYPE,
)
from src.schemas.estimate_sleep import DailyEstimateSleepRecord
from src.schemas.mobile_feedback import MobileSleepRecord


def normalize_mobile_sleep_records(
    records: List[MobileSleepRecord],
) -> List[DailyEstimateSleepRecord]:
    """モバイルアプリの睡眠記録を推定睡眠データの形式に正規化する\n
    起床日（JST）を1日とみなし、同じ日に複数の記録がある場合は
    MOBILE_DATA_SOURCE_PRIORITY の優先度が最も高い1件を採用する。

    Args:
        records (List[MobileSleepRecord]): モバイルアプリから取得した睡眠記録のリスト

    Returns:
        List[DailyEstimateSleepRecord]: 日々の睡眠データのリスト（日付の昇順）
    """

    # 起床日ごとに採用するレコードを保持する辞書
    adopted: Dict[datetime, MobileSleepRecord] = {}

    for record in records:
        # 睡眠以外のレコードは対象外
        if record.type != MOBILE_SLEEP_RECORD_TYPE:
            continue

        bed_time, wake_time = _resolve_sleep_time_range(record)

        # 就寝時刻が起床時刻より後の不正なレコードは対象外
        if bed_time >= wake_time:
            continue

        # 起床日（JST）をその睡眠の日付とする
        date = datetime.combine(wake_time.date(), datetime.min.time())

        current = adopted.get(date)
        if current is None or _is_higher_priority(record, current):
            adopted[date] = record

    # 日付の昇順で整列して返す
    results: List[DailyEstimateSleepRecord] = []
    for date in sorted(adopted):
        bed_time, wake_time = _resolve_sleep_time_range(adopted[date])

        results.append(
            DailyEstimateSleepRecord(
                date=date,
                bed_time=bed_time.strftime("%H:%M"),
                wake_time=wake_time.strftime("%H:%M"),
                # 実測値のためデフォルトの時間は使用しない
                is_default_time=[False, False],
            )
        )

    return results


def _resolve_sleep_time_range(
    record: MobileSleepRecord,
) -> tuple[datetime, datetime]:
    """レコードから JST の就寝・起床日時を取得する\n
    ユーザーが編集した日時が存在する場合はそちらを優先する。

    Args:
        record (MobileSleepRecord): モバイルアプリの睡眠記録

    Returns:
        tuple[datetime, datetime]: (就寝日時, 起床日時) いずれも JST
    """

    content = record.content

    bed_time = content.date_from_edit or content.date_from
    wake_time = content.date_to_edit or content.date_to

    return bed_time.astimezone(JST), wake_time.astimezone(JST)


def _is_higher_priority(record: MobileSleepRecord, current: MobileSleepRecord) -> bool:
    """採用済みのレコードより優先度が高いかどうかを判定する\n
    データソースの優先度が同じ場合は、より新しく記録されたレコードを優先する。

    Args:
        record (MobileSleepRecord): 判定対象のレコード
        current (MobileSleepRecord): 採用済みのレコード

    Returns:
        bool: 優先度が高い場合は True
    """

    record_rank = _data_source_rank(record.content.data_source)
    current_rank = _data_source_rank(current.content.data_source)

    if record_rank != current_rank:
        return record_rank < current_rank

    return record.time > current.time


def _data_source_rank(data_source: str) -> int:
    """データソースの優先順位を取得する（値が小さいほど優先度が高い）

    Args:
        data_source (str): 睡眠記録の取得元

    Returns:
        int: 優先順位。未知のデータソースは最も低い優先度となる
    """

    if data_source in MOBILE_DATA_SOURCE_PRIORITY:
        return MOBILE_DATA_SOURCE_PRIORITY.index(data_source)

    return len(MOBILE_DATA_SOURCE_PRIORITY)
