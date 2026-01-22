# -*- coding: utf-8 -*-
"""
applehealthdata.py: Extract data from Apple Health App"s export.xml.

Copyright (c) 2016 Nicholas J. Radcliffe
Licence: MIT

===Modifications===

Copyright (c) 2026 273*

This software includes modifications made by 273* to the original software licensed under the MIT License.
Modified portions of this software are that I changed some columns to extract only StepCount and SleepAnalysis and store them in a DataFrame.

Licence: MIT
"""

import hashlib
import re
from collections import Counter, OrderedDict
from collections.abc import Mapping
from datetime import datetime
from typing import List, Literal
from xml.etree import ElementTree

import pandas as pd
import pandera as pa
from dateutil.relativedelta import relativedelta
from pandera.typing import DataFrame

from src.core.constants import DEVICE_FILTER, SLEEP_ANALYSIS_IN_BED, WATCHOS_MIN_VERSION
from src.core.load_env import envs
from src.schemas.extract_steps import (
    SleepAnalysisDFSchema,
    StepCountDFSchema,
)


class HealthDataExtractor:
    def __init__(
        self,
        xml_data: str,
        start_date_of_extract: datetime | None,
        end_date_of_extract: datetime | None,
        months_of_extract: int | None,
        include_recorded_sleep: bool | None,
        verbose: bool = True,
    ):
        self.verbose: bool = verbose
        self.start_date_of_extract: datetime | None = start_date_of_extract
        self.end_date_of_extract: datetime | None = end_date_of_extract
        self.months_of_extract: int | None = months_of_extract
        self.include_recorded_sleep: bool | None = include_recorded_sleep

        """入力されたデータを一意に識別するためのID"""

        self.records: dict[str, List[dict[str, str]]] = {
            "StepCount": [],
            "SleepAnalysis": [],
        }

        # 文字列を読み込んでXMLを解析
        self.root = ElementTree.fromstring(xml_data)

        self.nodes = list(self.root)

        self.abbreviate_types()
        self.collect_stats()

    def count_tags_and_fields(self) -> None:
        self.tags: Counter[str] = Counter()
        self.fields: Counter[str] = Counter()
        for record in self.nodes:
            self.tags[record.tag] += 1
            for k in record.keys():
                self.fields[k] += 1

    def count_record_types(self) -> None:
        self.record_types: Counter[str] = Counter()
        self.other_types: Counter[str] = Counter()
        for record in self.nodes:
            if record.tag == "Record":
                self.record_types[record.attrib["type"]] += 1
            elif record.tag in ("ActivitySummary", "Workout"):
                self.other_types[record.tag] += 1

    def collect_stats(self) -> None:
        self.count_record_types()
        self.count_tags_and_fields()

    def _is_in_date_range(self, date_str: str | None) -> bool:
        """レコードが指定された日付範囲内かチェック"""
        if not date_str:
            return True

        # start_dateとend_dateが両方Noneの場合は全て含める
        if self.start_date_of_extract is None and self.end_date_of_extract is None:
            return True

        try:
            record_date = datetime.fromisoformat(date_str.replace(" +", "+"))
            # タイムゾーン情報を削除してnaive datetimeに変換
            record_date = record_date.replace(tzinfo=None)
        except (ValueError, AttributeError):
            return False

        # 範囲チェック
        if (
            self.start_date_of_extract
            and record_date < self.start_date_of_extract.replace(tzinfo=None)
        ):
            return False
        if self.end_date_of_extract and record_date > self.end_date_of_extract.replace(
            tzinfo=None
        ):
            return False

        return True

    def _filter_by_months(self) -> None:
        """months_of_extractに基づいてDataFrameをフィルタリング"""
        for kind in ["StepCount", "SleepAnalysis"]:
            df = self.dataframes[kind]

            # DataFrameが空の場合はスキップ
            if df.empty:
                continue

            # end_dateカラムをdatetimeに変換
            df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")

            # 最後の日付を取得
            last_date: datetime = df["end_date"].max()

            if pd.notna(last_date) and self.months_of_extract is not None:
                # nヶ月前を計算
                start_date: datetime = last_date - relativedelta(  # type: ignore
                    months=self.months_of_extract
                )

                # フィルタリング
                filtered_df = df[
                    (pd.to_datetime(df["start_date"], errors="coerce") >= start_date)
                    & (pd.to_datetime(df["start_date"], errors="coerce") <= last_date)
                ]

                # フィルタリング後、start_dateとend_dateを文字列に戻す
                filtered_df["start_date"] = filtered_df["start_date"].astype(str)
                filtered_df["end_date"] = filtered_df["end_date"].astype(str)

                self.dataframes[kind] = filtered_df

    def abbreviate_types(self) -> None:
        for node in self.nodes:
            if node.tag == "Record" and "type" in node.attrib:
                node.attrib["type"] = _abbreviate(node.attrib["type"])

    def get_first_record(self) -> dict[str, str] | None:
        """絞り込み前の最初のレコードを取得する

        Returns:
            最初のレコードの属性辞書、見つからない場合はNone
        """
        target_kinds = ["StepCount"]

        kinds = FIELDS.keys()

        for node in self.nodes:
            if node.tag in kinds:
                attributes = node.attrib
                kind = attributes["type"] if node.tag == "Record" else node.tag

                target = _abbreviate(kind)
                if target not in target_kinds:
                    continue

                # 最初にマッチしたレコードをそのまま返す
                return dict(attributes)

        return None

    def write_records(self) -> None:
        target_kinds = ["StepCount"]

        if self.include_recorded_sleep:
            target_kinds.append("SleepAnalysis")

        kinds = FIELDS.keys()

        for node in self.nodes:
            if node.tag in kinds:
                attributes = node.attrib
                kind = attributes["type"] if node.tag == "Record" else node.tag

                target = _abbreviate(kind)
                if target not in target_kinds:
                    continue

                # months_of_extractが指定されている場合は日付範囲チェックをスキップ
                # 最後にDataFrameからフィルタリング
                if self.months_of_extract is None:
                    if not self._is_in_date_range(attributes.get("startDate")):
                        continue

                # 必要な項目を絞り込み
                if target == target_kinds[0]:
                    # 歩数データを抽出
                    if (
                        "device" not in attributes
                        or DEVICE_FILTER not in attributes["device"]
                    ):
                        continue
                elif target == target_kinds[1]:
                    # 睡眠データを抽出
                    # 指定のWatchOS以降のデータのみを抽出
                    if (
                        "sourceVersion" not in attributes
                        or str(WATCHOS_MIN_VERSION) not in attributes["sourceVersion"]
                        or attributes["value"] != SLEEP_ANALYSIS_IN_BED
                    ):
                        continue

                values = {
                    field: _format_value(attributes.get(field), datatype)
                    for field, datatype in FIELDS[node.tag].items()
                }

                self.records[target].append(values)

    def extract(self) -> None:
        self.write_records()

        # 必要なカラムのみを抽出
        columns_to_extract = ["startDate", "endDate", "value"]

        # スキーママッピング
        schemas: dict[str, type[pa.DataFrameModel]] = {
            "StepCount": StepCountDFSchema,
            "SleepAnalysis": SleepAnalysisDFSchema,
        }

        self.dataframes: dict[
            str, DataFrame[StepCountDFSchema] | DataFrame[SleepAnalysisDFSchema]
        ] = {}
        for kind in ["StepCount", "SleepAnalysis"]:
            df = pd.DataFrame(self.records[kind])

            if not df.empty:
                # カラムを抽出して型検証を実行
                extracted_df = df[columns_to_extract]
                # startDate, endDateをstringに変換
                extracted_df["startDate"] = extracted_df["startDate"].astype(str)
                extracted_df["endDate"] = extracted_df["endDate"].astype(str)

                # カラム名をスネークケースに変換
                extracted_df = extracted_df.rename(
                    columns={"startDate": "start_date", "endDate": "end_date"}
                )

                self.dataframes[kind] = schemas[kind].validate(extracted_df)  # type: ignore
            else:
                # 空の場合は指定したカラムを持つ空のDataFrameを作成
                self.dataframes[kind] = pd.DataFrame(columns=columns_to_extract)  # type: ignore

        # months_of_extractが指定されている場合、最後の日付から範囲を計算してフィルタリング
        if self.months_of_extract is not None:
            self._filter_by_months()

    def get_dataframes(
        self,
    ) -> dict[str, DataFrame[StepCountDFSchema] | DataFrame[SleepAnalysisDFSchema]]:
        return self.dataframes

    def generate_data_id(self) -> str:
        """データを一意に識別するためのIDを生成する"""

        first_record = self.get_first_record()

        hashed_record: str = hashlib.sha256(
            (str(first_record) + str(envs.DATA_ID_SALT)).encode()
        ).hexdigest()

        # 先頭と末尾から8文字ずつを結合してIDとする
        data_id: str = f"{hashed_record[:8]}{hashed_record[-8:]}"

        return data_id


