#!/bin/bash

set -euo pipefail

source .env

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Ollama Model Setup ==="

for modelfile in "$SCRIPT_DIR"/Modelfile.*; do
  [ -f "$modelfile" ] || continue

  # Modelfile.llama3 -> thor-llama3
  name="${MODEL_NAME_PREFIX}$(basename "$modelfile" | sed 's/^Modelfile\.//')"

  echo "Creating model: $name from $(basename "$modelfile")"
  ollama create "$name" -f "$modelfile"
done

# ollama に登録されたモデル一覧をJSONで出力
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_FILE="$REPO_ROOT/backend/datastore/models.json"
echo "[" > "$OUTPUT_FILE" # [をファイルに出力
first=true
ollama list | tail -n +2 | while read -r line; do
  model_name=$(echo "$line" | awk '{print $1}')
  if [ "$first" = true ]; then
    first=false
  else
    echo "," >> "$OUTPUT_FILE" # ,をファイルに書き込み
  fi
  echo "  \"$model_name\"" >> "$OUTPUT_FILE" # モデル名をファイルに書き込み
done
echo "]" >> "$OUTPUT_FILE" # ]をファイルに書き込み

echo ""
echo "=== Setup Complete ==="
ollama list
