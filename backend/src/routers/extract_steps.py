from fastapi import APIRouter, Body

router = APIRouter(prefix="/extract-steps", tags=["extract-steps"])


@router.post(
    "",
    summary="歩数データの抽出",
    description="apple healthcareデータから歩数を抽出します。",
    responses={
        200: {
            "description": "歩数データの抽出が完了",
        }
    },
)
async def extract_steps(
    xml_data: str = Body(
        media_type="text/xml",
        description="Apple Healthcareからエクスポートしたzipファイルを解凍した時に取得できるXMLファイル(export.xml)",
    ),
):
    """歩数データの抽出を受け付ける"""
    return {
        "message": "Extracted steps from Apple Healthcare data.",
        "size": len(xml_data),
    }
