from fastapi import APIRouter

from src.schemas.estimate_sleep import EstimateSleepResponse
from src.schemas.mobile_feedback import MobileFeedbackRequest
from src.usecases.estimate_sleep.save_data_to_storage_usecase import get_llms
from src.usecases.mobile_feedback.normalize_sleep_records_usecase import (
    normalize_mobile_sleep_records,
)

router = APIRouter(prefix="/mobile-feedback", tags=["mobile-feedback"])


@router.post(
    "",
    summary="モバイルアプリの睡眠記録を正規化",
    description="iOS / Android のアプリから取得した睡眠記録を、睡眠推定と同じ形式に正規化して返す。",
    responses={
        200: {
            "description": "睡眠記録の正規化が完了",
        },
        400: {
            "description": "リクエストのバリデーションエラー",
        },
    },
)
def mobile_feedback(req: MobileFeedbackRequest) -> EstimateSleepResponse:
    """モバイルアプリの睡眠記録を受け付ける"""

    normalized_data = normalize_mobile_sleep_records(req.records)
    models = get_llms()

    # TODO: 正規化した睡眠記録をストレージに保存する処理を追加する
    # TODO: LLMsの推論結果を返すようにする（現状は空のリストを返す）

    return EstimateSleepResponse(data=normalized_data, models=models)
