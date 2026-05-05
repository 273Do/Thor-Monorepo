# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Thor is an AI-driven full-stack monorepo that extracts step count data from Apple Healthcare XML exports to estimate and visualize sleep patterns, with LLM-generated feedback via Ollama.

## Architecture

### Monorepo Structure

```
Thor-Monorepo/
├── frontend/          # React Router v7 + TypeScript + Tailwind CSS
├── backend/           # FastAPI (Python 3.12+)
├── Taskfile.yml       # Task runner configuration
└── docker-compose.yml # Infrastructure configuration
```

### Backend Architecture

```
backend/src/
├── core/              # Shared utilities (Envs class, constants)
├── routers/           # FastAPI endpoint definitions (thin layer only)
├── schemas/           # Pydantic request/response models
└── usecases/          # All business logic
    ├── extract_steps/ # Apple XML parsing
    ├── estimate_sleep/# K-means clustering → feature extraction → sleep time estimation
    ├── llm_feedback/  # Ollama integration (via OpenAI-compatible SDK)
    └── via_email/     # SMTP email delivery with Jinja2 templates
```

**Design principles:**
- `routers/` must only contain endpoint definitions — business logic goes in `usecases/`
- `schemas/` holds all Pydantic models
- `core/` contains shared utilities: `load_env.py` (Envs class) and `constants.py`

### Backend API Endpoints (`/api/v1`)

1. **POST `/extract-steps`** — Parses Apple Healthcare XML, returns step data in 15-min intervals. Body is raw `text/xml`. Query params: `months_of_extract` (int) OR `start_date_of_extract`+`end_date_of_extract` (ISO 8601), `include_recorded_sleep` (bool).
2. **POST `/estimate-sleep`** — Runs ML pipeline (K-means → feature extraction → late-night detection → bed/wake time estimation). Returns daily sleep estimates + available LLM models.
3. **POST `/feedback`** — Fetches LLM feedback from Ollama for a previously saved estimation (identified by `id`). Params: `id`, `llm` (model name), `lang` (`ja`/`en`).
4. **POST `/via-email`** — One-shot workflow: extract → estimate → feedback → send email. FormData with `xml_file` (multipart) + `req` (JSON string).

**Data persistence pattern**: `extract-steps` generates a hash-based `id` and saves data as JSON to `VAULT_DIR`. Subsequent endpoints use this `id` to retrieve the saved data, enabling stateless requests.

### Frontend Architecture

Single-page application (all UI in `app/routes/home.tsx`) with three UI states:
1. **Input** — Survey form (3 questions about phone habits + bedtime), XML file upload, optional email
2. **Loading** — Progress through extract → estimate → feedback stages
3. **Results** — Recharts timeline/bar charts for bed/wake times; LLM feedback rendered as Markdown via react-markdown

Key directories:
- `app/components/` — Reusable components (survey-form, file-upload, result-view, ai-feedback)
- `app/utils/` — SWR hooks (`use-extract-steps`, `use-estimate-sleep`, `use-ai-feedback`) + fetch wrappers in `api.ts`
- `app/core/` — `constants.ts` (API endpoint), `survey-schema.ts` (Zod validation)
- `app/locales/` — `translation-ja.json` and `translation-en.json` (i18next)

## Development Environment

### Container Services

- `thor-workspace`: Dev Container (VSCode)
- `thor-backend`: FastAPI on port 8000
- `thor-frontend`: React Router dev server on port 5173
- `thor-ollama`: Ollama LLM service on port 11434

### Environment Variables

**Backend** (`backend/.env`) — all defined in `src/core/load_env.py` as the `Envs` class:

Required:
```
DATA_ID_SALT=          # Salt for ID generation
MAIL_ADDRESS=          # Gmail address
MAIL_USERNAME=         # Same as MAIL_ADDRESS
MAIL_PASSWORD=         # Gmail App Password (16 chars, not account password)
MAIL_FROM=             # Sender address
```

Optional (defaults shown):
```
IS_DEBUG=false
DATASTORE_DIR=./datastore
VAULT_DIR=./datastore/vault
OLLAMA_ENDPOINT=http://host.docker.internal:11434/v1/
FRONTEND_ENDPOINT=http://localhost:5173
API_V1_PREFIX=/api/v1
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

**Frontend** (`frontend/.env`):
```
VITE_BACKEND_ENDPOINT=http://localhost:8000
```

## Development Commands

This project uses Go-Task. View all commands with `task -l`.

### Servers

```bash
task backend:dev   # FastAPI with auto-reload on port 8000
task frontend:dev  # Vite HMR on port 5173
```

### Format, Lint & Type Check

```bash
task format           # Format backend (Ruff) + frontend (Prettier)
task lint             # Lint and auto-fix backend (Ruff) + frontend (ESLint)
task type-check       # TypeScript type check (frontend only)
task check            # CI-equivalent: format-check + lint-check + type-check (no auto-fix)
```

### Tests

```bash
task test             # Run all tests
task backend:test     # pytest -v
task frontend:test    # pnpm run test
```

Run a single backend test file or function:
```bash
task backend -- uv run pytest path/to/test_file.py -v
task backend -- uv run pytest path/to/test_file.py::test_function_name -v
```

### Arbitrary Container Commands

```bash
task backend -- <command>   # Run in backend container (e.g., uv add <pkg>)
task frontend -- <command>  # Run in frontend container (e.g., pnpm add <pkg>)
```

## Commit Conventions

Git hooks via Lefthook:
- **pre-commit**: Auto-formats and lints, stages fixes
- **pre-push**: Runs `task check` (no auto-fix)

Commit message format: `<type>: <description>`

Allowed types: `feat`, `fix`, `refactor`, `chore`

## API Development Guide

### Receiving XML Files

For raw XML bodies (not JSON), use `Body()` directly — `BaseModel` schemas expect JSON and won't work:

```python
from fastapi import APIRouter, Body

@router.post("/extract-steps")
async def extract_steps(
    xml_data: str = Body(
        media_type="text/xml",
        description="XML file exported from Apple Healthcare",
        example="<?xml version=\"1.0\"?>..."
    )
):
    pass
```

```bash
curl -X POST -H 'Content-Type: text/xml' \
  --data-binary @export.xml \
  'http://localhost:8000/api/v1/extract-steps?months_of_extract=1'
```

### LLM Integration

The backend uses the OpenAI Python SDK pointed at the Ollama endpoint — not actual OpenAI. The `OLLAMA_ENDPOINT` env var configures this. Model names come from Ollama's model list (e.g., `thor-gemma3:latest`).

## Package Management

- **Backend**: `uv` (`pyproject.toml`)
- **Frontend**: `pnpm` (`package.json`)
