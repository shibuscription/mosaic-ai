# MOSAIC Phase 1 実装計画書

## 1. 文書の目的

本書は、MOSAIC 学習型 CPU プロジェクトにおける Phase 1 の実装計画を整理するための文書である。目的は、実装そのものに入る前に、Phase 1 で何を作るか、何をまだ作らないか、どの順序で進めるかを明確にし、Codex や他 AI を含む実装担当がブレずに作業を進められる状態を作ることにある。

ルートの `README.md` が全体ロードマップの入口、`docs/game-rules-standard.md` が通常 2人用 7×7 のルール一次資料、`docs/engine-spec.md` がエンジン責務整理、本書がその Phase 1 実装計画という役割分担を前提とする。

本書は Phase 1 専用の計画書であり、kobalab 連携、学習スクリプト、評価リーグなどの後続フェーズは主対象としない。

## 2. Phase 1 の到達目標

Phase 1 の到達目標は、通常 2人用 7×7 MOSAIC に対して、Python エンジンの最小実装基盤を正しく動かせる状態にすることである。

少なくとも以下を満たすことを目標とする。

- 通常 2人用 7×7 の初期局面を正しく生成できる
- 座標系に基づいた state を保持できる
- legal actions を列挙できる
- 通常配置を適用できる
- 自動配置と連鎖を deterministic に解決できる
- 終局判定ができる
- シリアライズと最低限の再現テストがある

### Phase 1 の成果物イメージ

- Python エンジンの最小実装
- ルール準拠の legal_actions / apply_action / terminal 判定
- 最低限のユニットテストと既知局面テストの土台
- 次フェーズで kobalab 連携やデータ生成に進めるだけの安定基盤

## 3. Phase 1 のスコープ内

Phase 1 で扱うものは以下の通りである。

- Python エンジン最小実装
- 通常 2人用 7×7 に限定したルール準拠の盤面処理
- 座標系と state 雛形
- 初期局面生成
- legal actions 列挙
- 通常配置適用
- 最小正方形判定
- 自動配置判定
- 連鎖処理
- 終局判定
- 最低限のシリアライズ
- 最低限のテスト
- デバッグしやすい基本構造

## 4. Phase 1 のスコープ外

Phase 1 では以下を主対象にしない。

- kobalab bridge 実装
- 学習スクリプト
- ニューラルネット推論
- 模倣学習 / 強化学習本体
- 評価リーグ
- UI / GUI
- 高度な最適化
- mini / quo / 多人数対応

### 方針

- まずは通常 2人用 7×7 を正しく動かす最小実装を優先する
- 性能改善や機能拡張は、正しい盤面処理が安定した後に進める

## 5. 実装順序

Phase 1 の推奨実装順序は以下の通りである。

### Step 1: 基本データ構造と座標系

目的:

- `docs/coordinate-system.md` と `docs/state-representation.md` に沿った基盤を作る

やること:

- 座標ユーティリティの用意
- level ごとのサイズ計算
- 位置検証の基礎
- `GameState` の最小雛形

### Step 2: 初期局面生成と state シリアライズ

目的:

- 初期局面を安定して生成し、保存・表示できるようにする

やること:

- 通常 2人用 7×7 の初期状態生成
- 中央中立コマの配置
- プレイヤー残り駒数の初期化
- state の辞書化 / JSON 向け変換

### Step 3: legal actions 列挙

目的:

- 現局面で置ける通常配置候補を正しく列挙する

やること:

- 最下層の空き位置列挙
- 直下 4 点支持がある上層空き位置の列挙
- 走査順の deterministic 化

### Step 4: 通常配置の適用

目的:

- プレイヤーが選ぶ通常配置 1 手を state に適用できるようにする

やること:

- action 検証
- 通常配置反映
- 残り駒数更新
- 手番進行前の着手後処理入口整備

### Step 5: 自動配置判定と連鎖処理

目的:

- 通常配置後に起こる最小正方形判定、自動配置、連鎖を正しく解決する

やること:

- 最小正方形候補走査
- 中立コマを含む条件判定
- 上層自動配置
- 下層から上層、同一層では左上から右下への deterministic 解決

### Step 6: 終局判定

目的:

- 連鎖解決後に終局と勝者を正しく確定できるようにする

やること:

- 持ちコマ置き切り判定
- `game_over` / `winner` 更新
- 追加 action を受け付けない制御

### Step 7: テスト拡充

目的:

- Phase 1 実装を安心して次フェーズへ渡せる状態にする

やること:

- 初期局面テスト
- legal actions テスト
- 通常配置反映テスト
- 自動配置 / 連鎖テスト
- シリアライズ往復テスト
- 既知局面テスト

## 6. 初期ファイル構成案

以下は Phase 1 を進めやすくするための初期案であり、最終確定ではない。

