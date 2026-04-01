from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .coordinates import BASE_SIZE, level_size, validate_coordinate

INITIAL_REMAINING_PIECES = 70
INITIAL_CURRENT_PLAYER = 1


class Occupant(StrEnum):
    EMPTY = "empty"
    NEUTRAL = "neutral"
    PLAYER1 = "player1"
    PLAYER2 = "player2"


@dataclass(slots=True)
class PlayerState:
    player_id: int
    remaining_pieces: int

    def to_dict(self) -> dict[str, int]:
        return {
            "player_id": self.player_id,
            "remaining_pieces": self.remaining_pieces,
        }

    @classmethod
    def from_dict(cls, data: dict[str, int]) -> "PlayerState":
        return cls(
            player_id=int(data["player_id"]),
            remaining_pieces=int(data["remaining_pieces"]),
        )


@dataclass(slots=True)
class GameState:
    board: list[list[list[Occupant]]]
    players: dict[int, PlayerState]
    current_player: int
    ply_index: int
    game_over: bool
    winner: int | None

    def occupant_at(self, level: int, x: int, y: int) -> Occupant:
        validate_coordinate(level, x, y)
        return self.board[level][y][x]

    def set_occupant(self, level: int, x: int, y: int, occupant: Occupant) -> None:
        validate_coordinate(level, x, y)
        self.board[level][y][x] = occupant

    def is_empty(self, level: int, x: int, y: int) -> bool:
        return self.occupant_at(level, x, y) == Occupant.EMPTY

    def is_occupied(self, level: int, x: int, y: int) -> bool:
        return self.occupant_at(level, x, y) != Occupant.EMPTY

    def clone(self) -> "GameState":
        return GameState(
            board=[[row[:] for row in level_rows] for level_rows in self.board],
            players={
                player_id: PlayerState(
                    player_id=player_state.player_id,
                    remaining_pieces=player_state.remaining_pieces,
                )
                for player_id, player_state in self.players.items()
            },
            current_player=self.current_player,
            ply_index=self.ply_index,
            game_over=self.game_over,
            winner=self.winner,
        )


def _empty_level(level: int) -> list[list[Occupant]]:
    size = level_size(level)
    return [[Occupant.EMPTY for _ in range(size)] for _ in range(size)]


def create_initial_state() -> GameState:
    board = [_empty_level(level) for level in range(BASE_SIZE)]
    center = BASE_SIZE // 2
    board[0][center][center] = Occupant.NEUTRAL
    players = {
        1: PlayerState(player_id=1, remaining_pieces=INITIAL_REMAINING_PIECES),
        2: PlayerState(player_id=2, remaining_pieces=INITIAL_REMAINING_PIECES),
    }
    return GameState(
        board=board,
        players=players,
        current_player=INITIAL_CURRENT_PLAYER,
        ply_index=0,
        game_over=False,
        winner=None,
    )
