from fastapi import APIRouter

from src.schemas.llm_feedback import LLMFeedbackRequest

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
    print(id)

    return
