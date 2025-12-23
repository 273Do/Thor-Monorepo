FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# ============================================================================
# Environment Configuration
# ============================================================================
ENV LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8

# ============================================================================
# Japanese Locale
# ============================================================================
RUN sudo apt-get update && \
    sudo apt-get install -y locales && \
    sudo locale-gen ja_JP.UTF-8 && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*

# ============================================================================
# Node.js & Package Managers
# ============================================================================
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash - && \
    sudo apt-get install -y nodejs && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/* && \
    corepack enable && \
    corepack prepare pnpm@latest --activate

# ============================================================================
# Development Tools
# ============================================================================
# Install lefthook
RUN curl -1sLf 'https://dl.cloudsmith.io/public/evilmartians/lefthook/setup.deb.sh' | sudo bash && \
    sudo apt-get update && \
    sudo apt-get install -y lefthook && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*

# Install Task
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin

# Install Claude Code
RUN curl -fsSL https://claude.ai/install.sh | bash

# ============================================================================
# Workspace Configuration
# ============================================================================
WORKDIR /workspace

CMD ["sleep", "infinity"]