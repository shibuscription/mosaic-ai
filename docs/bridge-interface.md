# MOSAIC Python-Node ブリッジ最小 I/O 仕様メモ v0

## 1. 文書の目的

本書は、MOSAIC 学習型 CPU プロジェクトにおいて、Python エンジンと kobalab 側ブリッジを薄い JSON I/O で接続する場合の、最小入出力仕様を整理するための文書である。主目的は、最初の疎通確認を成立させることであり、単一局面を渡して 1 手を返す最小実験を実装しやすくすることにある。

`docs/kobalab-bridge.md` が接続方式の比較整理を扱うのに対し、本書は「Node 温存 + 薄い JSON ブリッジ」を採る場合の、最小インターフェース設計に焦点を当てる。`docs/engine-spec.md`、`docs/data-format.md`、`docs/action-encoding.md` の前提と整合するように、state / action / legal actions / error handling を最低限の範囲で整理する。

本書は最終仕様ではなく、最初の疎通確認に使う暫定仕様メモである。最適化や並列化は先に詰めすぎず、まずは正しく問い合わせできること、ログで追えること、異常系を切り分けられることを優先する。

## 2. 想定する利用シナリオ

本ブリッジが関係する利用シナリオは以下の通りである。

| シナリオ | 目的 | 今回の優先度 |
| --- | --- | --- |
| 単一局面を渡して推奨手を 1 つ返す | 最小疎通確認 | 最優先 |
| Python エンジンから外部プレイヤーとして呼ぶ | 対戦ループへの組み込み | 高い |
| 教師手生成に使う | 模倣学習データ生成 | 高い |
| 評価戦で対戦相手として使う | ベンチマーク比較 | 中程度 |

### 今回の中心

今回は特に以下を成立させることを主眼に置く。

- Python 側から単一局面を渡せること
- kobalab 側が 1 手を返せること
- request / response をログとして追えること
- 成功系と異常系の切り分けができること

## 3. 最小 request の考え方

Python 側から渡す request は、最小疎通確認に必要な情報に絞る。現時点では、少なくとも以下を候補とする。

| 項目 | 内容 | 重要度 |
| --- | --- | --- |
| `format_version` | request 形式の版 | 必須 |
| `request_id` | 問い合わせ識別子 | 必須 |
| `state` | 局面情報または局面交換表現 | 必須 |
| `current_player` | 現在手番のプレイヤー | 必須 |
| `legal_actions` | Python 側で列挙した合法手 | 要検討だが初期は推奨 |
| `debug` | verbose 出力や補足応答の指定 | 任意 |
| `metadata` | 将来拡張用の補助情報 | 任意 |

### `format_version`

- I/O 形式の変更可能性を見越して、最初から持たせる
- 例: `bridge.v0`
- 単純でも version を入れておく価値が高い

### `request_id`

- 疎通確認時のログ追跡に必須
- 同じ request に対応する response を紐付けるために使う
- 将来的には `game_id` や `ply_index` と関連づけてもよいが、最初は独立 ID でもよい

### `state`

- Python エンジン内部表現そのものではなく、bridge 専用の交換表現を渡す前提が望ましい
- 人間が読める JSON 互換構造を優先する
- 最終フィールドは未確定だが、kobalab が意思決定に必要な最小状態を欠かさないことが重要である

### `current_player`

- `state` に含める設計もありうるが、初期は見落としを避けるため明示項目でもよい
- state 内と二重管理する場合は、矛盾検出ができるようにする

### `legal_actions`

- 初期疎通確認では、Python 側で legal actions を列挙して渡す案を第一候補とする
- これにより、kobalab 応答が Python 側の legal set に含まれるか確認しやすい
- 最終的に常に渡すかどうかは未確定である

### `debug`

- 最初の疎通確認では、速度より追跡しやすさを優先する
- `debug: true` のとき補足ログや候補手情報を返せる余地を持たせてもよい
- ただし、最小必須項目には含めない

## 4. 最小 response の考え方

kobalab 側から返す response は、成功か失敗かを判別でき、成功時には選択 action を返せることを最小条件とする。

