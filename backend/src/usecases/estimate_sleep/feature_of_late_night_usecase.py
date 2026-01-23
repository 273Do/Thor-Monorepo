from typing import List

import pandas as pd
from pandera.typing import DataFrame

from src.core.constants import FEATURE_TIME_RANGE, STEP_COUNT_CSV_FILENAME
from src.core.load_env import envs
from src.schemas.estimate_sleep import DailyStats, HourlyStats, LateNightFeature
from src.schemas.extract_steps import StepCountDFSchema


def create_feature_value(
    step_count_df: DataFrame[StepCountDFSchema], bedtime_answer: int
) -> LateNightFeature:
    """歩数データから夜更かしを推定するための特徴量を作成する\n
    0時~12時から1時間毎のレコード数と歩数データの合計、アンケートによる普段の就寝時刻(3時より以前0, 以降1)を特徴量とする

    Args:
        step_count_df (DataFrame[StepCountDFSchema]): 歩数データの DataFrame
        bedtime_answer (int): 就寝時間の回答

    Returns:
        LateNightFeature: 夜更かし推定のための特徴量
    """

    # step_count_df の start_date カラムを文字列から日付型に変更
    step_count_df["start_date"] = pd.to_datetime(step_count_df["start_date"])

    # Dataframe 内の全ての日付を抽出
    unique_dates = pd.date_range(
        start=step_count_df["start_date"].iloc[0].date(),
        end=step_count_df["start_date"].iloc[-1].date(),
    ).date

    # 特徴量となるデータの時間範囲の指定
    start, end = FEATURE_TIME_RANGE

    # 特徴量(日付ごとの歩数データの統計)を保存するためのリスト
    feature: List[DailyStats] = []

    # 1日毎に抽出処理を繰り返す
    for date in unique_dates:
        # 指定の日付でデータを絞る
        date_df = step_count_df[step_count_df["start_date"].dt.date == date]  # type: ignore

        # その日の1時間ごとの歩数データの統計を格納する配列
        hourly_statistics: List[HourlyStats] = []

        # 1時間毎に抽出処理を繰り返す
        for hour in range(start, end):
            # 時間型で時間範囲を定義
            start_time = pd.to_datetime(f"{hour}:00")
            end_time = pd.to_datetime(f"{hour + 1}:00")

            hour_range: str = f"{hour}to{hour + 1}"

            # 指定の時間範囲でデータを絞る
            hour_df = date_df[  # type: ignore
                (date_df["start_date"].dt.time >= start_time.time())  # type: ignore
                & (date_df["start_date"].dt.time <= end_time.time())  # type: ignore
            ]

            # 1時間毎の歩数の合計とデータ数を取得
            total_steps: int = hour_df["value"].sum()  # type: ignore
            records: int = hour_df.shape[0]  # type: ignore

            # 1時間毎の歩数データの統計を作成
            hourly_stats = HourlyStats(
                hour_range=hour_range,
                total_steps=total_steps,  # type: ignore
                records=records,  # type: ignore
            )

            hourly_statistics.append(hourly_stats)

        # その日の歩数データの統計を作成
        daily_stats = DailyStats(
            date=date,
            hourly_statistics=hourly_statistics,
            bedtime_answer=bedtime_answer,
        )

        feature.append(daily_stats)

    print(feature)

    return LateNightFeature(feature=feature)


# TODO: 特徴量を DataFrame に変換する処理を記述する

# デモ実行
# task backend -- uv run python -m src.usecases.estimate_sleep.feature_of_late_night
if __name__ == "__main__":
    demo_df: DataFrame[StepCountDFSchema] = pd.read_csv(  # type: ignore
        f"/workspace/backend/{envs.SAMPLE_DATA_DIR}/{STEP_COUNT_CSV_FILENAME}"
    )

    # クラスタリング実行
    create_feature_value(demo_df, 1)
