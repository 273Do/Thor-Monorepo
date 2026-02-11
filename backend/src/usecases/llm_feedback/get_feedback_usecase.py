import json
from typing import List

from openai import OpenAI

from src.core.load_env import envs
from src.schemas.estimate_sleep import DailyEstimateSleepRecord
from src.schemas.extract_steps import StepCountRecord

client = OpenAI(
    base_url=str(envs.OLLAMA_ENDPOINT),
    api_key="ollama",
)


def get_feedback(data: List[StepCountRecord] | List[DailyEstimateSleepRecord]) -> str:
    completion = client.chat.completions.create(
        # TODO: モデルやsystem promptは別で設定するようにする
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": "You are an expert on the health, lifestyle, and sleep habits of university students, and also have knowledge of mental health. The data you will be providing is data on daily sleep duration estimated from step count data. Please provide detailed feedback and advice on what you can learn from this information, areas for improvement, and lifestyle habits.",
            },
            {
                "role": "user",
                "content": json.dumps(data, ensure_ascii=False),
            },
        ],
    )

    feedback: str = completion.choices[0].message.content

    return feedback
