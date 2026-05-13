# Codex Market Skills

Codex Market Skills は、取引、投資リサーチ、市場カレンダー管理のための Codex skills 集です。もともとは `market-calendar-google` だけのプロジェクトでしたが、現在は複数の市場関連 skill を同じ GitHub リポジトリで管理する構成に変更しています。

## 含まれる skills

### [`market-calendar-google`](docs/skills/market-calendar-google.md)

米国株決算、日本株決算、中国・米国・日本のマクロ指標、中央銀行イベント、国債入札、その他の重要市場イベントを整理し、ユーザーのルールに従って Google Calendar に追加します。

主な用途：

- Earnings Whispers の週間米国決算画像を整理する。
- ウォッチリストに基づいて米国株・日本株決算を絞り込む。
- 中国・米国・日本の重要度が高い経済イベントを整理する。
- 日本時間で Google Calendar に登録し、重複を避ける。

### [`jp-stock-move-reason`](docs/skills/jp-stock-move-reason.md)

入力された日本株コードについて、Yahoo Finance のリアルタイム株価欄、Yahoo 掲示板、Yahoo/Kabutan/Traders のニュース、基本指標を収集し、Codex が株価変動理由を分析するための材料を作ります。この skill は Gemini などの LLM API を呼び出さず、認証情報も読みません。

主な用途：

- 日本株の急騰、急落、出来高急増の理由を調べる。
- ニュースで確認できる材料と、掲示板上の思惑を分けて見る。
- 現在の騰落率、時価総額、PER/PBR、信用倍率、掲示板の温度感を確認する。

### [`cn-stock-move-reason`](docs/skills/cn-stock-move-reason.md)

入力された単一の A 株コードについて、Eastmoney の公開株価データ、公告、股吧/资讯投稿を収集し、Sohu の指数・セクター情報と A 株の騰落銘柄数も合わせて、Codex が株価変動理由、市場/セクター/個別株の共振、短期センチメントサイクルを分析するための材料を作ります。この skill は Gemini などの LLM API を呼び出さず、認証情報も読みません。

主な用途：

- A 株の涨停、跌停、炸板、出来高急増の理由を調べる。
- 公告・業績で確認できる材料と、股吧上の思惑を分けて見る。
- 主要指数、業種/テーマ板、騰落銘柄数から、市場全体の共振、セクター主導、個別材料主導を切り分ける。
- 冰点、修复/潜伏、启动、加速、高潮、高位分歧/分化、退潮の七段階で短期情緒を確認する。

### [`us-stock-gamma-moomoo`](docs/skills/us-stock-gamma-moomoo.md)

moomoo OpenD から米国株・米国オプションデータを取得し、Codex が gamma/GEX、gamma wall、gamma flip、SPX/SPY/ES の日中構造、0DTE オプションのシナリオ価格表を分析するための skill です。ローカルで moomoo OpenD が起動している必要があり、環境がない場合は先にインストールまたは起動を案内します。

主な用途：

- 通常の米国株または米国 ETF のオプション gamma 構造を分析する。
- `.SPX`/SPXW の指数オプション構造を分析する。指数データやチェーンが直接取れない場合は、SPY オプション、ES/CFD、またはユーザー提供の指数アンカーで換算し、プロキシを明示する。
- 0DTE call/put について、時間 x 原資産価格の理論価値表を作り、回復、利確、損切り水準を検討する。
- 必要に応じてローカル HTML gamma レポートを生成し、急ぎの日中質問ではチャットだけで結論を返す。

### [`stock-technical-analysis`](docs/skills/stock-technical-analysis.md)

米国株、日本株、A 株のテクニカル構造を分析する skill です。日中トレンド、支持・抵抗、出来高と価格、KDJ/MACD/RSI、Vegas チャネル、チャート読解、特定価格に到達できるかの判断に使います。公開用の自己完結版であり、ローカルの `Stocks` フォルダには依存しません。

主な用途：

- 強トレンド継続、高値圏保ち合い、押し目確認、ブレイク失敗、ダイバージェンス、破位反発などを分類する。
- touch、break、tradable hold を区別し、一本のヒゲを有効ブレイクと誤認しない。
- moomoo/Yahoo/証券アプリのチャートやスクリーンショットから、現在値、構造、出来高・モメンタム、実行上の意味、次の確認点を読む。
- 個別株材料分析や米国 gamma skill と組み合わせ、材料をチャートが確認しているかを判断する。

