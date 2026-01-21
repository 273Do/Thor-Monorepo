import pandas as pd
from fastapi import APIRouter
from pandera.typing import DataFrame

from src.schemas.estimate_sleep import EstimateSleepRequest
from src.schemas.extract_steps import StepCountDFSchema
from src.usecases.estimate_sleep.step_clustering import step_clustering

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
def estimate_sleep(req: EstimateSleepRequest):
    """睡眠推定を受け付ける"""

    id = req.id
    questions = req.questions
    step_data = req.step_data

    print(id)
    print(questions)

    # TODO: NAS に入力データを保存

    step_count_df: DataFrame[StepCountDFSchema] = pd.DataFrame(
        [record.model_dump() for record in step_data]
    )  # type: ignore

    # 1分あたりの歩数を計算しクラスタリングを行う
    estimate_sleep_df, cluster_stats = step_clustering(step_count_df)

    print(estimate_sleep_df)

    print(cluster_stats)

    return
