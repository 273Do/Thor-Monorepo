from fastapi import APIRouter, Body, Depends, HTTPException

from src.schemas.extract_steps import (
    ExtractedSteps,
    ExtractedStepsResponse,
    ExtractStepsQueryParams,
    validate_extract_params,
)
from src.usecases.extract_steps.extract_steps_usecase import (
    extract_steps_from_applehealthcare,
)

router = APIRouter(prefix="/extract-steps", tags=["extract-steps"])


@router.post(
    "",
    summary="歩数データの抽出",
    description="apple healthcareデータから歩数を抽出します。クエリパラメータで抽出期間か範囲を指定します。",
    responses={
        200: {
            "description": "歩数データの抽出が完了",
        },
        400: {
            "description": "リクエストのバリデーションエラー",
        },
    },
)
def extract_steps(
    query_params: ExtractStepsQueryParams = Depends(),
    xml_data: str = Body(
        media_type="text/xml",
        description="Apple Healthcareからエクスポートしたzipファイルを解凍した時に取得できるXMLファイル(export.xml)",
    ),
) -> ExtractedStepsResponse:
    """歩数データの抽出を受け付ける"""

    try:
        validate_extract_params(query_params)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    extracted_data: ExtractedSteps = extract_steps_from_applehealthcare(
        xml_data,
        query_params.start_date_of_extract,
        query_params.end_date_of_extract,
        query_params.months_of_extract,
        query_params.include_recorded_sleep,
    )

    return ExtractedStepsResponse(data=extracted_data)