## インストール

リポジトリを任意の場所に clone し、使いたい skill ディレクトリを `~/.codex/skills/` にコピーまたはシンボリックリンクします。

```bash
git clone https://github.com/tsetsugekka/codex-market-skills.git
mkdir -p ~/.codex/skills
ln -s /path/to/codex-market-skills/skills/market-calendar-google ~/.codex/skills/market-calendar-google
ln -s /path/to/codex-market-skills/skills/jp-stock-move-reason ~/.codex/skills/jp-stock-move-reason
ln -s /path/to/codex-market-skills/skills/cn-stock-move-reason ~/.codex/skills/cn-stock-move-reason
ln -s /path/to/codex-market-skills/skills/us-stock-gamma-moomoo ~/.codex/skills/us-stock-gamma-moomoo
ln -s /path/to/codex-market-skills/skills/stock-technical-analysis ~/.codex/skills/stock-technical-analysis
```

必要な skill だけをインストールしても構いません。

## 使用例

```text
来週の Earnings Whispers 決算カレンダーを整理して Google Calendar に追加して。
```

```text
今週の中国・米国・日本の重要イベントを四つ星以上だけ Google Calendar に入れて。
```

```text
6758 の今日の急騰理由を分析して。
```

```text
6217 はニュース材料なのか掲示板の思惑なのか見て。
```

```text
300750 は公告材料なのか短期テーマ情緒なのか分析して。
```

```text
この米国株の gamma を見て、抵抗帯と今週行きやすい水準を出して。
```

```text
SPXW 0DTE 7370C を、時間と SPX 水準ごとに理論価格表にして。
```

```text
この株の今のテクニカル、支持線と抵抗線を見て。
```

## セキュリティ

- `market-calendar-google` は、ユーザーが明示的に依頼した場合に Google Calendar コネクタで予定を作成・更新します。
- `jp-stock-move-reason` は公開ページ/API だけを読み取り、token を読まず、外部サービスへ書き込まず、Gemini/OpenAI API も呼び出しません。
- `cn-stock-move-reason` は Eastmoney、Sohu 証券などの公開ページ/API だけを読み取り、token を読まず、外部サービスへ書き込まず、Gemini/OpenAI API も呼び出しません。
- `us-stock-gamma-moomoo` はローカルの moomoo OpenD の行情インターフェースを使い、取引ロック解除 API は呼び出しません。公開版はローカルの `Stocks` フォルダに依存せず、個人口座情報、OpenD ログ、スクリーンショット、私的な行情出力、独自戦略名、私的な人名/handle はコミットしないでください。
- `stock-technical-analysis` は汎用テクニカル分析ルールだけを保存します。公開版はローカルの `Stocks` フォルダに依存せず、個人ポジション、売買計画、スクリーンショット原本、私的な研究パス、専有指標名、独自戦略名、私的な人名/handle はコミットしないでください。
- 個人の学習資料を使う場合は、この公開リポジトリ外の private RAG/knowledge base に置き、抽象化した汎用ルールだけを skill に戻してください。
- 個人のウォッチリスト、認証情報、`.env`、実行キャッシュ、私的な出力はこのリポジトリにコミットしないでください。

## リポジトリ構成

```text
skills/
  market-calendar-google/
    SKILL.md
    agents/openai.yaml
  jp-stock-move-reason/
    SKILL.md
    references/experience.md
    scripts/stock_move_sources.py
  cn-stock-move-reason/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    scripts/stock_move_sources.py
  us-stock-gamma-moomoo/
    SKILL.md
    references/
    scripts/gamma_report.py
    scripts/option_scenario_table.py
  stock-technical-analysis/
    SKILL.md
    agents/openai.yaml
    references/
docs/
  skills/
    market-calendar-google.md
    jp-stock-move-reason.md
    cn-stock-move-reason.md
    us-stock-gamma-moomoo.md
    stock-technical-analysis.md
```

## 言語

- 中文：`README.md`
- 日本語：`README.ja.md`
- English: `README.en.md`
