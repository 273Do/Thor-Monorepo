import pandas as pd
from fastapi import APIRouter
from pandera.typing import DataFrame

from src.schemas.estimate_sleep import EstimateSleepRequest, EstimateSleepResponse
from src.schemas.extract_steps import StepCountDFSchema
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

router = APIRouter(prefix="/estimate-sleep", tags=["estimate-sleep"])


@router.post(
    "",
    summary="歩数データから睡眠状態を推定",
    description="歩数データから睡眠状態を推定する。",
    responses={
        200: {
            "description": "睡眠推定が完了",
        },
        400: {
            "description": "リクエストのバリデーションエラー",
        },
    },
)
def estimate_sleep(req: EstimateSleepRequest) -> EstimateSleepResponse:
    """睡眠推定を受け付ける"""

    id = req.id
    answers = req.answers
    step_data = req.step_data

    print(id)
    print(answers)

    # NAS に入力データを保存
    save_data_to_storage(id, step_data)

    step_count_df: DataFrame[StepCountDFSchema] = pd.DataFrame(
        [record.model_dump() for record in step_data]
    )  # type: ignore

    # 外出検知のため1分あたりの歩数を計算しクラスタリングを行う
    estimate_going_out_df, _cluster_stats = step_clustering(step_count_df)

    # 歩数データから夜更かしを推定するための特徴量を抽出
    feature = create_feature_value(step_count_df, answers.bedtime_answer)

    # 特徴量から夜更かし検知を行う
    late_night_list = detect_late_night(feature)

    # print(late_night_list)

    # print(estimate_going_out_df)

    # print(cluster_stats)

    # 歩数データから睡眠時刻を推定する
    estimated_data = estimate_sleep_duration_from_step(
        estimate_going_out_df,
        late_night_list,
        answers.charging_before_bed_answer,
        answers.carrying_a_smartphone_answer,
    )

    # NAS に推定結果を保存
    save_data_to_storage(id, estimated_data)

    return EstimateSleepResponse(data=estimated_data)