| 項目 | 内容 | 重要度 |
| --- | --- | --- |
| `format_version` | response 形式の版 | 必須 |
| `request_id` | 対応する request の ID | 必須 |
| `status` | 成功 / 失敗などの状態 | 必須 |
| `selected_action` | 選択された action | 成功時は必須 |
| `error` | エラー情報 | 失敗時は重要 |
| `info` | 補足情報、処理時間、候補手など | 任意 |

### `status`

少なくとも以下のような状態を区別できると扱いやすい。

- `ok`
- `invalid_request`
- `unsupported`
- `timeout`
- `internal_error`

最初から細かくしすぎる必要はないが、成功と失敗を曖昧にしないことが重要である。

### `selected_action`

- `status = ok` の場合に返す
- `docs/action-encoding.md` の保存 / 交換用表現に寄せた JSON 互換構造を前提とする
- 学習用整数 ID ではなく、意味を持つ交換表現で返す方針が自然である

### `error`

- 失敗理由を追えるようにする
- 少なくとも `code` と `message` に相当する情報を持てるとよい
- 例外文字列そのままの丸投げだけにしない方が望ましい

### 将来拡張の余地

将来的には以下を返す可能性がある。

- 候補手一覧
- 評価値
- 処理時間
- legal_actions 不一致の警告

ただし、最初の疎通確認では必須にしない。

## 5. state の受け渡し粒度

### 基本方針

- Python エンジン内部表現をそのまま外に出さない
- bridge 専用の交換表現を持つ
- 初期段階では可読性と追跡しやすさを重視する

### なぜ内部表現をそのまま出さないか

- 内部表現は将来変更される可能性がある
- Python 実装都合が Node 側へ漏れやすい
- ログやサンプルとして保存しにくくなる場合がある

### bridge 専用交換表現の考え方

- JSON 互換であること
- 人間が見て局面の意味を追いやすいこと
- `data-format.md` の局面スナップショット方針と相性が良いこと
- `engine-spec.md` の state シリアライズと整合しやすいこと

### 初期段階の温度感

- 最初から最小バイト数や高速化を追わない
- まずは「欠落なく意味を渡せること」を優先する
- 後で必要になれば、別途軽量化や圧縮を検討する

## 6. action の受け渡し粒度

### 基本方針

- action は学習用整数 ID ではなく、保存 / 交換用表現で受け渡す
- `docs/action-encoding.md` で整理した 3 レイヤーのうち、bridge では交換表現に寄せる

### 最初の疎通確認で重視すること

- 一意に読めること
- JSON 化しやすいこと
- Python 側で legal_actions と照合しやすいこと
- ログに残しても追いやすいこと

### 固定すること / 未確定に残すこと

現時点で固定寄りに扱いたい点:

- bridge では JSON 互換の明示的 action を使う
- `selected_action` は内部 ID ではなく意味を持つ交換表現で返す

未確定として残す点:

- action の最終フィールド定義
- 1 action の自然な粒度
- 可読文字列表現を併記するかどうか

## 7. legal actions の扱い

### 初期方針

最初の疎通確認では、Python 側で legal_actions を計算して request に含める案を第一候補とする。

### 理由

- Python エンジン側の legal_actions をそのまま検証材料として使える
- kobalab の返した action が legal set に含まれるか即座に確認できる
- 異常時に Python 側と kobalab 側の責務を切り分けやすい

### kobalab 側での扱い

- 最初の段階では、渡された legal_actions の中から 1 手を選ぶことを優先してよい
- ただし、kobalab 側が独自に検証可能なら、将来的に不一致検出へ発展させられる

### 将来への接続

- legal_actions は後の action mask 生成の基礎になる
- そのため、bridge で受け渡す action 表現と、学習用 encode の対応関係が後で取れるようにしておく必要がある

### 最初の疎通確認での厳密さ

- まずは legal_actions を渡し、返却 action がその中にあるか確認できれば十分
- Python 側と kobalab 側の完全一致検証までは初回の必須要件にしない

## 8. 異常系とエラー応答

少なくとも以下の異常系を想定する。

