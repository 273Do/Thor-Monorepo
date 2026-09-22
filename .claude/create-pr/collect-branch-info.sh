#!/bin/bash
# PR作成に必要なブランチ情報を収集する
set -euo pipefail

BASE_BRANCH="${1:-develop}"

echo "=== BRANCH ==="
git branch --show-current

echo "=== COMMITS ==="
git log "${BASE_BRANCH}..HEAD" --oneline

echo "=== STAT ==="
git diff "${BASE_BRANCH}...HEAD" --stat

echo "=== DIFF ==="
git diff "${BASE_BRANCH}...HEAD"
