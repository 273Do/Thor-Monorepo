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
    llm: str,
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
        model=llm,
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

    return _strip_code_fence(feedback)


def _strip_code_fence(text: str) -> str:
    """LLMの出力からマークダウンのコードフェンスを除去する

    Args:
        text (str): LLMの出力テキスト

    Returns:
        str: コードフェンスを除去したテキスト
    """
    import re

    return re.sub(r"^```(?:markdown|md)?\n?", "", re.sub(r"\n?```\s*$", "", text))


def _load_system_prompt(lang: Literal["ja", "en"]) -> str:
    """言語に応じたシステムプロンプトをファイルから読み込む

    Args:
        lang (Literal[ja", "en"]): 言語

    Returns:
        str: prompt テキスト
    """

    prompt_path = Path(envs.SAMPLE_DATA_DIR) / f"prompt-{lang}.md"
    return prompt_path.read_text(encoding="utf-8")