| ケース | 例 | response 側で欲しいこと |
| --- | --- | --- |
| 不正な request | 必須項目欠落、形式不正 | `invalid_request` と理由 |
| state 不足 | 局面情報が足りない | 不足項目の明示 |
| action を返せない | legal_actions が空、解釈不能 | `unsupported` などの状態 |
| タイムアウト | 応答が時間内に返らない | `timeout` または呼び出し側で timeout 判定 |
| bridge 側例外 | Node 側内部エラー | `internal_error` と追跡情報 |

### ログに残すべき情報

- `request_id`
- request の要約
- エラー種別
- メッセージ
- 可能なら stack trace 相当の補助情報
- 実行時刻

### 方針

- 異常を黙って補正しない
- 失敗したことと理由を追えることを優先する
- 疎通確認段階では、詳細ログを残す側に倒す

## 9. デバッグしやすさのための要件

### `request_id` の必要性

- request / response 対応付けの軸になる
- 対局ログ、教師手ログ、不具合報告を横断して追いやすい

### 局面再現に必要なログ

- 渡した state
- current_player
- legal_actions
- 返ってきた selected_action
- status

最初の段階では、少なくともこれらを JSON ベースで保存できると再現性が高い。

### JSON の可読性

- compact すぎるバイナリ表現より、まずは人間が追えることを優先する
- 開発初期の不具合切り分けでは特に重要である

### verbose / debug フラグ

- 最初は任意フラグとして持つ余地を残す
- 候補手一覧や処理時間などを返す用途に使える
- ただし、通常系の最小仕様には必須にしない

## 10. format_version と将来拡張

### version フィールドの必要性

- state 交換形式や action 交換形式は今後変わる可能性が高い
- そのため、request / response の両方に `format_version` を持たせる価値がある

### 後方互換の考え方

- 初期段階では完全な後方互換を重く考えすぎない
- ただし、「何が変わったか」を追える形にはしておく
- 将来的な変換や比較のために version を残す

### 将来拡張の例

- 候補手一覧の返却
- 評価値の返却
- 乱数 seed 指定
- 対局単位 request
- 並列処理用メタ情報

最初の疎通確認ではこれらを含めないが、version と任意フィールド領域を持つことで拡張しやすくする。

## 11. 現時点での暫定仕様

最初の疎通確認に必要な最小 I/O は、以下のような構成を暫定仕様とするのが自然である。

### 暫定 request

- `format_version`
- `request_id`
- `state`
- `current_player`
- `legal_actions`
- 任意で `debug`

### 暫定 response

- `format_version`
- `request_id`
- `status`
- 成功時は `selected_action`
- 失敗時は `error`
- 任意で `info`

### この暫定仕様の意図

- 単一局面を渡して 1 手を返す最小実験に必要十分である
- legal_actions と selected_action の整合確認がしやすい
- request_id によりログ追跡しやすい
- 将来拡張を邪魔しない

## 12. 未確定事項

現時点で未確定または要検討の事項は以下の通りである。

- state の最終交換表現
- action の最終交換表現
- legal_actions を常に渡すかどうか
- kobalab 側でも legal 検証するかどうか
- 評価値や候補手一覧を返すか
- timeout を response として返すか、呼び出し側の責務にするか
- 並列実行時の request_id 管理方法
- 対局単位 request を将来どう扱うか

## 13. 次アクション

### 最初の疎通確認でやるべき最小タスク

- 単一局面 request のサンプルを 1 つ作る
- その request に対して `selected_action` を返す最小 response を確認する
- 同一 request を複数回投げて応答が安定するか確認する
- 返却 action が `legal_actions` に含まれるかを確認する
- 異常 request を 1 つ用意し、エラー応答形式を確認する

### 追加であるとよい文書

- `docs/bridge-io-samples.md`
  request / response の具体例集
- `docs/bridge-test-cases.md`
  正常系と異常系の確認項目

本書は最小疎通確認のための暫定仕様である。最初は速度や最適化よりも、request / response を人間が追えること、成功系と異常系を切り分けられること、legal_actions と selected_action の整合を確認できることを優先する。
