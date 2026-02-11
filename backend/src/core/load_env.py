"""環境変数のロードモジュール"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Envs(BaseSettings):
    """環境変数の管理"""

    IS_DEBUG: bool = Field(default=False)
    """デバッグモードの有効化フラグ"""

    DATASTORE_DIR: str = Field(default="./datastore")
    """データを格納するディレクトリパス"""

    SAMPLE_DATA_DIR: str = Field(default="./datastore/sample_data")
    """サンプルデータを格納するディレクトリパス"""

    MODELS_DIR: str = Field(default="./datastore/models")
    """modelを格納しているディレクトリパス"""

    STATISTICAL_DATA_DIR: str = Field(default="./datastore/statistical_data")
    """統計データを格納しているディレクトリパス"""

    VAULT_DIR: str = Field(default="./datastore/vault")
    """歩数データや推定結果を格納しているディレクトリパス"""

    API_V1_PREFIX: str = Field(default="/api/v1")
    """APIの接頭辞"""

    DATA_ID_SALT: str = Field()
    """識別id生成用のソルト"""

    OLLAMA_ENDPOINT: str = Field(default="http://host.docker.internal:11434/v1/")
    """ollamaのエンドポイント"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    def __init__(
        self,
    ) -> None:
        """型エラー防止のために明示的にコンストラクタを上書き"""
        super().__init__()


@lru_cache
def get_envs() -> Envs:
    """@lru_cacheで.envの結果をキャッシュする

    Returns:
        Envs: 環境変数のクラス
    """

    return Envs()


envs = get_envs()
