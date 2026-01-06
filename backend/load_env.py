from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Envs(BaseSettings):
    """環境変数を読み込む"""

    API_V1_PREFIX: str = Field(description="APIのプレフィックス", default="/api/v1")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_envs() -> Envs:
    """@lru_cacheで.envの結果をキャッシュする"""
    return Envs()
