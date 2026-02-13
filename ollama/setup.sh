#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

first=true
OUTPUT_FILE="$SCRIPT_DIR/models.json"

echo "=== Ollama Model Setup ==="

echo "[" > "$OUTPUT_FILE"
for modelfile in "$SCRIPT_DIR"/Modelfile.*; do
  [ -f "$modelfile" ] || continue

  # Modelfile.llama3 -> thor-llama3
  name="thor-$(basename "$modelfile" | sed 's/^Modelfile\.//')"

  echo "Creating model: $name from $(basename "$modelfile")"
  ollama create "$name" -f "$modelfile"

  # 作成したモデル一覧をJSONで出力
  if [ "$first" = true ]; then
    first=false
  else
    echo "," >> "$OUTPUT_FILE"
  fi
  echo "  \"$name\"" >> "$OUTPUT_FILE"
done
echo "]" >> "$OUTPUT_FILE"

echo ""
echo "=== Setup Complete ==="
ollama list

