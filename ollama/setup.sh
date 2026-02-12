#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Ollama Model Setup ==="

for modelfile in "$SCRIPT_DIR"/Modelfile.*; do
  [ -f "$modelfile" ] || continue

  # Modelfile.llama3 -> thor-llama3
  name="thor-$(basename "$modelfile" | sed 's/^Modelfile\.//')"

  echo "Creating model: $name from $(basename "$modelfile")"
  ollama create "$name" -f "$modelfile"
done

echo ""
echo "=== Setup Complete ==="
ollama list
