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

## インストール

リポジトリを任意の場所に clone し、使いたい skill ディレクトリを `~/.codex/skills/` にコピーまたはシンボリックリンクします。

```bash
git clone https://github.com/tsetsugekka/codex-market-skills.git
mkdir -p ~/.codex/skills
ln -s /path/to/codex-market-skills/skills/market-calendar-google ~/.codex/skills/market-calendar-google
ln -s /path/to/codex-market-skills/skills/jp-stock-move-reason ~/.codex/skills/jp-stock-move-reason
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

## セキュリティ

- `market-calendar-google` は、ユーザーが明示的に依頼した場合に Google Calendar コネクタで予定を作成・更新します。
- `jp-stock-move-reason` は公開ページ/API だけを読み取り、token を読まず、外部サービスへ書き込まず、Gemini/OpenAI API も呼び出しません。
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
```

## 言語

- 中文：`README.md`
- 日本語：`README.ja.md`
- English: `README.en.md`