def _abbreviate(s: str, enabled: bool = True) -> str:
    PREFIX_RE = re.compile(r"^HK.*TypeIdentifier(.+)$")
    m = re.match(PREFIX_RE, s)
    return m.group(1) if enabled and m else s


def _format_value(value: str | None, datatype: Literal["s", "n", "d"]) -> str:
    if value is None:
        return ""
    elif datatype == "s":
        return value
    elif datatype in ("n", "d"):
        return value
    else:
        raise KeyError("Unexpected format value: %s" % datatype)


# 定義されているフィールド
FIELDS: dict[str, Mapping[str, Literal["s", "n", "d"]]] = {
    "Record": OrderedDict(
        (
            ("sourceVersion", "s"),
            ("device", "s"),
            ("startDate", "d"),
            ("endDate", "d"),
            ("value", "n"),
        )
    ),
    "ActivitySummary": OrderedDict(
        (
            ("dateComponents", "d"),
            ("activeEnergyBurned", "n"),
            ("activeEnergyBurnedGoal", "n"),
            ("activeEnergyBurnedUnit", "s"),
            ("appleExerciseTime", "s"),
            ("appleExerciseTimeGoal", "s"),
            ("appleStandHours", "n"),
            ("appleStandHoursGoal", "n"),
        )
    ),
    "Workout": OrderedDict(
        (
            ("sourceVersion", "s"),
            ("device", "s"),
            ("creationDate", "d"),
            ("startDate", "d"),
            ("endDate", "d"),
            ("workoutActivityType", "s"),
            ("duration", "n"),
            ("durationUnit", "s"),
            ("totalDistance", "n"),
            ("totalDistanceUnit", "s"),
            ("totalEnergyBurned", "n"),
            ("totalEnergyBurnedUnit", "s"),
        )
    ),
}
