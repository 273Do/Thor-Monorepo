from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from src.schemas.extract_steps import ExtractStepsQueryParams, validate_extract_params
from src.schemas.via_email import ViaEmailRequest
from src.usecases.estimate_sleep.run_estimate_sleep_usecase import run_estimate_sleep
from src.usecases.estimate_sleep.save_data_to_storage_usecase import get_llms
from src.usecases.extract_steps.extract_steps_usecase import (
    extract_steps_from_applehealthcare,
)
from src.usecases.llm_feedback.get_feedback_usecase import get_feedback
from src.usecases.via_email.send_email_usecase import send_email

router = APIRouter(prefix="/via-email", tags=["via-email"])


async def _parse_via_email_req(
    req: str = Form(
        description="アンケート回答・送信先メールアドレスを含むJSONデータ",
        example='{"answers": {"charging_before_bed_answer": 2, "carrying_a_smartphone_answer": 1, "bedtime_answer": 1}, "lang": "ja", "email_to": "user@example.com"}',
    ),
) -> ViaEmailRequest:
    try:
        return ViaEmailRequest.model_validate_json(req)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post(
    "",
    summary="睡眠推定・フィードバック処理を実行し、Email で結果を送信",
    description="睡眠推定・フィードバック処理を実行し、Email で結果を送信する。",
    responses={
        200: {
            "description": "解析・フィードバック処理が完了",
        },
        400: {
            "description": "リクエストのバリデーションエラー",
        },
    },
)
async def via_email(
    query_params: ExtractStepsQueryParams = Depends(),
    xml_file: UploadFile = File(
        description="Apple Healthcareからエクスポートしたzipファイルを解凍した時に取得できるXMLファイル(export.xml)",
    ),
    via_email_req: ViaEmailRequest = Depends(_parse_via_email_req),
) -> None:
    """Email 経由で睡眠推定・フィードバック処理を実行する\n"""

    try:
        validate_extract_params(query_params)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    xml_data = (await xml_file.read()).decode()

    extracted = extract_steps_from_applehealthcare(
        xml_data,
        query_params.start_date_of_extract,
        query_params.end_date_of_extract,
        query_params.months_of_extract,
        query_params.include_recorded_sleep,
    )

    estimated_data, clusters = run_estimate_sleep(
        extracted.id,
        extracted.step_data,
        via_email_req.answers,
    )

    models = get_llms()

    feedback = get_feedback(
        [r.model_dump(mode="json") for r in estimated_data],  # type: ignore
        [c.model_dump(mode="json") for c in clusters],  # type: ignore
        models[0],
        via_email_req.lang,
    )

    print(feedback)

    send_email(via_email_req.email_to, feedback)
