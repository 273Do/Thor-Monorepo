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

import re
from collections import Counter, OrderedDict
from xml.etree import ElementTree

import pandas as pd


class HealthDataExtractor:
    def __init__(self, data: str, verbose=True):
        self.verbose = verbose
        self.records = {"StepCount": [], "SleepAnalysis": []}

        # 文字列を読み込んでXMLを解析
        self.root = ElementTree.fromstring(data)

        self.nodes = list(self.root)

        self.abbreviate_types()
        self.collect_stats()

    def count_tags_and_fields(self):
        self.tags = Counter()
        self.fields = Counter()
        for record in self.nodes:
            self.tags[record.tag] += 1
            for k in record.keys():
                self.fields[k] += 1

    def count_record_types(self):
        self.record_types = Counter()
        self.other_types = Counter()
        for record in self.nodes:
            if record.tag == "Record":
                self.record_types[record.attrib["type"]] += 1
            elif record.tag in ("ActivitySummary", "Workout"):
                self.other_types[record.tag] += 1

    def collect_stats(self):
        self.count_record_types()
        self.count_tags_and_fields()

    def abbreviate_types(self):
        for node in self.nodes:
            if node.tag == "Record" and "type" in node.attrib:
                node.attrib["type"] = _abbreviate(node.attrib["type"])

    def write_records(self):
        target_kinds = ["StepCount", "SleepAnalysis"]
        kinds = FIELDS.keys()

        for node in self.nodes:
            if node.tag in kinds:
                attributes = node.attrib
                kind = attributes["type"] if node.tag == "Record" else node.tag

                if _abbreviate(kind) not in target_kinds:
                    continue

                values = {
                    field: _format_value(attributes.get(field), datatype)
                    for field, datatype in FIELDS[node.tag].items()
                }
                self.records[_abbreviate(kind)].append(values)

    def extract(self):
        self.write_records()
        self.dataframes = {
            "StepCount": pd.DataFrame(self.records["StepCount"]),
            "SleepAnalysis": pd.DataFrame(self.records["SleepAnalysis"]),
        }

    def get_dataframes(self):
        return self.dataframes


def _abbreviate(s, enabled=True):
    PREFIX_RE = re.compile(r"^HK.*TypeIdentifier(.+)$")
    m = re.match(PREFIX_RE, s)
    return m.group(1) if enabled and m else s


def _format_value(value, datatype):
    if value is None:
        return ""
    elif datatype == "s":
        return value
    elif datatype in ("n", "d"):
        return value
    else:
        raise KeyError("Unexpected format value: %s" % datatype)


# 定義されているフィールド
FIELDS = {
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
