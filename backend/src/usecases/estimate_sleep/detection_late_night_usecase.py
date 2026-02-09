from pathlib import Path
from typing import List

import joblib
import pandas as pd

from src.core.load_env import envs
from src.schemas.estimate_sleep import DailyStats, LateNightFeature


def detect_late_night(feature: LateNightFeature) -> List[int]:
    """その日が夜更かしをしているかどうかを機械学習モデルから推定

    Args:
        feature (LateNightFeature): 歩数データから夜更かしを推定するための特徴量

    Returns:
        List[int]: 夜ふかし検知結果の配列
    """

    # 特徴量を DataFrame に変換
    feature_df = pd.DataFrame(
        [_daily_stats_to_flat_dict(daily) for daily in feature.feature]
    )

    # 全てのモデルのパスを取得
    models_dir = Path(f"/workspace/backend/{envs.MODELS_DIR}")

    models_path = list(models_dir.glob("*.pkl"))

    # 各モデルで予測を実行
    predictions: List[List[int]] = []
    for path in models_path:
        # モデルをロード
        model = joblib.load(path)

        # ロードしたモデルで予測
        pred: List[int] = model.predict(feature_df.drop("date", axis=1))

        # 予測結果を格納
        predictions.append(pred)

    # 最終予測結果の集計(アンサンブル学習 / 投票ベース)
    # 予測結果を多数決で決定
    late_night_list: List[int] = []
    for i in range(len(feature_df)):
        # 各モデルの i 行目の予測を収集
        votes = [pred[i] for pred in predictions]

        # 最も多くのモデルが予測したクラスを最終予測とする
        majority_vote = max(set(votes), key=votes.count)

        late_night_list.append(majority_vote)

    return late_night_list


def _daily_stats_to_flat_dict(daily_stats: DailyStats) -> dict:
    """DailyStats を1行のレコード用にフラット化し、モデルに合わせてカラム名を変更

    Args:
        daily_stats (DailyStats): 日付ごとの歩数の統計

    Returns:
        dict: 辞書型に変換された日付ごとの歩数の統計
    """

    row = {
        "date": daily_stats.date,
    }

    # hourly_statisticsをフラットに展開
    for stat in daily_stats.hourly_statistics:
        # model に合わせてカラム名を変更する
        suffix = stat.hour_range.replace("to", "_")

        row[f"sumValue_{suffix}"] = stat.total_steps
        row[f"valueCount_{suffix}"] = stat.records

    row["habit"] = daily_stats.bedtime_answer

    return row