| パス案 | 役割 |
| --- | --- |
| `src/engine/coordinates.py` | 座標系、level サイズ、位置検証 |
| `src/engine/game_state.py` | state 定義、初期化補助 |
| `src/engine/serialization.py` | state の辞書化、JSON 向け変換 |
| `src/engine/legal_actions.py` | legal actions 列挙 |
| `src/engine/apply_action.py` | 通常配置適用 |
| `src/engine/auto_placement.py` | 最小正方形判定、自動配置、連鎖 |
| `src/engine/termination.py` | 終局判定、勝者判定 |
| `src/engine/__init__.py` | 公開 API まとめ |
| `tests/test_coordinates.py` | 座標系テスト |
| `tests/test_initial_state.py` | 初期局面テスト |
| `tests/test_legal_actions.py` | legal actions テスト |
| `tests/test_apply_action.py` | 通常配置テスト |
| `tests/test_auto_placement.py` | 自動配置・連鎖テスト |
| `tests/test_termination.py` | 終局判定テスト |
| `tests/test_serialization.py` | シリアライズ往復テスト |
| `docs/` | 既存設計文書群 |

## 7. 各ファイルの責務案

### `game_state`

- `GameState` の定義
- 初期値セットアップの補助
- プレイヤー状態と盤面状態の保持

### `coordinates`

- `level / x / y` の検証
- `size(level)` 計算
- 最上段判定
- 2×2 左上基準の補助

### `rules / auto_placement`

- 最小正方形判定
- 同色条件判定
- 中立コマを含む場合の扱い
- 連鎖解決

### `serialization`

- state の辞書変換
- JSON 向け整形
- テスト fixture 向けの安定表現

### `legal_actions`

- 通常配置候補の列挙
- 順序の deterministic 化
- 不正位置除外

### `apply_action`

- action 検証
- 通常配置反映
- 自動配置処理への受け渡し

### `termination`

- 終局判定
- 勝者確定
- 終局後 action を禁止する制御補助

### `tests`

- 各責務ごとの単体テスト
- 既知局面テスト
- 再現性テスト

## 8. 先に書くべきテスト

Phase 1 では、実装と同じくらいテストの順序も重要である。少なくとも以下を優先する。

| テスト | 確認内容 |
| --- | --- |
| 初期局面の正しさ | 中央中立コマ、残り駒数、手番が正しいか |
| legal actions の件数と中身 | 初期局面での候補数と位置が正しいか |
| 通常配置後の state 変化 | 指定位置に配置され、残り駒数が減るか |
| 自動配置発生ケース | 3 同色 / 4 同色で自動配置が起こるか |
| 中立コマを含むケース | 中立を含む最小正方形条件が正しく判定されるか |
| 連鎖の deterministic 再現 | 同じ局面・同じ着手で同じ連鎖順になるか |
| 終局判定 | 持ちコマ置き切りを正しく検出できるか |
| シリアライズ往復 | 保存・読込で同じ state を再現できるか |

### 実装順との関係

- Step 1-2 の段階で `test_coordinates` と `test_initial_state` を先に用意する
- Step 3 で `test_legal_actions`
- Step 4-5 で `test_apply_action` と `test_auto_placement`
- Step 6-7 で `test_termination` と `test_serialization`

## 9. commit の粒度案

Phase 1 では、1 テーマ 1 コミットを基本にするのが望ましい。

### おすすめのまとまり

1. 座標系と基本データ構造
2. 初期局面生成とシリアライズ雛形
3. legal actions 列挙
4. 通常配置適用
5. 自動配置と連鎖処理
6. 終局判定
7. テスト拡充と整理

### commit 粒度の考え方

- 1 回の commit で責務が 1 つに絞られていること
- テストが通る区切りで commit すること
- 連鎖処理のような重い実装は、必要なら判定部と解決部を分けてもよい

## 10. Phase 1 完了条件

Phase 1 は、以下を満たした時点で完了とみなす。

- 通常 2人用 7×7 の初期局面が正しく生成できる
- legal actions がルール文書と整合している
- 通常配置、自動配置、連鎖処理が deterministic に動く
- 終局判定と勝者確定が行える
- state をシリアライズできる
- 最低限のテストが存在し、主要ケースをカバーしている
- `README.md`、`docs/game-rules-standard.md`、`docs/engine-spec.md`、`docs/coordinate-system.md`、`docs/state-representation.md`、`docs/action-encoding.md` と矛盾しない

### 次フェーズへ渡せる状態

- kobalab 連携前の単体エンジンとして信頼できる
- bridge やデータ生成に必要な state / action / legal_actions の基盤が揃っている
- fixture や既知局面テストを増やしやすい構造になっている

## 11. 次アクション

この計画書の次に着手すべき最初の実装タスクは、**Step 1: 基本データ構造と座標系** である。

### 最初の実装依頼の位置づけ

Codex に最初に投げる実装依頼としては、以下の範囲が適切である。

- `src/engine/coordinates.py`
- `src/engine/game_state.py`
- `tests/test_coordinates.py`
- `tests/test_initial_state.py` の雛形または最小ケース

### この順序にする理由

- 以後の legal actions、apply_action、自動配置処理のすべてが座標系と state 雛形に依存するため
- 最初に土台を固定すると、後続実装の手戻りを減らしやすい

本書は Phase 1 の実務用計画書であり、実装開始後に必要に応じて更新する。ただし、通常 2人用 7×7 を正しく動かす最小実装を優先し、Phase 1 では kobalab 連携や学習本体へ踏み込みすぎないという方針は維持する。
