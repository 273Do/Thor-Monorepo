from fastapi import APIRouter, Body, Depends, HTTPException

from src.schemas.extract_steps import ExtractStepsQueryParams
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
async def extract_steps(
    query_params: ExtractStepsQueryParams = Depends(),
    xml_data: str = Body(
        media_type="text/xml",
        description="Apple Healthcareからエクスポートしたzipファイルを解凍した時に取得できるXMLファイル(export.xml)",
    ),
):
    """歩数データの抽出を受け付ける"""

    start_date_of_extract = query_params.start_date_of_extract
    end_date_of_extract = query_params.end_date_of_extract
    months_of_extract = query_params.months_of_extract

    # バリデーション: start_date と end_date の両方が指定されているか、months_of_extract のみが指定されているか
    has_date_range = (
        start_date_of_extract is not None and end_date_of_extract is not None
    )
    has_months = months_of_extract is not None

    if has_date_range and has_months:
        raise HTTPException(
            status_code=400,
            detail="start_date_of_extract / end_date_of_extract と months_of_extract は同時に指定できません。どちらか一方を指定してください。",
        )

    if not has_date_range and not has_months:
        raise HTTPException(
            status_code=400,
            detail="start_date_of_extract / end_date_of_extract の両方、または months_of_extract のいずれかを指定してください。",
        )

    if has_date_range:
        # start_date と end_date の片方だけ指定されていないかチェック
        if start_date_of_extract is None or end_date_of_extract is None:
            raise HTTPException(
                status_code=400,
                detail="start_date_of_extract と end_date_of_extract は両方指定する必要があります。",
            )

    extract_steps_from_applehealthcare(
        xml_data,
        start_date_of_extract,
        end_date_of_extract,
        months_of_extract,
    )
    return {
        "message": "Extracted steps from Apple Healthcare data.",
        "start_date": start_date_of_extract.isoformat()
        if start_date_of_extract
        else None,
        "end_date": end_date_of_extract.isoformat() if end_date_of_extract else None,
        "months_of_extract": months_of_extract,
        "size": len(xml_data),
    }
