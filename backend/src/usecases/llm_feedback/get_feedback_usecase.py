import json
from pathlib import Path
from typing import List, Literal, Tuple

from openai import OpenAI

from src.core.load_env import envs
from src.schemas.estimate_sleep import DailyEstimateSleepRecord, StepClusterRecord

client = OpenAI(
    base_url=str(envs.OLLAMA_ENDPOINT),
    api_key="ollama",
)


def get_feedback(
    estimate_sleep_json: List[DailyEstimateSleepRecord],
    clusters: Tuple[StepClusterRecord, StepClusterRecord, StepClusterRecord],
    lang: Literal["ja", "en"],
) -> str:
    """推定睡眠データを使用して LLM からフィードバックを取得する

    Args:
        data (List[StepCountRecord] | List[DailyEstimateSleepRecord]): 推定睡眠データ
        clusters (Tuple[StepClusterRecord, StepClusterRecord, StepClusterRecord]): 歩数クラスターデータ
        lang (Literal[ja", "en"]): 言語

    Returns:
        str: LLM から得たフィードバック
    """

    system_prompt = _load_system_prompt(lang)

    completion = client.chat.completions.create(
        # TODO: モデルは別で設定するようにする
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": json.dumps(clusters, ensure_ascii=False),
            },
            {
                "role": "user",
                "content": json.dumps(estimate_sleep_json, ensure_ascii=False),
            },
        ],
    )

    feedback: str = completion.choices[0].message.content

    return feedback


def _load_system_prompt(lang: Literal["ja", "en"]) -> str:
    """言語に応じたシステムプロンプトをファイルから読み込む

    Args:
        lang (Literal[ja", "en"]): 言語

    Returns:
        str: prompt テキスト
    """

    prompt_path = Path(envs.SAMPLE_DATA_DIR) / f"prompt-{lang}.md"
    return prompt_path.read_text(encoding="utf-8")
