FROM ghcr.io/astral-sh/uv:0.9.11-python3.14-bookworm-slim

WORKDIR /workspace/backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy


# Install additional system dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends git openssh-client && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Install ruff using uv
RUN uv tool install ruff

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen --no-install-project --no-dev

# Copy application code
COPY . .

# Install the project
RUN uv sync --frozen --no-dev

# Add virtual environment to PATH
ENV PATH="/workspace/backend/.venv/bin:$PATH"

# Keep container running
CMD ["sleep", "infinity"]