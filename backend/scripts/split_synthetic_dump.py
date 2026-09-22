#!/usr/bin/env python3
"""疑似データダンプ (synthetic_sleep_datadump.csv) を user_id ごとに分割するスクリプト。

安定/非安定 × iOS/Android × 2人 = 8人分のダンプから、type が sleep のレコードを
ユーザーごとの CSV に切り出す。オプションで step も出力できる。

使い方：
    task backend:split_synthetic_dump
    task backend:split_synthetic_dump -- --with-step
"""

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from src.core.load_env import envs

BACKEND_DIR = Path(__file__).resolve().parent.parent

DUMP_FILENAME = "synthetic_sleep_datadump.csv"
OUTPUT_DIR_NAME = "synthetic_users"

TIME_COLUMN = "time"
USER_ID_COLUMN = "user_id"
TYPE_COLUMN = "type"

SLEEP_TYPE = "sleep"
STEP_TYPE = "step"

EXPECTED_USER_COUNT = 8


def resolve_sample_data_dir() -> Path:
    """環境変数 SAMPLE_DATA_DIR を絶対パスに解決する

    Returns:
        Path: サンプルデータディレクトリの絶対パス
    """

    sample_data_dir = Path(envs.SAMPLE_DATA_DIR)

    if sample_data_dir.is_absolute():
        return sample_data_dir

    # Envs の値は backend ディレクトリからの相対パスで定義されている
    return BACKEND_DIR / sample_data_dir


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパースする"""

    sample_data_dir = resolve_sample_data_dir()

    parser = argparse.ArgumentParser(
        description="疑似データダンプを user_id ごとの CSV に分割する",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=sample_data_dir / DUMP_FILENAME,
        help=f"入力するダンプ CSV のパス (default: SAMPLE_DATA_DIR/{DUMP_FILENAME})",
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        type=Path,
        default=sample_data_dir / OUTPUT_DIR_NAME,
        help=f"出力先ディレクトリ (default: SAMPLE_DATA_DIR/{OUTPUT_DIR_NAME})",
    )
    parser.add_argument(
        "--with-step",
        action="store_true",
        help="sleep に加えて step のレコードも出力する",
    )

    return parser.parse_args()


def load_rows(input_path: Path) -> tuple[List[str], List[Dict[str, str]]]:
    """ダンプ CSV を読み込む

    Args:
        input_path (Path): ダンプ CSV のパス

    Returns:
        tuple[List[str], List[Dict[str, str]]]: ヘッダー列名のリストと行のリスト
    """

    # ダンプ先頭に BOM が含まれるため utf-8-sig で読む
    with input_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"ヘッダー行が読み取れません: {input_path}")

        return list(reader.fieldnames), list(reader)


def group_rows(
    rows: List[Dict[str, str]], target_types: List[str]
) -> Dict[tuple[str, str], List[Dict[str, str]]]:
    """(user_id, type) ごとに行をまとめる

    Args:
        rows (List[Dict[str, str]]): ダンプの全行
        target_types (List[str]): 抽出対象の type

    Returns:
        Dict[tuple[str, str], List[Dict[str, str]]]: (user_id, type) をキーとした行のリスト
    """

    grouped: Dict[tuple[str, str], List[Dict[str, str]]] = defaultdict(list)

    for row in rows:
        row_type = row[TYPE_COLUMN]
        if row_type not in target_types:
            continue

        grouped[(row[USER_ID_COLUMN], row_type)].append(row)

    # 時系列順に整える
    for group in grouped.values():
        group.sort(key=lambda row: row[TIME_COLUMN])

    return grouped


def write_group(
    out_dir: Path,
    user_id: str,
    row_type: str,
    fieldnames: List[str],
    rows: List[Dict[str, str]],
) -> Path:
    """1 ユーザー 1 type 分の CSV を書き出す

    Args:
        out_dir (Path): 出力先ディレクトリ
        user_id (str): ユーザーID
        row_type (str): レコードの type
        fieldnames (List[str]): 出力する列名
        rows (List[Dict[str, str]]): 出力する行

    Returns:
        Path: 書き出したファイルのパス
    """

    out_path = out_dir / f"{user_id}_{row_type}.csv"

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return out_path


def main() -> int:
    """エントリポイント"""

    args = parse_args()

    if not args.input.is_file():
        print(f"入力ファイルが見つかりません: {args.input}", file=sys.stderr)
        return 1

    target_types = [SLEEP_TYPE] + ([STEP_TYPE] if args.with_step else [])

    fieldnames, rows = load_rows(args.input)
    grouped = group_rows(rows, target_types)

    if not grouped:
        print(
            f"対象のレコードが見つかりませんでした (type: {', '.join(target_types)})",
            file=sys.stderr,
        )
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)

    user_ids = sorted({user_id for user_id, _ in grouped})
    if len(user_ids) != EXPECTED_USER_COUNT:
        print(
            f"警告: ユーザー数が想定 ({EXPECTED_USER_COUNT}人) と異なります: {len(user_ids)}人",
            file=sys.stderr,
        )

    print(f"入力: {args.input}")
    print(f"出力先: {args.out_dir}")
    print(f"対象 type: {', '.join(target_types)}")

    for user_id in user_ids:
        for row_type in target_types:
            group = grouped.get((user_id, row_type))
            if not group:
                print(f"  {user_id} ({row_type}): レコードなし", file=sys.stderr)
                continue

            out_path = write_group(args.out_dir, user_id, row_type, fieldnames, group)
            print(f"  {out_path.name}: {len(group)} 件")

    print(f"完了: {len(user_ids)}人分を出力しました")

    return 0


if __name__ == "__main__":
    sys.exit(main())
