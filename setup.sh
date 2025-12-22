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

# Install backend dependencies (if pyproject.toml exists)
if [ -f "/workspace/backend/pyproject.toml" ]; then
    echo "📦 Installing backend dependencies..."
    cd /workspace/backend
    if uv sync; then
        echo "✓ Backend dependencies installed"
    else
        echo "⚠ Backend dependency installation failed"
    fi
fi

# Install frontend dependencies (if package.json exists)
if [ -f "/workspace/frontend/package.json" ]; then
    echo "📦 Installing frontend dependencies..."
    cd /workspace/frontend
    if pnpm install; then
        echo "✓ Frontend dependencies installed"
    else
        echo "⚠ Frontend dependency installation failed"
    fi
fi

echo ""
echo "✅ Dev container is ready!"
echo "---"
echo "Available tools:"
echo "  • Claude Code: claude --help"
echo "  • Lefthook: lefthook run pre-commit"
echo "  • Python (uv): cd backend && uv run python"
echo "  • Node.js (pnpm): cd frontend && pnpm dev"
