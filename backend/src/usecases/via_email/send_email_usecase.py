from fastapi import HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from src.core.load_env import envs

conf = ConnectionConfig(
    MAIL_USERNAME=envs.MAIL_USERNAME,
    MAIL_PASSWORD=envs.MAIL_PASSWORD,  # type: ignore
    MAIL_FROM=envs.MAIL_FROM,
    MAIL_PORT=envs.MAIL_PORT,
    MAIL_SERVER=envs.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email(email_to: str, feedback: str) -> None:
    try:
        message = MessageSchema(
            subject="睡眠推定フィードバック",
            recipients=[email_to],  # type: ignore
            body=feedback,
            subtype=MessageType.plain,
        )
        fm = FastMail(conf)
        await fm.send_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"エラー: {str(e)}")
