from datetime import datetime, timedelta
from typing import Any, List

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

    # estimate_going_out_df の start_date とend_date カラムを文字列から日付型に変更
    estimate_going_out_df["start_date"] = pd.to_datetime(
        estimate_going_out_df["start_date"]
    )
    estimate_going_out_df["end_date"] = pd.to_datetime(
        estimate_going_out_df["end_date"]
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

        print(f"{date}==============")

        # 夜更かししているかどうかで推定方法が異なる
        if is_late_night:
            # 夜更かししている場合の推定処理

            # その日の歩数データを start_date で整列して取得
            day_df: DataFrame[EstimateGoingOutDFSchema] = estimate_going_out_df[  # type: ignore
                (estimate_going_out_df["start_date"].dt.date == date)  # type: ignore
            ].sort_values("start_date")

            # 推定処理を実行
            sleep_time_range = _late_night_estimate(day_df, time_range)

            print(f"sleep_time_range:{sleep_time_range}")

        else:
            # 夜更かししていない場合の推定処理

            # その日と前日の歩数データを start_date で整列して取得
            target_dates: List[datetime] = [date - timedelta(days=1), date]
            day_df: DataFrame[EstimateGoingOutDFSchema] = estimate_going_out_df[  # type: ignore
                estimate_going_out_df["start_date"].dt.date.isin(target_dates)  # type: ignore
            ].sort_values("start_date")

            # 推定処理を実行
            _normal_estimate(day_df, time_range)

        # break

    return


def _late_night_estimate(
    day_df: DataFrame[EstimateGoingOutDFSchema], time_range: list[str]
) -> List[Any]:
    """夜更かししている場合の推定処理\n
    0000->0300にレコードがあればそこを、なければ0300を精査開始時間とし、そこから2100までの歩数レコード間隔が最も長い時間を就寝/起床時刻とする。

    Args:
        day_df (DataFrame[EstimateGoingOutDFSchema]): 日々の歩数 DataFrame
        time_range (list[str]): 精査範囲
    Returns:
        List[Any]: 日々の推定睡眠時間範囲 [就寝時刻, 起床時刻]
    """

    # 精査するデータの時間範囲の指定
    initial_time = pd.to_datetime("00:00:00").time()
    start_time = pd.to_datetime(f"{time_range[0]}:00").time()
    end_time = pd.to_datetime(f"{time_range[3]}:00").time()

    # 精査初期値は、3時より前を見て最初に観測されたステップの end_date とする
    # なければ3時を初期値とする
    initial_time_df: DataFrame[EstimateGoingOutDFSchema] = day_df[
        (day_df["end_date"].dt.time >= initial_time)
        & (day_df["end_date"].dt.time <= start_time)
    ]
    if not initial_time_df.empty:
        start_time = initial_time_df["end_date"].max().time()

    # 精査範囲でデータを絞る
    filtered_df: DataFrame[EstimateGoingOutDFSchema] = day_df[
        (day_df["end_date"].dt.time >= start_time)
        & (day_df["start_date"].dt.time <= end_time)
    ]

    # データが無い場合は終了
    if filtered_df.empty:
        return []

    # 最大の睡眠時間と、その時の就寝・起床時刻を記録する変数
    max_sleep_duration = timedelta()
    sleep_time_range: List[Any] = []

    # 前のレコードの終了時刻（初期時刻は精査開始時刻）
    prev_start_time = start_time

    # その日の歩数データごとに処理を繰り返す
    for row in filtered_df.itertuples():
        # 現在のレコードの終了・開始時刻をそれぞれ間隔の開始・終了時刻とする取得
        current_start_time = row.end_date.time()
        current_end_time = row.start_date.time()

        # 終了時刻が初期開始時刻より小さい場合はスキップ（複数端末への対応）
        if prev_start_time > current_end_time:
            continue

        # 前のレコードの終了時刻と現在のレコードの開始時刻の差（睡眠時間）を計算
        prev_start_datetime = datetime.combine(datetime.today(), prev_start_time)
        current_end_datetime = datetime.combine(datetime.today(), current_end_time)
        sleep_duration = current_end_datetime - prev_start_datetime

        # 現在の睡眠時間が最大より大きい場合は更新
        if sleep_duration > max_sleep_duration:
            max_sleep_duration = sleep_duration

            # 開始時刻と終了時刻を記録
            sleep_time_range = [prev_start_datetime.time(), current_end_datetime.time()]

        # 終了時刻を更新
        prev_start_time = current_start_time

        # TODO: 外出検知の場合はスキップ(1,2クラスタ)

    # 睡眠時間が見つからなかった場合は空リストを返す
    if not sleep_time_range:
        return []

    return sleep_time_range


def _normal_estimate(
    day_df: DataFrame[EstimateGoingOutDFSchema], time_range: List[str]
) -> List[Any]:
    """夜更かししていない場合の推定処理\n
    2500->2100、0415->1200を遡って最初に観測された歩数レコードを就寝・起床時刻とする。


    Args:
        day_df (DataFrame[EstimateGoingOutDFSchema]): 日々の歩数 DataFrame
        time_range (list[str]): 精査範囲

    Returns:
        List[Any]: 日々の推定睡眠時間範囲 [就寝時刻, 起床時刻]
    """

    # 前日，当日の取得
    unique_dates = day_df["start_date"].dt.date.unique()

    # データが無い場合は空の配列を返す
    if len(unique_dates) < 2:
        return []

    # 精査するデータの時間範囲の指定
    bed_end = pd.to_datetime(f"{time_range[0]}:00").time()
    wake_start = pd.to_datetime(f"{time_range[1]}:00").time()
    wake_end = pd.to_datetime(f"{time_range[2]}:00").time()
    bed_start = pd.to_datetime(f"{time_range[3]}:00").time()

    # 就寝時刻は前日から当日のデータを精査する
    bed_start_time = pd.Timestamp(f"{unique_dates[0].isoformat()} {bed_start}+09:00")
    bed_end_time = pd.Timestamp(f"{unique_dates[1].isoformat()} {bed_end}+09:00")
    bed_df = day_df[day_df["start_date"].between(bed_start_time, bed_end_time)]

    # 起床時刻は当日のデータから精査する
    wake_start_time = pd.Timestamp(f"{unique_dates[1].isoformat()} {wake_start}+09:00")
    wake_end_time = pd.Timestamp(f"{unique_dates[1].isoformat()} {wake_end}+09:00")
    wake_df = day_df[day_df["start_date"].between(wake_start_time, wake_end_time)]

    # 就寝時刻の推定
    if bed_df.empty:
        bed_time = bed_end
    else:
        bed_time = bed_df["end_date"].max().time()

    # 起床時刻の推定
    if wake_df.empty:
        wake_time = wake_start
    else:
        wake_time = wake_df["start_date"].min().time()

    print([bed_time, wake_time])

    return [bed_time, wake_time]
