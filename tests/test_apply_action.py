import pytest

from mosaic_ai.apply_action import apply_action, next_player
from mosaic_ai.game_state import Occupant, create_initial_state
from mosaic_ai.legal_actions import PlaceAction, legal_actions


def test_apply_action_places_piece_and_updates_turn_state():
    state = create_initial_state()
    action = PlaceAction(level=0, x=0, y=0)

    new_state = apply_action(state, action)

    assert new_state.occupant_at(0, 0, 0) == Occupant.PLAYER1
    assert new_state.players[1].remaining_pieces == 69
    assert new_state.players[2].remaining_pieces == 70
    assert new_state.current_player == 2
    assert new_state.ply_index == 1
    assert new_state.game_over is False
    assert new_state.winner is None


def test_apply_action_does_not_mutate_original_state():
    state = create_initial_state()
    action = PlaceAction(level=0, x=0, y=0)

    new_state = apply_action(state, action)

    assert state.occupant_at(0, 0, 0) == Occupant.EMPTY
    assert state.players[1].remaining_pieces == 70
    assert state.current_player == 1
    assert state.ply_index == 0
    assert new_state is not state


def test_apply_action_rejects_occupied_position():
    state = create_initial_state()

    with pytest.raises(ValueError, match="already occupied"):
        apply_action(state, PlaceAction(level=0, x=3, y=3))


def test_apply_action_rejects_unsupported_upper_level_position():
    state = create_initial_state()

    with pytest.raises(ValueError, match="not supported"):
        apply_action(state, PlaceAction(level=1, x=0, y=0))


def test_apply_action_rejects_out_of_range_coordinate():
    state = create_initial_state()

    with pytest.raises(ValueError, match="invalid coordinate"):
        apply_action(state, PlaceAction(level=0, x=7, y=0))


def test_apply_action_rejects_neutral_center_position_in_initial_state():
    state = create_initial_state()

    with pytest.raises(ValueError, match="already occupied"):
        apply_action(state, PlaceAction(level=0, x=3, y=3))


def test_apply_action_removes_played_position_from_legal_actions():
    state = create_initial_state()
    action = PlaceAction(level=0, x=0, y=0)

    new_state = apply_action(state, action)
    actions_after = legal_actions(new_state)

    assert action not in actions_after


def test_next_player_switches_between_two_players():
    assert next_player(1) == 2
    assert next_player(2) == 1
