# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Thor is an AI-driven full-stack monorepo project that extracts and analyzes step count data from Apple Healthcare exports.

## Architecture

### Monorepo Structure

```
Thor-Monorepo/
├── frontend/          # React Router v7 + TypeScript + Tailwind CSS
├── backend/           # FastAPI (Python 3.12+)
├── ollama/            # AI/LLM service
├── Taskfile.yml       # Task runner configuration
└── docker-compose.yml # Infrastructure configuration
```

### Backend Architecture

```
backend/src/
├── core/              # Common utilities (environment variables, etc.)
├── routers/           # FastAPI endpoint definitions
├── schemas/           # Pydantic schemas (request/response models)
└── usecases/          # Business logic layer
```

**Important design principles:**
- `routers/` should only contain endpoint definitions
- Business logic must be placed in `usecases/`
- Request/response type definitions go in `schemas/`
- `core/` contains shared utilities like environment variables and middleware

### Frontend Architecture

Built with React Router v7, a full-stack framework with server-side rendering support.

## Development Environment

### Prerequisites
- VSCode with Dev Container extension
- Docker running
- GitHub SSH connection configured

### Container Services
- `thor-workspace`: Development workspace
- `thor-backend`: FastAPI server (port 8000)
- `thor-frontend`: React Router dev server (port 5173)
- `thor-ollama`: AI/LLM service (port 11434)

### Environment Variables
- Backend environment variables are managed in `backend/.env`
- Defined and accessed via the `Envs` class in `src/core/load_env.py`

## Development Commands

### Task Runner
This project uses Go-Task. View available commands with `task -l`.

### Start Development Servers
```bash
# Start backend
task backend:dev

# Start frontend
task frontend:dev
```

Backend runs at `http://localhost:8000`, Frontend at `http://localhost:5173`.

### Format & Lint
```bash
# Format everything
task format

# Lint everything
task lint

# Backend only
task backend:format
task backend:fix

# Frontend only
task frontend:format
task frontend:lint
```

### Tests
```bash
# Run all tests
task test

# Backend only
task backend:test

# Frontend only
task frontend:test
```

### Type Checking
```bash
# Type check everything
task type-check

# Frontend only
task frontend:type-check
```

### CI-equivalent Checks
```bash
# Run pre-push checks (format-check + lint-check + type-check)
task check
```

## Commit Conventions

Git hooks are managed by Lefthook.

### Commit Message Format
```
<type>: <description>
```

Allowed `<type>` values:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `chore`: Other changes

### Automatic Hooks
- **pre-commit**: Auto-formats and lints code, staging fixes automatically
- **pre-push**: Runs all checks (format-check + lint-check + type-check)

## API Development Guide

### Receiving XML Files

For large files like Apple Healthcare's export.xml, use this pattern:

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
    # xml_data contains raw XML string
    pass
```

Client-side usage:
```bash
# Using curl
curl -X POST -H 'Content-Type: text/xml' \
  --data-binary @export.xml \
  http://localhost:8000/api/v1/extract-steps

# Using JavaScript fetch
const file = document.getElementById('input').files[0];
await fetch('http://localhost:8000/api/v1/extract-steps', {
  method: 'POST',
  headers: {'Content-Type': 'text/xml'},
  body: file
});
```

**Note**: Using a `BaseModel` schema expects JSON format and won't work with raw XML. Use `Body()` directly instead.

## Package Management

- **Backend**: Uses `uv` (dependencies managed in `pyproject.toml`)
- **Frontend**: Uses `pnpm` (dependencies managed in `package.json`)

Execute commands inside containers:
```bash
# Run arbitrary command in backend container
task backend -- <command>

# Run arbitrary command in frontend container
task frontend -- <command>
```
