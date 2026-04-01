# MOSAIC 主要データ概念例集 v0

## 1. 文書の目的

本書は、MOSAIC 学習型 CPU プロジェクトで扱う主要データの具体例をまとめるための文書である。目的は、抽象的な設計方針だけでなく、「実際に 1 件のデータをどう持つ想定か」を実装者が掴みやすくすることにある。

`docs/data-format.md` がデータ種別と保存方針を整理し、`docs/action-encoding.md` が action 表現を整理し、`docs/bridge-interface.md` が bridge の最小 I/O を整理するのに対し、本書はそれらを横断する概念例集として位置づける。

ルール面は [game-rules-standard.md](/d:/projects/mosaic_ai/docs/game-rules-standard.md)、座標面は [coordinate-system.md](/d:/projects/mosaic_ai/docs/coordinate-system.md)、state の内部的な考え方は [state-representation.md](/d:/projects/mosaic_ai/docs/state-representation.md) を参照する前提とする。本書は、それらを前提にした概念例集であり、仕様本文そのものの代替ではない。

本書は最終確定仕様ではなく、現時点の概念例である。将来そのまま fixture やサンプル JSON のたたき台にできる程度の具体性を持たせるが、未確定部分は未確定として明記する。

## 2. サンプル記述の方針

- 例はできるだけ具体的に書く
- ただし、未確定な state / action 詳細は placeholder や仮名を用いる
- 実装都合で変わりうる点は注記する
- 初期段階では人間可読性を優先した表現を使う
- machine-friendly な最終形と完全一致することを保証しない
- 当面の対象は通常 2人用 7×7 とし、mini / quo / 多人数差分は例の対象外とする
- 位置を示す例は、原則として `level / x / y` を持つ座標系に整合する形で書く

### この文書で特に未確定として扱うもの

- `state` の最終フィールド構造
- `action` の最終フィールド定義
- `legal_actions` を保存するか参照にするか
- `value_target` の具体的な意味
- bridge で返す補足情報の粒度

## 3. 対局メタデータの例

### 概念例

```json
{
  "game_id": "game_2026-04-02_0001",
  "format_version": "game-meta.v0",
  "engine_version": "engine.v0",
  "rule_version": "mosaic.rule.v0",
  "players": [
    {
      "seat": 0,
      "name": "kobalab_cpu",
      "type": "external_cpu",
      "impl": "kobalab",
      "config": {
        "bridge_mode": "json-bridge"
      }
    },
    {
      "seat": 1,
      "name": "python_random",
      "type": "random_player",
      "impl": "python"
    }
  ],
  "start_info": {
    "started_at": "2026-04-02T02:30:00+09:00",
    "seed": 12345,
    "initial_state_source": "default_initial_state"
  },
  "end_info": {
    "ended_at": "2026-04-02T02:31:10+09:00",
    "termination_reason": "normal_end"
  },
  "result": {
    "winner": 0,
    "result_type": "win_loss"
  },
  "notes": "bridge 疎通確認用のサンプル対局"
}
```

### 補足

- この例は通常 2人用 7×7 の対局メタデータを想定している
- `players.config` の中身は未確定である
- `rule_version` と `engine_version` は分けて持つ前提の概念例である
- `result` の詳細表現は今後変更されうる

## 4. 棋譜データの例

### 概念例

```json
{
  "game_id": "game_2026-04-02_0001",
  "format_version": "record.v0",
  "engine_version": "engine.v0",
  "players": [
    { "seat": 0, "name": "kobalab_cpu" },
    { "seat": 1, "name": "python_random" }
  ],
  "result": {
    "winner": 0,
    "result_type": "win_loss"
  },
  "moves": [
    {
      "ply_index": 0,
      "player": 0,
      "action": {
        "action_type": "place_piece",
        "params": {
          "position": { "level": 0, "x": 1, "y": 2 }
        }
      },
      "action_text": "L0(1,2) に通常配置",
      "action_source": "player_choice",
      "state_hash_before": "statehash_0000",
      "state_hash_after": "statehash_0001",
      "resolved_auto_placements": [
        {
          "position": { "level": 1, "x": 1, "y": 2 },
          "owner": 0
        }
      ]
    },
    {
      "ply_index": 1,
      "player": 1,
      "action": {
        "action_type": "place_piece",
        "params": {
          "position": { "level": 0, "x": 2, "y": 2 }
        }
      },
      "action_text": "L0(2,2) に通常配置",
      "action_source": "player_choice"
    }
  ]
}
```

### 補足

