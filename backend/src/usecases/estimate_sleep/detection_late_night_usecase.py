from pathlib import Path

import joblib
import pandas as pd

from src.core.load_env import envs
from src.schemas.estimate_sleep import DailyStats, LateNightFeature


def detect_late_night(feature: LateNightFeature):
    """その日が夜更かしをしているかどうかを機械学習モデルから推定"""

    # 特徴量を DataFrame に変換
    feature_df = pd.DataFrame(
        [_daily_stats_to_flat_dict(daily) for daily in feature.feature]
    )

    print(feature_df)

    # 全てのモデルを取得
    models_dir = Path(f"/workspace/backend/{envs.MODELS_DIR}")

    models_path = list(models_dir.glob("*.pkl"))

    # 各モデルで予測を実行
    predictions = []
    for path in models_path:
        # モデルをロード
        model = joblib.load(path)  # type: ignore

        # ロードしたモデルで予測
        pred = model.predict(feature_df.drop("date", axis=1))

        # 予測結果を格納
        predictions.append(pred)  # type: ignore
        print(path, pred)

    # 最終予測結果の集計(アンサンブル学習 / 投票ベース)
    # 予測結果を多数決で決定(各モデルの予測結果の平均値を取り，四捨五入)

    print(predictions)  # type: ignore
    return


def _daily_stats_to_flat_dict(daily_stats: DailyStats) -> dict:  # type: ignore
    """DailyStats を1行のレコード用にフラット化し、モデルに合わせてカラム名を変更"""

    row = {
        "date": daily_stats.date,
    }

    # hourly_statisticsをフラットに展開
    for stat in daily_stats.hourly_statistics:
        # model に合わせてカラム名を変更する
        suffix = stat.hour_range.replace("to", "_")

        row[f"sumValue_{suffix}"] = stat.total_steps  # type: ignore
        row[f"valueCount_{suffix}"] = stat.records  # type: ignore

    row["habit"] = daily_stats.bedtime_answer  # type: ignore

    return row
