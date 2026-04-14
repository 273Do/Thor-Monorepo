# Thor-Monorepo

Thor の AI 駆動のフルスタック

https://github.com/273Do/Thor
https://github.com/273Do/Thor-Web-App-Frontend  
https://github.com/273Do/Thor-Web-App-Backend

## アプリ概要

本 web アプリは、iPhone のヘルスケアデータから睡眠パターンを推定・分析するWebサービスです。

### フロー

1. アンケート回答 - 睡眠に関する3つの質問に答える
   - スマホの充電タイミング
   - 家の中でスマホを持ち歩くか
   - 普段の就寝時刻

2. データアップロード - Apple ヘルスケアからエクスポートした XML ファイルをアップロード
3. 歩数抽出 - XML から歩数データ（＋睡眠データ）を抽出
4. 睡眠推定 - 歩数データ＋アンケート回答をもとに、日ごとの就寝・起床時刻を推定
5. 結果表示 - 推定結果をチャートで可視化
   - 就寝・起床時刻の折れ線グラフ
   - 睡眠時間の棒グラフ
6. AIフィードバック - LLM（ Ollama 経由）が睡眠パターンについてマークダウン形式のアドバイスを生成

### iPhone 端末以外の方について

本サービスは Apple ヘルスケアの XML エクスポートを利用するため、iPhone ユーザーを対象としています。Android など他のデバイスをお使いの方は、ヘルスデータを[指定の形式](https://github.com/273Do/Thor-Monorepo/blob/1923da19e313a79f8afa3c7c4b4036ce1542586a/backend/src/schemas/estimate_sleep.py#L29-L46)に変換したうえで API を直接呼び出すことでご利用いただけます。

## プロジェクト構成

- **Frontend**: React + TypeScript + Tailwind CSS
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

### 3. LLM の用意

以下のコマンドを実行して`ollama/` 内に用意された LLM を読み込みます。

```bash
chmod +x ollama/setup.sh
./ollama/setup.sh
```

うまく読み込めると以下のように表示されますが、自作モデル（thor-\*）はベースモデルの重みを共有して参照しているだけなので、ディスク容量が2倍になるわけではありません。Modelfile
で設定したパラメータの差分だけが追加で保持されています。

```
NAME                  ID              SIZE      MODIFIED
gemma3:12b            hogehogehoge    o GB    x seconds ago
thor-gemma3:latest    fugafugafuga    o GB    x seconds ago
thor-llama3:latest    piyopiyopiyo    o GB    x seconds ago
llama3.1:8b           fofoofoofoof    o GB    x seconds ago
```

### 4. 起動方法

VSCode で Dev Container でプロジェクトを開きます。

### 5. 初期設定

1. `backend`ディレクトリに事前のデータを格納するディレクトリを作成します。
2. 以下の手順に従って送信用のメールアドレスを設定します。
   1. [myaccount.google.com/security](https://myaccount.google.com/security) を開きます。
   2. 「2段階認証プロセス」を有効にします。
   3. [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) を開きます。
   4. 「アプリ名」に任意の名前を入力して「作成」を押し、表示された16文字のパスワード（xxxx xxxx xxxx xxxx形式<環境変数に設定する際は空白は含まない>）を控える。

3. 各環境変数を作成します。
4. 以下のコマンドでパッケージをインストールします。

```bash
task frontend -- pnpm i
task backend -- uv sync
```

5. 以下のコマンドでアプリを起動します。

```bash
task frontend:dev
task backend:dev
```

6. アプリを公開する場合はドメインを取得しておきます。

### 6. Claude Code

Claude Code を契約している場合はターミナルから以下のコマンドでセットアップが可能です。

```bash
claude
```

## 開発コマンド

- 各種コマンドは`task -l`で確認できます。
- [http://localhost:8000/docs](http://localhost:8000/docs) で Swagger を使用できます。
- API 仕様書を作成する場合はこちらのツールを使用すると楽です。

## 公開設定

- cloudflare tunnel を使用してアプリを公開します。

1. [Cloudflareダッシュボード](https://dash.cloudflare.com)から [Zero Trust] > [Networks] > [Overview] > [Manage Tunnels] > [Create new cloudflared Tunnel] を選択します。

2. トンネル名を入力して作成します。

3. [Configure] 画面にて [Install and run a connector] の項目で [Docker] を選択し、表示されているコマンド内のトークンを env ファイルに設定します。

4. [Published application routes] 画面にてルーティング設定を行います。
   | Subdomain | Domain | Service Type | URL (Docker内部名) |  
    | --------- | ----------- | ------------ | ------------------------ |  
    | (空欄) | example.com | HTTP | http://frontend:5173 |  
    | api | example.com | HTTP | http://backend:8000 |

# クレジット

- 開発：273\*
- This source code contains a partially modified version of [**applehealthdata**](https://github.com/tdda/applehealthdata) .
- この作成物および同梱物を使用したことによって生じたすべての障害・損害・不具合等に関しては，私と私の関係者および私の所属するいかなる団体・組織とも，一切の責任を負いません．各自の責任においてご使用ください．
