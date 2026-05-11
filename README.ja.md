# Codex Market Skills

Codex Market Skills は、取引、投資リサーチ、市場カレンダー管理のための Codex skills 集です。もともとは `market-calendar-google` だけのプロジェクトでしたが、現在は複数の市場関連 skill を同じ GitHub リポジトリで管理する構成に変更しています。

## 含まれる skills

### [`market-calendar-google`](skills/market-calendar-google/README.md)

米国株決算、日本株決算、中国・米国・日本のマクロ指標、中央銀行イベント、国債入札、その他の重要市場イベントを整理し、ユーザーのルールに従って Google Calendar に追加します。

主な用途：

- Earnings Whispers の週間米国決算画像を整理する。
- ウォッチリストに基づいて米国株・日本株決算を絞り込む。
- 中国・米国・日本の重要度が高い経済イベントを整理する。
- 日本時間で Google Calendar に登録し、重複を避ける。

### [`jp-stock-move-reason`](skills/jp-stock-move-reason/README.md)

入力された日本株コードについて、Yahoo Finance のリアルタイム株価欄、Yahoo 掲示板、Yahoo/Kabutan/Traders のニュース、基本指標を収集し、Codex が株価変動理由を分析するための材料を作ります。この skill は Gemini などの LLM API を呼び出さず、認証情報も読みません。

主な用途：

- 日本株の急騰、急落、出来高急増の理由を調べる。
- ニュースで確認できる材料と、掲示板上の思惑を分けて見る。
- 現在の騰落率、時価総額、PER/PBR、信用倍率、掲示板の温度感を確認する。

### [`cn-stock-move-reason`](skills/cn-stock-move-reason/README.md)

入力された単一の A 株コードについて、Eastmoney の公開株価データ、公告、股吧/资讯投稿を収集し、Sohu の指数・セクター情報と A 株の騰落銘柄数も合わせて、Codex が株価変動理由、市場/セクター/個別株の共振、短期センチメントサイクルを分析するための材料を作ります。この skill は Gemini などの LLM API を呼び出さず、認証情報も読みません。

主な用途：

- A 株の涨停、跌停、炸板、出来高急増の理由を調べる。
- 公告・業績で確認できる材料と、股吧上の思惑を分けて見る。
- 主要指数、業種/テーマ板、騰落銘柄数から、市場全体の共振、セクター主導、個別材料主導を切り分ける。
- 冰点、修复、启动、加速、高潮、退潮の六段階で短期情緒を確認する。

## インストール

リポジトリを任意の場所に clone し、使いたい skill ディレクトリを `~/.codex/skills/` にコピーまたはシンボリックリンクします。

```bash
git clone https://github.com/tsetsugekka/codex-market-skills.git
mkdir -p ~/.codex/skills
ln -s /path/to/codex-market-skills/skills/market-calendar-google ~/.codex/skills/market-calendar-google
ln -s /path/to/codex-market-skills/skills/jp-stock-move-reason ~/.codex/skills/jp-stock-move-reason
ln -s /path/to/codex-market-skills/skills/cn-stock-move-reason ~/.codex/skills/cn-stock-move-reason
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

## セキュリティ

- `market-calendar-google` は、ユーザーが明示的に依頼した場合に Google Calendar コネクタで予定を作成・更新します。
- `jp-stock-move-reason` は公開ページ/API だけを読み取り、token を読まず、外部サービスへ書き込まず、Gemini/OpenAI API も呼び出しません。
- `cn-stock-move-reason` は Eastmoney、Sohu 証券、Tonghuashun 行情センターなどの公開ページ/API だけを読み取り、token を読まず、外部サービスへ書き込まず、Gemini/OpenAI API も呼び出しません。
- 個人のウォッチリスト、認証情報、`.env`、実行キャッシュ、私的な出力はこのリポジトリにコミットしないでください。

## リポジトリ構成

```text
skills/
  market-calendar-google/
    SKILL.md
    README.md
    agents/openai.yaml
  jp-stock-move-reason/
    SKILL.md
    README.md
    scripts/stock_move_sources.py
  cn-stock-move-reason/
    SKILL.md
    README.md
    agents/openai.yaml
    scripts/stock_move_sources.py
```

## 言語

- 中文：`README.md`
- 日本語：`README.ja.md`
- English: `README.en.md`
