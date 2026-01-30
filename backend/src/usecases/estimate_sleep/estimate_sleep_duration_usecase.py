from typing import List

import pandas as pd
from pandera.typing import DataFrame

from src.schemas.estimate_sleep import EstimateGoingOutDFSchema


def estimate_sleep_duration_from_step(
    estimate_going_out_df: DataFrame[EstimateGoingOutDFSchema],
    late_night_list: List[int],
    charging_before_bed_answer: int,
    carrying_a_smartphone_answer: int,
):
    """歩数から睡眠を推定する"""

    # estimate_going_out_df の start_date カラムを文字列から日付型に変更
    estimate_going_out_df["start_date"] = pd.to_datetime(
        estimate_going_out_df["start_date"]
    )

    # Dataframe 内の全ての日付を抽出
    unique_dates = pd.date_range(
        start=estimate_going_out_df["start_date"].iloc[0].date(),
        end=estimate_going_out_df["start_date"].iloc[-1].date(),
    ).date

    print(unique_dates)

    return
