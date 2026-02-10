import json
from pathlib import Path
from typing import List

from src.core.constants import ESTIMATE_SLEEP_JSON_FILENAME, STEP_COUNT_JSON_FILENAME
from src.core.load_env import envs
from src.schemas.estimate_sleep import DailyEstimateSleepRecord
from src.schemas.extract_steps import StepCountRecord


def save_data_to_storage(
    id: str, data: List[StepCountRecord] | List[DailyEstimateSleepRecord]
):
    # 渡された ID から entity id と version id を抽出する
    # id は基本的に [ hash値_timestamp ] の形式であるため、_で分けたものを適応する
    entry_id, version_id = id.rsplit("_", 1)

    # data の型 から filename を指定する
    if isinstance(data[0], StepCountRecord):
        filename = STEP_COUNT_JSON_FILENAME
    else:
        filename = ESTIMATE_SLEEP_JSON_FILENAME

    # 保存先のファイルパス
    file_path = Path(
        f"/workspace/backend/{envs.VAULT_DIR}/{entry_id}/{version_id}/{filename}"
    )
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # データを保存する
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            [record.model_dump() for record in data], f, ensure_ascii=False, indent=4
        )

    return
