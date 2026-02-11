"""定数"""

DEVICE_FILTER = "name:iPhone"
"""歩数を抽出する際のデバイスフィルタ"""

SLEEP_ANALYSIS_IN_BED = "HKCategoryValueSleepAnalysisInBed"
"""睡眠データのうち、ベッドに入っている状態を示す値"""

WATCHOS_MIN_VERSION = 10
"""WatchOSの最低バージョン"""

STEP_COUNT_CSV_FILENAME = "step_count_data.csv"
"""デバッグ用に保存する歩数データのCSVファイル名"""

SLEEP_ANALYSIS_CSV_FILENAME = "sleep_analysis_data.csv"
"""デバッグ用に保存する睡眠データのCSVファイル名"""

STEP_COUNT_JSON_FILENAME = "step_count_data.json"
"""保存する歩数データのJSONファイル名"""

ESTIMATE_SLEEP_JSON_FILENAME = "estimate_sleep_data.json"
"""保存する推定睡眠データのJSONファイル名"""

STEP_CLUSTER_JSON_FILENAME = "step_cluster.json"
"""歩数データクラスタのJSONファイル名"""

CORRECTION_VALUE_JSON_FILENAME = "correction_value.json"
"""アンケートごとの時間補正値のJSONファイル名"""

FEATURE_TIME_RANGE = 0, 12  # (0時~12時)
"""特徴量となるデータの時間範囲(1時間ごと)"""

WEEKDAY_TIME_RANGE = ["3:00", "4:15", "12:00", "21:00"]
"""平日の精査範囲"""

HOLIDAY_TIME_RANGE = ["3:00", "4:45", "12:45", "20:45"]
"""休日の精査範囲"""
