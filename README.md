# Thor-Monorepo

Thor の AI 駆動のフルスタック

https://github.com/273Do/Thor
https://github.com/273Do/Thor-Web-App-Frontend  
https://github.com/273Do/Thor-Web-App-Backend

## プロジェクト構成

- **Frontend**: React Router v7 + TypeScript + Tailwind CSS
- **Backend**: FastAPI (Python 3.12+)
- **AI/LLM**: Ollama (ホストマシン)
- **インフラ**: Docker Compose
- **タスクランナー**: Go-Task
- **Coding Agent**: Claude Code

## 必要な環境

- VSCode
- Docker
- 事前に GitHub で ssh key を発行して ssh 接続ができるよう準備してください。

## セットアップ

### 1. Ollama をインストール

[こちら](https://ollama.com/download/mac)から Ollama をインストール

### 2. リポジトリのクローン

```bash
git clone git@github.com:273Do/Thor-Monorepo.git
```

### 3. 起動方法

VSCode で Dev Container でプロジェクトを開きます。

### 4. 初期設定

1. `backend`ディレクトリに事前のデータを格納するディレクトリを作成します。
2. 環境変数を作成します。
3. 以下のコマンドでパッケージをインストールします。

```bash
task frontend -- pnpm i
task backend -- uv sync
```

4. 以下のコマンドで react router の型を作成します。

```bash
task frontend -- pnpm react-router typegen
```

### 5. Claude Code

Claude Code を契約している場合はターミナルから以下のコマンドでセットアップが可能です。

```bash
claude
```

## 開発コマンド

- 各種コマンドは`task -l`で確認できます。
- [http://localhost:8000/docs](http://localhost:8000/docs) で Swagger を使用できます。

# クレジット

- 開発：273\*
- This source code contains a partially modified version of [**applehealthdata**](https://github.com/tdda/applehealthdata) .
- この作成物および同梱物を使用したことによって生じたすべての障害・損害・不具合等に関しては，私と私の関係者および私の所属するいかなる団体・組織とも，一切の責任を負いません．各自の責任においてご使用ください．
