from datetime import datetime

from .applehealthdata_usecase import HealthDataExtractor


def extract_steps_from_applehealthcare(
    xml_data: str,
    start_date_of_extract: datetime | None,
    end_date_of_extract: datetime | None,
    months_of_extract: int | None,
) -> None:
    """抽出期間か範囲を指定してApple HealthcareのXMLデータから歩数を抽出する

    Args:
        xml_data (str): Apple HealthcareのXMLデータ
        start_date_of_extract (datetime | None): 解析開始日
        end_date_of_extract (datetime | None): 解析終了日
        months_of_extract (int | None): 最新の日付から遡って抽出する月数

    Returns:
        dict: 抽出結果
    """

    # xml文字列をHealthDataExtractorに直接渡す
    extractor = HealthDataExtractor(
        xml_data,
        start_date_of_extract,
        end_date_of_extract,
        months_of_extract,
        verbose=False,
    )
    extractor.extract()

    dataframes = extractor.get_dataframes()
    step_count_df = dataframes.get("StepCount")

    if step_count_df is not None and not step_count_df.empty:
        if "startDate" in step_count_df.columns:
            actual_start_date = step_count_df["startDate"]
            print(actual_start_date)
        if "endDate" in step_count_df.columns:
            actual_end_date = step_count_df["endDate"]
            print(actual_end_date)

    return
