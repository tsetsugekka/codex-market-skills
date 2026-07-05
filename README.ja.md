# Codex Market Skills

<p align="center">
  <strong>取引、投資リサーチ、市場変動分析、市場カレンダー管理のための Codex Skill Suite。</strong>
</p>

<p align="center">
  <a href="README.md">中文</a> |
  <a href="README.en.md">English</a> |
  <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <code>Codex Skill</code> · <code>CN / JP / US Markets</code> · <code>Public-safe</code> · <code>No secrets</code>
</p>

---

> 取引、投資リサーチ、市場変動分析、市場カレンダー管理のための Codex Skill Suite。

![Codex](https://img.shields.io/badge/Codex-Skill%20Suite-4f46e5)
![Markets](https://img.shields.io/badge/Markets-CN%20%7C%20JP%20%7C%20US-22c55e)
![Language](https://img.shields.io/badge/Language-日本語-blue)
![Secrets](https://img.shields.io/badge/Secrets-not%20included-critical)

## これは何か

Codex Market Skills は、取引、投資リサーチ、市場カレンダー管理のための Codex skills 集です。複数の市場関連 skill を同じ GitHub リポジトリで管理し、それぞれを独立してインストール・保守できます。

主に 4 つの作業領域をカバーします。

| 領域 | 対象 |
| --- | --- |
| 個別株の変動理由 | A 株、日本株、米国株/ETF の上昇、下落、出来高急増、涨停、寄り前・引け後変動 |
| テーマとセンチメント | A 株テーマ強弱、短期情緒サイクル、掲示板/フォーラム/コミュニティ温度、主線、期待差 |
| マクロと構造 | マクロ速報、大局 tape、テクニカル構造、支持・抵抗、gamma/GEX、0DTE シナリオ表 |
| カレンダーとレポート | 米国/日本株決算、マクロイベント、中央銀行イベント、市場戦略、引け後レビュー |

## Skill 一覧

| Skill | 用途 | 主な依存 |
| --- | --- | --- |
| [`market-calendar-google`](docs/market-calendar-google.md) | 決算、マクロ指標、中央銀行イベント、入札などを整理し Google Calendar に追加 | 必須：`google-calendar:google-calendar` |
| [`jp-stock-move-reason`](docs/jp-stock-move-reason.md) | 日本株の急騰、急落、出来高急増、ニュース/掲示板材料を分析 | なし |
| [`cn-stock-move-reason`](docs/cn-stock-move-reason.md) | A 株の涨停、跌停、炸板、出来高急増、市場/セクター/個別株共振を分析 | 任意：`mx-data`、`mx-search`、`mx-xuangu`、`mx-zixuan` |
| [`cn-theme-strength-mx`](docs/cn-theme-strength-mx.md) | ローカル A 株テーママッピングの TOP10/BOTTOM10 強弱ランキングを盤中計算 | 必須：`mx-zixuan`、`mx-xuangu`、`mx-search` |
| [`stock-sentiment-analysis`](docs/stock-sentiment-analysis.md) | 他の株式 skill で再利用する公開安全なセンチメント分析フレームワーク | 任意：Eastmoney Miaoxiang、moomoo コミュニティサンプル |
| [`macro-news-check`](docs/macro-news-check.md) | 個別株、指数、テクニカル、gamma 分析で必要な場合にマクロ/大局背景を確認 | なし |
| [`market-daily-strategist`](docs/market-daily-strategist.md) | 米国株、日株、A 株の寄り前戦略、引け後レビュー、長期単銘柄推薦を作成 | 任意：市場データ、変動理由、テクニカル、情緒、gamma skill |
| [`us-stock-move-reason`](docs/us-stock-move-reason.md) | moomoo ニュース、要約、コミュニティ、資金、オプション、テクニカル異常で米国株/ETF 変動を分析 | 任意推奨：moomoo 系 skill |
| [`us-stock-gamma-moomoo`](docs/us-stock-gamma-moomoo.md) | moomoo OpenD で米国オプション gamma/GEX、gamma wall、0DTE シナリオ表を分析 | 必須：ローカル moomoo OpenD、Python SDK `moomoo` |
| [`stock-technical-analysis`](docs/stock-technical-analysis.md) | 米国株、日本株、A 株のテクニカル構造、支持・抵抗、出来高、指標を分析 | 任意：Eastmoney Miaoxiang、`moomoo-technical-anomaly` |

## 特徴

- **複数市場を一つの suite で管理**  
  A 株、日本株、米国株、ETF、指数、決算カレンダー、マクロイベント、オプション構造を同じリポジトリに置きつつ、各 skill の責務は分離しています。

- **公開安全な設計**  
  汎用ワークフロー、公開安全なルール、スクリプトだけを保存します。ウォッチリスト、認証情報、API key、`.env`、private RAG、実行キャッシュ、私的出力は含めません。

- **証拠優先の市場リサーチ**  
  確認済み材料、市場の思惑、掲示板熱量、チャート確認、マクロ増幅要因、背景ノイズを分けて考えます。

- **組み合わせて使える構成**  
  変動理由、情緒サイクル、マクロ tape、テクニカル分析、gamma 構造を必要に応じて組み合わせられます。

- **中国語レポート優先**  
  デフォルトは中国語の取引リサーチと盤中判断向けです。英語・日本語 README はインストールと公開説明の補助です。

## どの Skill を使うか

| 質問の意図 | 推奨 skill |
| --- | --- |
| 「この A 株はなぜ涨停/跌停/炸板した？」 | `cn-stock-move-reason` |
| 「この日株はニュース材料か掲示板の思惑か？」 | `jp-stock-move-reason` |
| 「この米国株はなぜ寄り前/引け後に動いた？」 | `us-stock-move-reason` |
| 「今日の A 株で強い/弱いテーマは？」 | `cn-theme-strength-mx` |
| 「この株は主線启动、高潮分歧、退潮反発のどれ？」 | `stock-sentiment-analysis` |
| 「マクロや大局要因がある？」 | `macro-news-check` |
| 「今のテクニカルはどう見える？」 | `stock-technical-analysis` |
| 「SPX/SPY/個別株の option gamma は？」 | `us-stock-gamma-moomoo` |
| 「寄り前戦略や引け後レビューを書いて。」 | `market-daily-strategist` |
| 「今週の決算と市場イベントをカレンダーに入れて。」 | `market-calendar-google` |

## Skill 詳細

<details>
<summary><code>market-calendar-google</code> - 市場カレンダー</summary>

米国株決算、日本株決算、中国・米国・日本のマクロ指標、中央銀行イベント、国債入札、その他の重要市場イベントを整理し、ユーザーのルールに従って Google Calendar に追加します。

依存：必須 - `google-calendar:google-calendar`。

連携 skill：なし。

主な用途：

- Earnings Whispers の今週または来週の米国決算画像を整理する。
- ウォッチリストに基づいて米国株・日本株決算を絞り込む。
- 中国・米国・日本の重要度が高い経済イベントを整理する。
- ユーザーのローカル時間で Google Calendar に登録し、重複を避ける。

</details>

<details>
<summary><code>jp-stock-move-reason</code> - 日株変動理由</summary>

入力された日本株コードについて、Yahoo Finance のリアルタイム株価欄、Yahoo 掲示板、Yahoo/Kabutan/Traders のニュース、基本指標を収集し、Codex が株価変動理由を分析するための材料を作ります。

依存：なし。

連携 skill：`stock-sentiment-analysis`、`macro-news-check`、`stock-technical-analysis`。

主な用途：

- 日本株の急騰、急落、出来高急増の理由を調べる。
- ニュースで確認できる材料と、掲示板上の思惑を分けて見る。
- 現在の騰落率、時価総額、PER/PBR、信用倍率、掲示板の温度感を確認する。

</details>

<details>
<summary><code>cn-stock-move-reason</code> - A 株変動理由</summary>

入力された単一の A 株コードについて、Eastmoney の公開株価データ、公告、股吧/资讯投稿を収集し、Sohu の指数・セクター情報と A 株の騰落銘柄数も合わせて、Codex が株価変動理由、市場/セクター/個別株の共振、短期センチメントサイクルを分析するための材料を作ります。

依存：任意 - `mx-data`、`mx-search`、`mx-xuangu`、`mx-zixuan`（Eastmoney Miaoxiang 強化）。

連携 skill：`stock-sentiment-analysis`、`macro-news-check`、`stock-technical-analysis`。

主な用途：

- A 株の涨停、跌停、炸板、出来高急増の理由を調べる。
- 公告・業績で確認できる材料と、股吧上の思惑を分けて見る。
- 主要指数、業種/テーマ板、騰落銘柄数から、市場全体の共振、セクター主導、個別材料主導を切り分ける。
- 冰点、修复/潜伏、启动、加速、高潮、高位分歧/分化、退潮の七段階で短期情緒を確認する。

</details>

<details>
<summary><code>cn-theme-strength-mx</code> - A 株テーマ強弱</summary>

ローカル A 株テーママッピングキャッシュと中国語テーマラベルを読み、Eastmoney Miaoxiang の自選株と選股インターフェースで A 株の盤中または直近取引日の行情を取得し、マッピング重みに基づいてテーマ加重騰落率を計算します。中国語テーマ名で TOP10 と BOTTOM10 を出力し、TOP3 テーマからそれぞれ上昇率が最も高い代表株を 1 つ選び、股吧手がかりと Miaoxiang ニュースでテーマ変動理由を補助的に判断します。盤中利用を前提に、自選接口のカバー数、残り補完数、補完バッチ進捗、限頻 retry、最終補完状況をリアルタイムに報告します。

依存：必須 - `mx-zixuan`、`mx-xuangu`、`mx-search`；任意 - `mx-data`（財務やバリュエーションの追加確認）。

連携 skill：`cn-stock-move-reason`。

主な用途：

- 盤中にローカル A 株テーママッピングで強いテーマ、弱いテーマを確認する。
- Eastmoney 自選株で素早く行情を取得し、自選接口にないテーマ成分を Miaoxiang 選股で補完する。
- 板名や単一銘柄ではなく、テーマ重みに基づいて A 株テーマ強弱を出す。
- 回答には TOP10、BOTTOM10、TOP3 テーマ駆動確認を表示し、デフォルトではファイルを書かない。

</details>

<details>
<summary><code>stock-sentiment-analysis</code> - センチメントフレームワーク</summary>

A 株、日本株、米国株、指数、セクターテーマに共通して使える、公開安全なセンチメント分析フレームワークです。情緒サイクル、主線/フォロワー、期待差、掲示板/フォーラムの温度感、混雑取引、クロスマーケットの risk-on/risk-off を整理し、private RAG の中身を公開リポジトリに持ち込みません。

依存：任意 - `mx-data`、`mx-search`、`mx-xuangu`（A 株証拠、テーマ成分、選股強化）；`mx-zixuan`（ユーザーが自選株タスクを明示した場合のみ）；`moomoo-comment-sentiment`（米国株コミュニティサンプル強化）。

連携 skill：`cn-stock-move-reason`、`jp-stock-move-reason`、`us-stock-move-reason`、`stock-technical-analysis`、`us-stock-gamma-moomoo`。

主な用途：

- フォーラム/掲示板の熱量、ニュースの期待差、需給の広がり、チャート確認を統合し、センチメント結論を作る。
- 複数の変動理由、テクニカル、gamma skill に共通の情緒フレームを提供する。
- ユーザーが private RAG ディレクトリを指定した場合、テーマ、ソース別名、ページ/slide 範囲、キーワード、公開安全な要約だけを持つローカル索引作成を案内する。private 原資料はこの公開リポジトリに書かない。

</details>

<details>
<summary><code>macro-news-check</code> - マクロ速報確認</summary>

他の市場 skill から呼び出すマクロ速報チェック用 skill です。個別株、指数、テクニカル、gamma 分析で現在のマクロ/大局背景が本当に必要な場合だけ使います。ユーザーが大局、マクロ、クロスアセット、リスク情緒の影響を聞けば、公開速報と市場確認ソースを自動で選びます。

依存：なし。

連携 skill：なし。

主な用途：

- 金利、為替、中央銀行、経済指標、商品、地政学、広い risk-on/risk-off が個別株や指数に影響しているかを確認する。
- `cn-stock-move-reason`、`jp-stock-move-reason`、`stock-technical-analysis`、`us-stock-gamma-moomoo` にマクロ tape を提供する。
- 関連する 2-5 件の速報を、主因、二次的な増幅要因、または背景ノイズとして整理する。

</details>

<details>
<summary><code>market-daily-strategist</code> - 市場戦略レポート</summary>

米国株、日本株、A 株向けの中国語市場戦略レポートのルーティング層です。寄り前戦略、引け後レビュー、単一銘柄の長期推薦を扱い、ユーザー意図に応じて市場・時間帯別 reference を読み、マクロ、変動理由、情緒サイクル、テクニカル構造、利用可能なローカル行情ツールを意思決定向けレポートに圧縮します。

依存：任意 - `mx-data`、`mx-search`、`mx-xuangu`（A 株行情、ニュース、板/概念成分強化）；`mx-zixuan`（ユーザーが自選株タスクを明示した場合のみ）；公式 moomoo ニュース、要約、コメント、資金、オプション、テクニカル異常 skill（米国株レポート強化）。

連携 skill：`macro-news-check`、`stock-sentiment-analysis`、`stock-technical-analysis`、`cn-stock-move-reason`、`jp-stock-move-reason`、`us-stock-move-reason`、`us-stock-gamma-moomoo`。

主な用途：

- 米国株、日本株、A 株の寄り前戦略を書く。
- 米国株、日本株、A 株の引け後レビューを書く。
- 米国株、日本株、A 株/ETF/LOF を 1 つ推薦し、買い場、リスク、検証条件を出す。

</details>

<details>
<summary><code>us-stock-move-reason</code> - 米国株変動理由</summary>

公式 moomoo のニュース、銘柄ダイジェスト、コミュニティ感情、資金異常、オプション異常、テクニカル異常と、このリポジトリの gamma・テクニカル・マクロ skill を組み合わせ、米国株や ETF の変動理由を分析する skill です。

依存：任意推奨 - `moomoo-news-search`、`moomoo-stock-digest`、`moomoo-comment-sentiment`、`moomoo-capital-anomaly`、`moomoo-derivatives-anomaly`、`moomoo-technical-anomaly`；任意 - ローカル moomoo OpenD と Python SDK。

連携 skill：`us-stock-gamma-moomoo`、`stock-technical-analysis`、`stock-sentiment-analysis`、`macro-news-check`。

主な用途：

- DELL、NVDA、TSLA などの米国株が急騰、急落、寄り前ギャップ、引け後に動いた理由を調べる。
- 決算、ガイダンス、格付け、受注、ニュースで確認できる材料とコミュニティ上の思惑を分ける。
- 米国株に適用できるオプション大口、IV、オプション感情、資金フロー、空売り、テクニカル異常を確認する。
- SPY/QQQ/SPX 関連の動きについて、マクロ、テクニカル、オプション/gamma 構造を統合する。

</details>

<details>
<summary><code>us-stock-gamma-moomoo</code> - オプション Gamma 構造</summary>

moomoo OpenD から米国株・米国オプションデータを取得し、Codex が gamma/GEX、gamma wall、gamma flip、SPX/SPY/ES の日中構造、0DTE オプションのシナリオ価格表を分析するための skill です。ローカルで moomoo OpenD が起動している必要があり、環境がない場合は先にインストールまたは起動を案内します。

依存：必須 - ローカル moomoo OpenD、Python SDK `moomoo`；任意 - `moomoo-derivatives-anomaly`（米国オプション異常、大口、IV、PCR、オプション感情スキャン）。

連携 skill：`macro-news-check`、`stock-technical-analysis`、`stock-sentiment-analysis`、`us-stock-move-reason`。

主な用途：

- 通常の米国株または米国 ETF のオプション gamma 構造を分析し、必要に応じて公式 moomoo のオプション異常、大口、IV、PCR、オプション感情も補助的に確認する。
- `.SPX`/SPXW の指数オプション構造を分析する。指数データやチェーンが直接取れない場合は、SPY オプション、ES/CFD、またはユーザー提供の指数アンカーで換算し、プロキシを明示する。
- 0DTE call/put について、時間 x 原資産価格の理論価値表を作り、回復、利確、損切り水準を検討する。
- 文字の結論、箇条書き、テキスト表を中心に出力する。同じ会話内で日中に繰り返し質問された場合は、その日の過去の gamma 結果と比べて水準の移動や強弱を判断する。

</details>

<details>
<summary><code>stock-technical-analysis</code> - テクニカル分析</summary>

米国株、日本株、A 株のテクニカル構造を分析する skill です。日中トレンド、支持・抵抗、出来高と価格、KDJ/MACD/RSI、Vegas チャネル、チャート読解、特定価格に到達できるかの判断に使います。

依存：任意 - `mx-data`、`mx-search`、`mx-xuangu`（A 株行情、ニュース、板/概念成分、テクニカル選股強化）；`mx-zixuan`（ユーザーが自選株タスクを明示した場合のみ）；`moomoo-technical-anomaly`（米国株公式テクニカル異常スキャン）。

連携 skill：`macro-news-check`、`stock-sentiment-analysis`、`cn-stock-move-reason`、`jp-stock-move-reason`、`us-stock-move-reason`、`us-stock-gamma-moomoo`。

主な用途：

- 強トレンド継続、高値圏保ち合い、押し目確認、ブレイク失敗、ダイバージェンス、破位反発などを分類する。
- touch、break、tradable hold を区別し、一本のヒゲを有効ブレイクと誤認しない。
- moomoo/Yahoo/証券アプリのチャートやスクリーンショットから、現在値、構造、出来高・モメンタム、実行上の意味、次の確認点を読む。
- 日株/A 株の変動理由や米国 gamma skill と組み合わせ、材料をチャートが確認しているかを判断する。
- 米国株では公式テクニカル異常を一次ヒントにし、最終判断はトレンド位置、VWAP/移動平均、出来高・価格、モメンタム divergence、支持・抵抗、失敗ブレイクで行う。

</details>

## インストール

Codex にリポジトリ URL を送り、必要な skill をインストールするよう依頼します。

```text
https://github.com/tsetsugekka/codex-market-skills から必要な Codex skills をインストールしてください。
```

1 つだけ必要な場合は、`stock-technical-analysis` や `cn-theme-strength-mx` のように skill 名も指定します。

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
現在の A 株テーマ強弱を見て、TOP10 と BOTTOM10 を表示して。
```

```text
盤中で A 株のどのテーマが強く、どのテーマが弱いか見て。
```

```text
この株は主線の立ち上がり、高潮後の分岐、それとも退潮反発なのか見て。
```

```text
この株に今日、大局やマクロ材料の影響があるか確認して。
```

```text
今日の A 株引け後レビューを書いて。主線、明日のリスク、操作可能な方向を重視して。
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

## セキュリティ境界

- `market-calendar-google` は、ユーザーが明示的に依頼した場合に Google Calendar コネクタで予定を作成・更新します。
- `jp-stock-move-reason` は公開ページ/API だけを読み取り、token を読まず、外部サービスへ書き込まず、Gemini/OpenAI API も呼び出しません。
- `cn-stock-move-reason` は Eastmoney、Sohu 証券などの公開ページ/API だけを読み取り、token を読まず、外部サービスへ書き込まず、Gemini/OpenAI API も呼び出しません。
- `cn-theme-strength-mx` は Eastmoney Miaoxiang `mx-zixuan` と `mx-xuangu` を使います。テーマ強弱/自選関連ワークフローをユーザーが依頼した場合だけ自選株を読み、自動で追加・削除・変更せず、`MX_APIKEY`、完全な自選株リスト、ローカルテーママッピングキャッシュ、原始 API 応答、実行キャッシュをコミットしません。
- `stock-sentiment-analysis` は公開安全な汎用センチメント規則だけを保存します。private RAG、個人ラベル、原始ノート、スクリーンショット、取引ログはコミットしないでください。
- `macro-news-check` は公開マクロ速報ページ/Feed/エンドポイントだけを読み取り、login cookie、token、口座データ、private research material を読みません。長いニュース本文をコピーしないでください。
- `market-daily-strategist` はレポートのルーティングと統合層です。ローカル/私的行情ツールは任意の強化要素であり、個人ウォッチリスト、私的出力、ツールキャッシュを公開リポジトリに入れないでください。
- `us-stock-move-reason` は公開安全な米国株変動理由ワークフローだけを保存します。公式 moomoo skill と OpenD は実行時のデータ層であり、口座データ、OpenD ログ、コミュニティの生データ、私的出力、個人の取引記録はコミットしないでください。
- `us-stock-gamma-moomoo` はローカルの moomoo OpenD の行情インターフェースを使い、取引ロック解除 API は呼び出しません。公開版は private RAG に依存せず、個人口座情報、OpenD ログ、スクリーンショット、私的な行情出力、独自戦略名、私的な人名/handle はコミットしないでください。
- `stock-technical-analysis` は汎用テクニカル分析ルールだけを保存します。公開版は private RAG に依存せず、個人ポジション、売買計画、スクリーンショット原本、私的な研究パス、専有指標名、独自戦略名、私的な人名/handle はコミットしないでください。
- 個人のウォッチリスト、認証情報、API key、`.env`、private RAG、実行キャッシュ、私的な出力はこのリポジトリにコミットしないでください。

## リポジトリ構成

```text
skills/
  market-calendar-google/
    SKILL.md
    agents/openai.yaml
  jp-stock-move-reason/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    scripts/stock_move_sources.py
  cn-stock-move-reason/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    scripts/stock_move_sources.py
  cn-theme-strength-mx/
    SKILL.md
    agents/openai.yaml
    scripts/
  stock-sentiment-analysis/
    SKILL.md
    agents/openai.yaml
    references/experience.md
    references/sentiment-framework.md
  macro-news-check/
    SKILL.md
    agents/openai.yaml
  market-daily-strategist/
    SKILL.md
    references/
  us-stock-move-reason/
    SKILL.md
    agents/openai.yaml
  us-stock-gamma-moomoo/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/gamma_report.py
    scripts/option_scenario_table.py
  stock-technical-analysis/
    SKILL.md
    agents/openai.yaml
    references/
docs/
  market-calendar-google.md
  jp-stock-move-reason.md
  cn-stock-move-reason.md
  cn-theme-strength-mx.md
  macro-news-check.md
  market-daily-strategist.md
  stock-sentiment-analysis.md
  us-stock-move-reason.md
  us-stock-gamma-moomoo.md
  stock-technical-analysis.md
shared/
  references/release-and-privacy.md
```

## 言語

- 中文：`README.md`
- English: `README.en.md`
- 日本語：`README.ja.md`
