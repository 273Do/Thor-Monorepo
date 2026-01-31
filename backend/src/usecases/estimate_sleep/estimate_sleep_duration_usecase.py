from datetime import datetime, timedelta
from typing import List

import pandas as pd
from pandera.typing import DataFrame

from src.core.constants import HOLIDAY_TIME_RANGE, WEEKDAY_TIME_RANGE
from src.schemas.estimate_sleep import EstimateGoingOutDFSchema


def estimate_sleep_duration_from_step(
    estimate_going_out_df: DataFrame[EstimateGoingOutDFSchema],
    late_night_list: List[int],
    charging_before_bed_answer: int,
    carrying_a_smartphone_answer: int,
):
    """歩数から睡眠を推定する

    Args:
        estimate_going_out_df (DataFrame[EstimateGoingOutDFSchema]): クラスタリングのラベルを追加した DataFrame
        late_night_list (List[int]): 夜ふかし検知結果の配列
        charging_before_bed_answer (int): 就寝何時間前にスマホを充電するかの回答（0 ~ 4）
        carrying_a_smartphone_answer (int): の中でスマホを持ち歩くかの回答（0 ~ 2）
    """

    # estimate_going_out_df の start_date カラムを文字列から日付型に変更
    estimate_going_out_df["start_date"] = pd.to_datetime(
        estimate_going_out_df["start_date"]
    )

    # Dataframe 内の全ての日付を抽出
    unique_dates = pd.date_range(
        start=estimate_going_out_df["start_date"].iloc[0].date(),
        end=estimate_going_out_df["start_date"].iloc[-1].date(),
    ).date

    # 1日毎に抽出処理を繰り返す
    for i, date in enumerate(unique_dates):
        # 推定処理において前日を参照する関係上、レコードの最初の日はスキップする
        if i == 0:
            continue

        # その日に夜更かしをしているかどうかを取得する
        is_late_night: bool = bool(late_night_list[i])

        # その日が平日かどうかを判定し、精査範囲を定義する
        is_weekday: bool = date.weekday() < 5
        if is_weekday:
            time_range = WEEKDAY_TIME_RANGE
        else:
            time_range = HOLIDAY_TIME_RANGE

        # 夜更かししているかどうかで推定方法が異なる
        if is_late_night:
            # 夜更かししている場合の推定処理

            # その日の歩数データを取得
            day_df: DataFrame[EstimateGoingOutDFSchema] = estimate_going_out_df[
                (estimate_going_out_df["start_date"].dt.date == date)  # type: ignore
            ].sort_values("start_date")

        else:
            # 夜更かししていない場合の推定処理

            # その日と前日の歩数データを取得
            target_dates: List[datetime] = [date - timedelta(days=1), date]
            day_df: DataFrame[EstimateGoingOutDFSchema] = estimate_going_out_df[
                estimate_going_out_df["start_date"].dt.date.isin(target_dates)  # type: ignore
            ].sort_values("start_date")

        print(f"time_range:{time_range}")
        print(f"is_late_night:{is_late_night}")
        print(day_df)
        # break

    return
