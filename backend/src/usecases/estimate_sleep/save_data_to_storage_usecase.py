import json
from pathlib import Path
from typing import List

from src.core.constants import ESTIMATE_SLEEP_JSON_FILENAME, STEP_COUNT_JSON_FILENAME
from src.core.load_env import envs
from src.schemas.estimate_sleep import DailyEstimateSleepRecord
from src.schemas.extract_steps import StepCountRecord


def save_data_to_storage(
    id: str, data: List[StepCountRecord] | List[DailyEstimateSleepRecord]
) -> None:
    """NAS にデータを保存する

    Args:
        id (str): 識別用id
        data (List[StepCountRecord] | List[DailyEstimateSleepRecord]):
        歩数データ | 推定睡眠データ
    """

    # 渡された ID から entity id と version id を抽出する
    # id は基本的に [ hash値_timestamp ] の形式であるため、_で分けたものを適応する
    entry_id, version_id = id.rsplit("_", 1)

    # data の型 から filename を指定する
    if isinstance(data[0], StepCountRecord):
        filename = STEP_COUNT_JSON_FILENAME
    else:
        filename = ESTIMATE_SLEEP_JSON_FILENAME

    # TODO: NASに保存するようにする
    # 保存先のファイルパス
    file_path = Path(
        f"/workspace/backend/{envs.VAULT_DIR}/{entry_id}/{version_id}/{filename}"
    )
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # データを保存する
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            [record.model_dump(mode="json") for record in data],
            f,
            ensure_ascii=False,
            indent=4,
        )

    return


def get_data_from_storage(
    id: str, filename: str
) -> List[StepCountRecord] | List[DailyEstimateSleepRecord]:
    """NAS からデータを取得する

    Args:
        id (str): 識別用id
        filename (str): ファイル名

    Returns:
        List[StepCountRecord] | List[DailyEstimateSleepRecord]: 保存されたJSONデータ
    """

    # 渡された ID から entity id と version id を抽出する
    # id は基本的に [ hash値_timestamp ] の形式であるため、_で分けたものを適応する
    entry_id, version_id = id.rsplit("_", 1)

    # TODO: NASから取得するようにする

    # 読み込むデータのファイルパス
    file_path = Path(
        f"/workspace/backend/{envs.VAULT_DIR}/{entry_id}/{version_id}/{filename}"
    )

    with open(file_path, encoding="utf-8") as f:
        return json.load(f)