- `action_type` や `params` の詳細は未確定である
- 位置は `coordinate-system.md` の `level / x / y` を前提にした概念例へ寄せている
- `moves[].action` は手番で選択した通常配置を表し、自動配置は `resolved_auto_placements` 側で補助的に示している
- `action_text` は人間可読性のための補助項目であり、必須とは限らない
- `state_hash_before/after` は再現や照合のための候補項目である
- `resolved_auto_placements` の持ち方は未確定であり、棋譜本体に含めるかは今後の検討対象である

### machine-friendly との違い

- 人間向けには `action_text` が有用
- 機械向けには構造化 `action` が主となる
- 最終的には両方を持つか、必要に応じて生成するかは未確定

## 5. 局面スナップショットの例

### 概念例

```json
{
  "snapshot_id": "snapshot_game_2026-04-02_0001_ply_12",
  "format_version": "snapshot.v0",
  "engine_version": "engine.v0",
  "source_game_id": "game_2026-04-02_0001",
  "ply_index": 12,
  "state": {
    "board": {
      "levels": [
        {
          "level": 0,
          "size": 7,
          "cells": "未確定: 実際には board[level][y][x] 相当の JSON 互換構造を想定"
        }
      ]
    },
    "players": [
      {
        "seat": 0,
        "remaining_pieces": 41
      },
      {
        "seat": 1,
        "remaining_pieces": 44
      }
    ],
    "current_player": 0,
    "ply_index": 12,
    "game_over": false,
    "winner": null
  },
  "notes": "既知局面テスト候補"
}
```

### 再現用途で最低限ほしいもの

- `snapshot_id`
- `engine_version`
- `state`
- 必要なら `source_game_id`
- 必要なら `ply_index`

### 補足

- `state` は [state-representation.md](/d:/projects/mosaic_ai/docs/state-representation.md) の考え方に寄せた概念例である
- `board.levels[].cells` の最終形は未確定だが、内部では `board[level][y][x]` に近い構造を意識している
- この例は通常 2人用 7×7 の局面を想定している

## 6. 学習サンプルの例

### policy 学習向きの例

```json
{
  "sample_id": "sample_game_2026-04-02_0001_ply_12",
  "format_version": "train-sample.v0",
  "source_game_id": "game_2026-04-02_0001",
  "ply_index": 12,
  "current_player": 0,
  "state": {
    "ref": "snapshot_game_2026-04-02_0001_ply_12"
  },
  "legal_actions": [
    {
      "action_type": "place_piece",
      "params": { "position": { "level": 0, "x": 1, "y": 2 } }
    },
    {
      "action_type": "place_piece",
      "params": { "position": { "level": 1, "x": 2, "y": 1 } }
    }
  ],
  "target_action": {
    "action_type": "place_piece",
    "params": { "position": { "level": 0, "x": 1, "y": 2 } }
  },
  "metadata": {
    "teacher_source": "kobalab_cpu",
    "generation_mode": "imitation_learning"
  },
  "notes": "policy 学習用の最小例。target_action は通常配置として選択された手であり、自動配置連鎖は含めていない"
}
```

### value 学習も視野に入れた例

```json
{
  "sample_id": "sample_game_2026-04-02_0001_ply_12",
  "format_version": "train-sample.v0",
  "source_game_id": "game_2026-04-02_0001",
  "ply_index": 12,
  "current_player": 0,
  "state": {
    "ref": "snapshot_game_2026-04-02_0001_ply_12"
  },
  "target_action": {
    "action_type": "place_piece",
    "params": { "position": { "level": 0, "x": 1, "y": 2 } }
  },
  "final_result": {
    "winner": 0,
    "result_type": "win_loss"
  },
  "value_target": {
    "player_view": 0,
    "target": 1.0,
    "scheme": "win_loss_binary"
  },
  "metadata": {
    "teacher_source": "kobalab_cpu",
    "generation_mode": "imitation_learning_with_result_label"
  }
}
```

### 補足

- `state` を直接持つか `ref` を持つかは未確定である
- `legal_actions` と `action_mask` のどちらを保存するかは未確定である
- `value_target` の意味は最終的な学習方針で変わりうる
- `legal_actions`、`target_action`、`selected_action` は、同じ局面に対する通常配置候補集合とその選択結果として読めるようにするのが望ましい
- ここでの `target_action` は教師が選んだ通常配置であり、自動配置や連鎖結果そのものは別情報として扱う余地がある

## 7. 評価戦結果の例

### 概念例

