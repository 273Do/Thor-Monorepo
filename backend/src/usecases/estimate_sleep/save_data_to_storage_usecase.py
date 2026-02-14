import json
from pathlib import Path
from typing import List, Tuple

from src.core.constants import (
    ESTIMATE_SLEEP_JSON_FILENAME,
    STEP_CLUSTER_JSON_FILENAME,
    STEP_COUNT_JSON_FILENAME,
)
from src.core.load_env import envs
from src.schemas.estimate_sleep import DailyEstimateSleepRecord, StepClusterRecord
from src.schemas.extract_steps import StepCountRecord


def save_data_to_storage(
    id: str,
    data: List[StepCountRecord]
    | List[DailyEstimateSleepRecord]
    | Tuple[StepClusterRecord, StepClusterRecord, StepClusterRecord],
) -> None:
    """NAS にデータを保存する

    Args:
        id (str): 識別用id
        data (List[StepCountRecord] | List[DailyEstimateSleepRecord]) | Tuple[StepClusterRecord, StepClusterRecord, StepClusterRecord]:
        歩数データ | 推定睡眠データ | 歩数クラスターデータ
    """

    # 渡された ID から entity id と version id を抽出する
    # id は基本的に [ hash値_timestamp ] の形式であるため、_で分けたものを適応する
    entry_id, version_id = id.rsplit("_", 1)

    # data の型 から filename を指定する
    if isinstance(data[0], StepCountRecord):
        filename = STEP_COUNT_JSON_FILENAME
    elif isinstance(data[0], DailyEstimateSleepRecord):
        filename = ESTIMATE_SLEEP_JSON_FILENAME
    else:
        filename = STEP_CLUSTER_JSON_FILENAME

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
) -> (
    List[StepCountRecord]
    | List[DailyEstimateSleepRecord]
    | Tuple[StepClusterRecord, StepClusterRecord, StepClusterRecord]
):
    """NAS からデータを取得する

    Args:
        id (str): 識別用id
        filename (str): ファイル名

    Returns:
        List[StepCountRecord] | List[DailyEstimateSleepRecord] | Tuple[StepClusterRecord, StepClusterRecord, StepClusterRecord]:
        保存されたJSONデータ
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


def get_llms() -> List[str]:
    """フィードバックに使用可能なLLMを取得する

    Returns:
        List[str]: フィードバックに使用可能なLLMの一覧
    """

    file_path = f"/workspace/backend/{envs.DATASTORE_DIR}/models.json"

    with open(file_path, encoding="utf-8") as f:
        return json.load(f)
