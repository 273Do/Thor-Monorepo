FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install common system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    openssh-client \
    build-essential \
    ca-certificates \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.12
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.12 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

# Install uv and ruff
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    curl -LsSf https://astral.sh/ruff/install.sh | sh

# Install Node.js 22
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Enable corepack and install pnpm
RUN corepack enable && \
    corepack prepare pnpm@latest --activate

# Install lefthook
RUN curl -1sLf 'https://dl.cloudsmith.io/public/evilmartians/lefthook/setup.deb.sh' | bash && \
    apt-get update && \
    apt-get install -y lefthook && \
    rm -rf /var/lib/apt/lists/*

# Install Task (go-task)
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin

# Install Claude Code
RUN curl -fsSL https://claude.ai/install.sh | bash

# Set working directory
WORKDIR /workspace

CMD ["sleep", "infinity"]
