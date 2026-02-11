from fastapi import APIRouter

from src.core.constants import ESTIMATE_SLEEP_JSON_FILENAME
from src.schemas.llm_feedback import LLMFeedbackRequest
from src.usecases.estimate_sleep.save_data_to_storage_usecase import (
    get_data_from_storage,
)

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post(
    "",
    summary="推定した睡眠状態を使ってLLMからフィードバックを取得",
    description="推定した睡眠状態を使ってLLMからフィードバックを取得する。",
    responses={
        200: {
            "description": "フィードバック処理が完了",
        },
        400: {
            "description": "リクエストのバリデーションエラー",
        },
    },
)
def llm_feedback(req: LLMFeedbackRequest):
    """フィードバックを受け付ける"""

    id = req.id
    lang = req.lang
    print(id, lang)

    get_data_from_storage(id, ESTIMATE_SLEEP_JSON_FILENAME)

    return
