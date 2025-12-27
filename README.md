# Thor-Monorepo

Thor の AI 駆動のフルスタック

https://github.com/273Do/Thor
https://github.com/273Do/Thor-Web-App-Frontend
https://github.com/273Do/Thor-Web-App-Backend

## プロジェクト構成

- **Frontend**: React Router v7 + TypeScript + Tailwind CSS
- **Backend**: FastAPI (Python 3.12+)
- **AI/LLM**: Ollama
- **インフラ**: Docker Compose
- **タスクランナー**: Go-Task
- **Coding Agent**: Claude Code

## 必要な環境

- VSCode
- Docker
- 事前に GitHub で ssh 接続ができるよう準備してください。

## セットアップ

### 1. リポジトリのクローン

```bash
git clone git@github.com:273Do/Thor-Monorepo.git
```

### 2. 起動方法

VSCode で Dev Container でプロジェクトを開きます。

### 3. Claude Code

Claude Code を契約している場合は`claude`でセットアップ可能です。

## 開発コマンド

- 各種コマンドは`task -l`で確認できます。
