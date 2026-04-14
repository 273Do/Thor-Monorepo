from typing import List, Tuple

import pandas as pd
from pandera.typing import DataFrame

from src.schemas.estimate_sleep import (
    Answers,
    DailyEstimateSleepRecord,
    StepClusterRecord,
)
from src.schemas.extract_steps import StepCountDFSchema, StepCountRecord
from src.usecases.estimate_sleep.detection_late_night_usecase import detect_late_night
from src.usecases.estimate_sleep.estimate_sleep_duration_usecase import (
    estimate_sleep_duration_from_step,
)
from src.usecases.estimate_sleep.feature_of_late_night_usecase import (
    create_feature_value,
)
from src.usecases.estimate_sleep.save_data_to_storage_usecase import (
    save_data_to_storage,
)
from src.usecases.estimate_sleep.step_clustering_usecase import step_clustering


def run_estimate_sleep(
    id: str,
    step_data: List[StepCountRecord],
    answers: Answers,
) -> Tuple[
    List[DailyEstimateSleepRecord],
    Tuple[StepClusterRecord, StepClusterRecord, StepClusterRecord],
]:
    """歩数データからの睡眠推定処理を一括実行する

    Args:
        id (str): データ識別用のID
        step_data (List[StepCountRecord]): 歩数データ
        answers (Answers): アンケートの回答

    Returns:
        Tuple: (推定睡眠データ, 歩数クラスター)
    """

    save_data_to_storage(id, step_data)

    step_count_df: DataFrame[StepCountDFSchema] = pd.DataFrame(
        [record.model_dump() for record in step_data]
    )  # type: ignore

    estimate_going_out_df, cluster_stats = step_clustering(step_count_df)
    feature = create_feature_value(step_count_df, answers.bedtime_answer)
    late_night_list = detect_late_night(feature)

    estimated_data = estimate_sleep_duration_from_step(
        estimate_going_out_df,
        late_night_list,
        answers.charging_before_bed_answer,
        answers.carrying_a_smartphone_answer,
    )

    save_data_to_storage(id, cluster_stats.clusters)
    save_data_to_storage(id, estimated_data)

    return estimated_data, cluster_stats.clusters
