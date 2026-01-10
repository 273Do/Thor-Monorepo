"""環境変数のロードモジュール"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Envs(BaseSettings):
    """環境変数の管理"""

    API_V1_PREFIX: str = Field(default="/api/v1")
    """APIの接頭辞"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_envs() -> Envs:
    """@lru_cacheで.envの結果をキャッシュする

    Returns:
        Envs: 環境変数のクラス
    """

    return Envs()
