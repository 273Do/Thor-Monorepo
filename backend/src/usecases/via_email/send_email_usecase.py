from pathlib import Path
from typing import Literal

import markdown
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
    TEMPLATE_FOLDER=Path(__file__).resolve().parents[3] / "templates",
)


async def send_email(
    email_to: str,
    feedback: str,
    llm: str,
    lang: Literal["ja", "en"],
) -> None:
    """フィードバックメール送信

    Args:
        email_to (str): 送信先メールアドレス
        feedback (str): フィードバック
        llm (str): llm名
        lang (Literal[ja", "en"]): 言語
    """

    template_name: str = f"email_{lang}.html"
    subject = "睡眠推定フィードバック" if lang == "ja" else "Sleep Estimation Feedback"

    try:
        message = MessageSchema(
            subject=subject,
            recipients=[email_to],  # type: ignore
            template_body={
                "feedback": markdown.markdown(feedback, extensions=["extra"]),
                "llm": llm,
            },
            subtype=MessageType.html,
        )
        fm = FastMail(conf)
        await fm.send_message(message, template_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
