from __future__ import annotations

from .coordinates import validate_coordinate
from .game_state import GameState, Occupant
from .legal_actions import PlaceAction, has_support


def next_player(player_id: int) -> int:
    if player_id == 1:
        return 2
    if player_id == 2:
        return 1
    raise ValueError(f"unsupported player id: {player_id}")


def player_occupant(player_id: int) -> Occupant:
    if player_id == 1:
        return Occupant.PLAYER1
    if player_id == 2:
        return Occupant.PLAYER2
    raise ValueError(f"unsupported player id: {player_id}")


def validate_action(state: GameState, action: PlaceAction) -> None:
    if state.game_over:
        raise ValueError("cannot apply action to a finished game")
    if action.action_type != "place":
        raise ValueError(f"unsupported action_type: {action.action_type}")

    validate_coordinate(action.level, action.x, action.y)

    if state.current_player not in state.players:
        raise ValueError(f"unknown current player: {state.current_player}")

    player_state = state.players[state.current_player]
    if player_state.remaining_pieces <= 0:
        raise ValueError(f"player {state.current_player} has no remaining pieces")

    if not state.is_empty(action.level, action.x, action.y):
        raise ValueError(
            f"position is already occupied: level={action.level}, x={action.x}, y={action.y}"
        )

    if action.level > 0 and not has_support(state, action.level, action.x, action.y):
        raise ValueError(
            f"position is not supported: level={action.level}, x={action.x}, y={action.y}"
        )


def apply_action(state: GameState, action: PlaceAction) -> GameState:
    validate_action(state, action)

    new_state = state.clone()
    current_player = new_state.current_player
    current_player_state = new_state.players[current_player]

    new_state.set_occupant(action.level, action.x, action.y, player_occupant(current_player))
    current_player_state.remaining_pieces -= 1
    new_state.ply_index += 1
    new_state.current_player = next_player(current_player)

    return new_state
