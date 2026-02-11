from fastapi import APIRouter

from src.core.constants import ESTIMATE_SLEEP_JSON_FILENAME
from src.schemas.llm_feedback import LLMFeedbackRequest
from src.usecases.estimate_sleep.save_data_to_storage_usecase import (
    get_data_from_storage,
)
from src.usecases.llm_feedback.get_feedback_usecase import get_feedback

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
def llm_feedback(req: LLMFeedbackRequest) -> str:
    """LLM による睡眠フィードバックを取得する\n
    睡眠推定の結果は NAS に保存済みのため、このエンドポイントでは推定処理を再実行せず、
    保存されたデータを読み込んで LLM にフィードバックを依頼する。
    推定処理とフィードバック処理を分離することで、推定済みのデータに対して
    繰り返しフィードバックを取得できるようにしている。
    新たな睡眠期間のフィードバックがほしい場合は、再度推定処理をするリクエストを投げる。
    """

    id = req.id
    lang = req.lang
    print(id, lang)

    # NAS から推推定睡眠データを取得する
    estimate_sleep_json = get_data_from_storage(id, ESTIMATE_SLEEP_JSON_FILENAME)

    # LLM からフィードバックを取得する
    feedback = get_feedback(estimate_sleep_json)

    return feedback
