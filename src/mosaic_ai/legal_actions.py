from __future__ import annotations

from dataclasses import dataclass

from .coordinates import BASE_SIZE, level_size
from .game_state import GameState


@dataclass(frozen=True, slots=True)
class PlaceAction:
    level: int
    x: int
    y: int
    action_type: str = "place"

    def to_dict(self) -> dict[str, int | str]:
        return {
            "action_type": self.action_type,
            "position": {
                "level": self.level,
                "x": self.x,
                "y": self.y,
            },
        }


def has_support(state: GameState, level: int, x: int, y: int) -> bool:
    if level <= 0:
        return True
    below = level - 1
    return (
        state.is_occupied(below, x, y)
        and state.is_occupied(below, x + 1, y)
        and state.is_occupied(below, x, y + 1)
        and state.is_occupied(below, x + 1, y + 1)
    )


def legal_actions(state: GameState) -> list[PlaceAction]:
    actions: list[PlaceAction] = []
    for level in range(BASE_SIZE):
        size = level_size(level)
        for y in range(size):
            for x in range(size):
                if not state.is_empty(level, x, y):
                    continue
                if level > 0 and not has_support(state, level, x, y):
                    continue
                actions.append(PlaceAction(level=level, x=x, y=y))
    return actions