```json
{
  "evaluation_id": "eval_2026-04-02_model_v1_vs_kobalab",
  "format_version": "evaluation.v0",
  "executed_at": "2026-04-02T03:10:00+09:00",
  "match_config": {
    "game_count": 100,
    "swap_sides": true,
    "seed_base": 5000
  },
  "player_a": {
    "name": "policy_model_v1",
    "type": "learned_model",
    "checkpoint": "ckpt_epoch_05"
  },
  "player_b": {
    "name": "kobalab_cpu",
    "type": "external_cpu",
    "bridge_mode": "json-bridge"
  },
  "summary": {
    "player_a_wins": 42,
    "player_b_wins": 55,
    "draws": 3
  },
  "by_side": {
    "player_a_as_first": { "wins": 24, "losses": 24, "draws": 2 },
    "player_a_as_second": { "wins": 18, "losses": 31, "draws": 1 }
  },
  "artifacts": {
    "game_id_prefix": "eval_2026-04-02_model_v1_vs_kobalab_game_*"
  },
  "notes": "初回ベンチマーク"
}
```

### 補足

- `summary` と `by_side` の細かな形は未確定である
- `artifacts` は個別棋譜への参照を持てれば十分で、形式は固定していない

## 8. bridge request / response の例

### request の最小例

```json
{
  "format_version": "bridge.v0",
  "request_id": "req_game_2026-04-02_0001_ply_12",
  "state": {
    "board": {
      "levels": [
        {
          "level": 0,
          "size": 7,
          "cells": "未確定: bridge 用の局面交換表現"
        }
      ]
    },
    "players": [
      { "seat": 0, "remaining_pieces": 41 },
      { "seat": 1, "remaining_pieces": 44 }
    ],
    "current_player": 0,
    "ply_index": 12
  },
  "current_player": 0,
  "legal_actions": [
    {
      "action_type": "place_piece",
      "params": { "position": { "level": 0, "x": 1, "y": 2 } }
    },
    {
      "action_type": "place_piece",
      "params": { "position": { "level": 1, "x": 2, "y": 1 } }
    }
  ],
  "debug": true
}
```

### response の成功例

```json
{
  "format_version": "bridge.v0",
  "request_id": "req_game_2026-04-02_0001_ply_12",
  "status": "ok",
  "selected_action": {
    "action_type": "place_piece",
    "params": { "position": { "level": 0, "x": 1, "y": 2 } }
  },
  "info": {
    "processing_ms": 4,
    "source": "kobalab_cpu"
  }
}
```

### response の異常例

```json
{
  "format_version": "bridge.v0",
  "request_id": "req_game_2026-04-02_0001_ply_12",
  "status": "invalid_request",
  "error": {
    "code": "missing_state_field",
    "message": "state.board が不足している"
  }
}
```

### 補足

- `state` の bridge 用最終表現は未確定
- `selected_action` は request の `legal_actions` のいずれかと整合する通常配置を返す想定である
- ここでは自動配置や連鎖結果は response 本体に含めていない
- `info` に何をどこまで返すかは未確定である

## 9. どこが未確定か

この文書の例を読む際に、特に未確定として認識しておくべき点は以下である。

| 論点 | 現時点の扱い |
| --- | --- |
| state 表現 | `board` や `players` の最終 JSON 構造は未確定 |
| action 詳細 | `action_type` と `params` の最終フィールドは未確定だが、位置は `level / x / y` 前提に寄せる |
| legal_actions の持ち方 | 常に保存するか、再生成前提にするか未確定 |
| action_mask | 学習サンプルに直接保存するか未確定 |
| value ラベル | 早期に入れるか、どのスキームにするか未確定 |
| bridge 補足情報 | 候補手一覧、評価値、処理時間の必須度は未確定 |
| 自動配置結果の記録 | 棋譜や学習データにどこまで明示的に持つか未確定 |

### この文書の読み方

- 例の形は「だいたいこの粒度で 1 件持つ」という目安として使う
- そのまま最終仕様とみなさない
- fixture 化する際は、`format_version` と未確定項目の整理を併せて行う

## 10. 次アクション

### この文書をもとに fixture 化できるもの

- 対局メタデータの最小 JSON
- 棋譜の 2 手程度のサンプル
- 局面スナップショットの最小 JSON
- policy 学習用サンプルの最小 JSON
- bridge request / response の正常系と異常系サンプル

### 実装前に最小限確定したい項目

- state の最小交換表現
- action の最小交換表現
- 学習サンプルで `state` を直持ちするか参照にするか
- legal_actions を保存するか再生成前提にするか

### 切り出し候補

- `sample-jsons/`
  実際の fixture 候補を置くディレクトリ
- `docs/bridge-io-samples.md`
  bridge request / response の具体例を拡充した文書
- `docs/action-examples.md`
  action のケース別具体例集

本書は、設計文書群の橋渡しとしての概念例集である。今後、state や action の最終仕様が詰まった段階で更新するが、現時点でも実装者が fixture やサンプル JSON を作り始める下敷きとして利用できることを意図している。
