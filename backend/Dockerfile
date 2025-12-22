FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /workspace/backend

# Install additional dependencies if needed
RUN apt-get update && \
  apt-get install -y --no-install-recommends git openssh-client && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

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