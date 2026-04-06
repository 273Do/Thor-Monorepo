from fastapi import APIRouter

from src.schemas.estimate_sleep import EstimateSleepRequest, EstimateSleepResponse
from src.usecases.estimate_sleep.run_estimate_sleep_usecase import run_estimate_sleep
from src.usecases.estimate_sleep.save_data_to_storage_usecase import get_llms

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

    estimated_data, _ = run_estimate_sleep(req.id, req.step_data, req.answers)
    models = get_llms()

    return EstimateSleepResponse(data=estimated_data, models=models)
