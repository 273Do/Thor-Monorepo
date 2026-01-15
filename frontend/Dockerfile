FROM node:22.16.0-bookworm

WORKDIR /workspace/frontend

RUN corepack enable && \
  corepack prepare pnpm@latest --activate

ENV PNPM_HOME="/root/.local/share/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN pnpm config set global-bin-dir /usr/local/bin && \
  pnpm add -g @evilmartians/lefthook

# Copy dependency files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy application code
COPY . .

RUN node --version && \
  pnpm --version

EXPOSE 5173

# Keep container running
CMD ["sleep", "infinity"]