from datetime import datetime
from typing import List

from pandera.typing import DataFrame

from src.core.constants import SLEEP_ANALYSIS_CSV_FILENAME, STEP_COUNT_CSV_FILENAME
from src.core.load_env import envs
from src.schemas.extract_steps import (
    ExtractedSteps,
    SleepAnalysisDFSchema,
    SleepAnalysisRecord,
    StepCountDFSchema,
    StepCountRecord,
)

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
        ExtractedSteps: 抽出された歩数データと睡眠データ
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

    dataframes: dict[
        str, DataFrame[StepCountDFSchema] | DataFrame[SleepAnalysisRecord]
    ] = extractor.get_dataframes()  # type: ignore

    step_count_df: DataFrame[StepCountDFSchema] | None = dataframes.get("StepCount")  # type: ignore

    sleep_analysis_df: DataFrame[SleepAnalysisDFSchema] | None = dataframes.get(
        "SleepAnalysis"
    )  # type: ignore

    # データから識別用のIDを生成
    timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
    data_id: str = extractor.generate_data_id()

    step_count_records: List[StepCountRecord] = step_count_df.to_dict(orient="records")  # type: ignore

    sleep_analysis_records: List[SleepAnalysisRecord] = sleep_analysis_df.to_dict(  # type: ignore
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
        step_data=step_count_records,
        sleep_data=sleep_analysis_records,
    )
