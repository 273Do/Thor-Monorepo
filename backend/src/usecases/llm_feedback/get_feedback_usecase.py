import json
from pathlib import Path
from typing import List, Literal, Tuple

from openai import OpenAI

from src.core.constants import FAILED_GENERATE_FEEDBACK
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
    is_specialized: bool,
) -> str:
    """推定睡眠データを使用して LLM からフィードバックを取得する

    Args:
        data (List[StepCountRecord] | List[DailyEstimateSleepRecord]): 推定睡眠データ
        clusters (Tuple[StepClusterRecord, StepClusterRecord, StepClusterRecord]): 歩数クラスターデータ(未使用だがいつでも使用できるように)
        llm (str): llm名
        lang (Literal[ja", "en"]): 言語
        is_specialized (bool): 専門的なフィードバックを返すかどうか(プロンプト選択)

    Returns:
        str: LLM から得たフィードバック
    """

    system_prompt = _load_system_prompt(lang, is_specialized)

    completion = client.chat.completions.create(
        model=llm,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": _format_llm_input(estimate_sleep_json),
            },
        ],
    )

    feedback: str = completion.choices[0].message.content or FAILED_GENERATE_FEEDBACK

    return _strip_code_fence(feedback)


def _format_llm_input(records: List[DailyEstimateSleepRecord]) -> str:
    """睡眠推定データを LLM 向けに最小構成文字列へ変換する

    Returns:
        str: {"YYYY-MM-DD": ["bed_time", "wake_time"]} 形式の JSON 文字列
    """
    formatted = {
        r["date"][:10]: [r["bed_time"], r["wake_time"]]  # type: ignore
        for r in records
    }

    return json.dumps(formatted, ensure_ascii=False)


def _strip_code_fence(text: str) -> str:
    """LLMの出力からマークダウンのコードフェンスを除去する

    Args:
        text (str): LLMの出力テキスト

    Returns:
        str: コードフェンスを除去したテキスト
    """
    import re

    return re.sub(r"^```(?:markdown|md)?\n?", "", re.sub(r"\n?```\s*$", "", text))


def _load_system_prompt(lang: Literal["ja", "en"], is_specialized: bool) -> str:
    """言語に応じたシステムプロンプトをファイルから読み込む

    Args:
        lang (Literal[ja", "en"]): 言語
        is_specialized (bool): 専門的なフィードバックを返すかどうか(プロンプト選択)

    Returns:
        str: prompt テキスト
    """

    prompt_filename = f"{'specialized-' if is_specialized else ''}prompt-{lang}.md"
    prompt_path = Path(envs.DATASTORE_DIR) / f"prompts/{prompt_filename}"

    return prompt_path.read_text(encoding="utf-8")
