from __future__ import annotations

from dataclasses import dataclass

BASE_SIZE = 7
MAX_LEVEL = BASE_SIZE - 1


@dataclass(frozen=True, slots=True)
class Coordinate:
    level: int
    x: int
    y: int


def level_size(level: int) -> int:
    if level < 0 or level > MAX_LEVEL:
        raise ValueError(f"level must be between 0 and {MAX_LEVEL}: {level}")
    return BASE_SIZE - level


def level_sizes() -> list[int]:
    return [level_size(level) for level in range(BASE_SIZE)]


def is_valid_coordinate(level: int, x: int, y: int) -> bool:
    if level < 0 or level > MAX_LEVEL:
        return False
    size = BASE_SIZE - level
    return 0 <= x < size and 0 <= y < size


def validate_coordinate(level: int, x: int, y: int) -> None:
    if not is_valid_coordinate(level, x, y):
        raise ValueError(f"invalid coordinate: level={level}, x={x}, y={y}")
