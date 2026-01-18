from fastapi import APIRouter

from src.schemas.estimate_sleep import EstimateSleepRequest

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
    print(step_data)
    return
