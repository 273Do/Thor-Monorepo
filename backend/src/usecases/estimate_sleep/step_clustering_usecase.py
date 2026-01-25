from typing import List, Tuple

import pandas as pd
from pandera.typing import DataFrame
from sklearn.cluster import KMeans

from src.core.constants import STEP_COUNT_CSV_FILENAME
from src.core.load_env import envs
from src.schemas.estimate_sleep import (
    EstimateGoingOutDFSchema,
    StepClusterRecord,
    StepClusters,
)
from src.schemas.extract_steps import StepCountDFSchema


def step_clustering(
    step_count_df: DataFrame[StepCountDFSchema],
) -> Tuple[DataFrame[EstimateGoingOutDFSchema], StepClusters]:
    """外出検知のため1分あたりの歩数を計算しクラスタリングを行う

    Args:
        step_count_df (DataFrame[StepCountDFSchema]): 歩数データの DataFrame

    Returns:
        Tuple[DataFrame[EstimateGoingOutDFSchema], StepClusters]:
        クラスタリングのラベルを追加した DataFrame,
        クラスタリング結果のラベルとセントロイド
    """

    # start_date と end_date を datetime に変換
    start_times = pd.to_datetime(step_count_df["start_date"])
    end_times = pd.to_datetime(step_count_df["end_date"])

    # 時間差を計算（分単位）
    duration_minutes = (end_times - start_times).dt.total_seconds() / 60

    # 1分あたりの歩数を計算
    steps_per_minute = step_count_df["value"] / duration_minutes

    step_count_df["steps_per_minute"] = round(steps_per_minute)

    # value カラムのみを抽出（クラスタリング用）
    # value_df = step_count_df[["value"]]

    # 1分あたりの歩数をクラスタリング
    kmeans = KMeans(
        n_clusters=3,  # クラスター数
        random_state=42,  # セントロイドの初期化
    ).fit(step_count_df[["steps_per_minute"]])  # 学習
    # ).fit(value_df)  # 学習

    # クラスタリング結果を取得
    labels = kmeans.labels_

    # セントロイドを取得
    centroids: Tuple[float, float, float] = kmeans.cluster_centers_.flatten().tolist()

    # セントロイドを値が小さい順に並び替え、インデックスを取得
    sorted_centroids_index: List[int] = sorted(
        range(len(centroids)), key=lambda i: centroids[i]
    )

    # クラスタ番号を再マッピングする辞書を作成 {元のクラスタ番号：新しいクラスタ番号}
    remap_clusters_dict: dict[int, int] = {
        old: new for new, old in enumerate(sorted_centroids_index)
    }

    # labels の各値を remap_clusters_dict でマッピング
    remapped_labels: List[int] = [
        remap_clusters_dict[label] for label in labels.tolist()
    ]

    # クラスターデータを作成
    cluster_list: List[StepClusterRecord] = []

    for cluster in sorted_centroids_index:
        cluster_data = StepClusterRecord(
            cluster_label=remap_clusters_dict[cluster],
            centroid=round(centroids[cluster], 2),
        )

        cluster_list.append(cluster_data)

    cluster_stats: Tuple[StepClusterRecord, StepClusterRecord, StepClusterRecord] = (
        tuple(cluster_list)
    )  # type: ignore

    # 睡眠状態を推定するためのDataFrameを作成
    estimate_going_out_df: DataFrame[EstimateGoingOutDFSchema] = step_count_df.copy()  # type: ignore
    estimate_going_out_df["cluster_label"] = remapped_labels

    return (estimate_going_out_df, StepClusters(clusters=cluster_stats))


# デモ実行
# task backend -- uv run python -m src.usecases.estimate_sleep.step_clustering_usecase
if __name__ == "__main__":
    demo_df: DataFrame[StepCountDFSchema] = pd.read_csv(  # type: ignore
        f"/workspace/backend/{envs.SAMPLE_DATA_DIR}/{STEP_COUNT_CSV_FILENAME}"
    )

    # クラスタリング実行
    step_clustering(demo_df)
