from __future__ import annotations

from .coordinates import BASE_SIZE
from .game_state import GameState, Occupant, PlayerState


def state_to_dict(state: GameState) -> dict:
    return {
        "board": {
            "levels": [
                {
                    "level": level,
                    "size": len(level_rows),
                    "cells": [[cell.value for cell in row] for row in level_rows],
                }
                for level, level_rows in enumerate(state.board)
            ]
        },
        "players": [state.players[player_id].to_dict() for player_id in sorted(state.players)],
        "current_player": state.current_player,
        "ply_index": state.ply_index,
        "game_over": state.game_over,
        "winner": state.winner,
    }


def state_from_dict(data: dict) -> GameState:
    level_entries = data["board"]["levels"]
    if len(level_entries) != BASE_SIZE:
        raise ValueError(f"expected {BASE_SIZE} levels, got {len(level_entries)}")

    board: list[list[list[Occupant]]] = []
    for expected_level, level_entry in enumerate(level_entries):
        if int(level_entry["level"]) != expected_level:
            raise ValueError(
                f"unexpected level ordering: expected {expected_level}, got {level_entry['level']}"
            )
        cells = [
            [Occupant(cell) for cell in row]
            for row in level_entry["cells"]
        ]
        board.append(cells)

    players = {
        int(player_data["player_id"]): PlayerState.from_dict(player_data)
        for player_data in data["players"]
    }

    return GameState(
        board=board,
        players=players,
        current_player=int(data["current_player"]),
        ply_index=int(data["ply_index"]),
        game_over=bool(data["game_over"]),
        winner=None if data["winner"] is None else int(data["winner"]),
    )
