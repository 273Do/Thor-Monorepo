from datetime import datetime

from src.core.constants import SLEEP_ANALYSIS_CSV_FILENAME, STEP_COUNT_CSV_FILENAME
from src.core.load_env import envs
from src.schemas.extract_steps import ExtractedSteps, SleepRecord, StepRecord

from .applehealthdata_usecase import HealthDataExtractor


def extract_steps_from_applehealthcare(
    xml_data: str,
    start_date_of_extract: datetime | None,
    end_date_of_extract: datetime | None,
    months_of_extract: int | None,
    include_recorded_sleep: bool | None,
) -> ExtractedSteps:
    """抽出期間か範囲を指定してApple HealthcareのXMLデータから歩数を抽出する

    Args:
        xml_data (str): Apple HealthcareのXMLデータ
        start_date_of_extract (datetime | None): 解析開始日
        end_date_of_extract (datetime | None): 解析終了日
        months_of_extract (int | None): 最新の日付から遡って抽出する月数
        include_recorded_sleep (bool | None): 記録された睡眠データを含めるかどうか

    Returns:
        dict: 抽出結果
    """

    # xml文字列をHealthDataExtractorに直接渡す
    extractor = HealthDataExtractor(
        xml_data,
        start_date_of_extract,
        end_date_of_extract,
        months_of_extract,
        include_recorded_sleep,
        verbose=False,
    )
    extractor.extract()

    dataframes = extractor.get_dataframes()

    step_count_df = dataframes.get("StepCount")

    # startDate, endDateをstr型に変換
    if step_count_df is not None:
        step_count_df["startDate"] = step_count_df["startDate"].astype(str)
        step_count_df["endDate"] = step_count_df["endDate"].astype(str)
        step_count_df["value"] = step_count_df["value"].astype(str)

    sleep_analysis_df = dataframes.get("SleepAnalysis")

    if sleep_analysis_df is not None:
        sleep_analysis_df["startDate"] = sleep_analysis_df["startDate"].astype(str)
        sleep_analysis_df["endDate"] = sleep_analysis_df["endDate"].astype(str)
        sleep_analysis_df["value"] = sleep_analysis_df["value"].astype(str)

    # データから識別用のIDを生成
    timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
    data_id: str = extractor.generate_data_id()

    step_count_records: list[StepRecord] = step_count_df.to_dict(orient="records")  # type: ignore

    sleep_analysis_records: list[SleepRecord] = sleep_analysis_df.to_dict(  # type: ignore
        orient="records"
    )

    # デバッグ用時は抽出したデータをCSVとして保存
    if envs.IS_DEBUG:
        if step_count_df is not None:
            step_count_df.to_csv(
                f"{envs.SAMPLE_DATA_DIR}/{STEP_COUNT_CSV_FILENAME}",
                index=False,
            )

        if sleep_analysis_df is not None:
            sleep_analysis_df.to_csv(
                f"{envs.SAMPLE_DATA_DIR}/{SLEEP_ANALYSIS_CSV_FILENAME}", index=False
            )

    return ExtractedSteps(
        id=data_id + "_" + timestamp,
        stepData=step_count_records,
        sleepData=sleep_analysis_records,
    )
