from datetime import datetime

from .applehealthdata_usecase import HealthDataExtractor


def extract_steps_from_applehealthcare(
    xml_data: str,
    start_date_of_extract: datetime | None,
    end_date_of_extract: datetime | None,
    months_of_extract: int | None,
) -> None:
    """Apple HealthcareのXMLデータから歩数を抽出する

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
    print(extractor.records["StepCount"][:1])  # デバッグ用に最初の1件を表示
    print(extractor.records["StepCount"][-1])  # デバッグ用に最後の1件を表示

    # TODO: start_date/end_date または months_of_extract でデータをフィルタリング
    # 現在は全データを取得

    return
