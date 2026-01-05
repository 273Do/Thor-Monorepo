#!/bin/bash
set -e

echo "🚀 Setting up development environment..."

# Initialize lefthook
echo "📦 Initializing lefthook..."
if lefthook install; then
    echo "✓ Lefthook git hooks installed"
else
    echo "⚠ Lefthook installation failed"
fi

# Verify Claude Code installation
if command -v claude &> /dev/null; then
    echo "✓ Claude Code is available at: $(which claude)"
else
    echo "⚠ Claude Code not found in PATH"
fi

# Note: Backend and frontend dependencies are installed in their respective Docker containers
# Backend: via backend/Dockerfile (uv sync)
# Frontend: via frontend/Dockerfile (pnpm install)

echo ""
echo "✅ Dev container is ready!"
echo "---"
echo "Available tools:"
echo "  • Claude Code: claude --help"
echo "  • Lefthook: lefthook run pre-commit"
echo "  • Python (uv): cd backend && uv run python"
echo "  • Node.js (pnpm): cd frontend && pnpm dev"
