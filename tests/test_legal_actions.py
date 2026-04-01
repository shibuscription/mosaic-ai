from mosaic_ai.game_state import Occupant, create_initial_state
from mosaic_ai.legal_actions import PlaceAction, has_support, legal_actions


def test_initial_state_has_48_legal_actions_all_on_bottom_level():
    state = create_initial_state()

    actions = legal_actions(state)

    assert len(actions) == 48
    assert all(action.level == 0 for action in actions)
    assert PlaceAction(level=0, x=3, y=3) not in actions


def test_supported_upper_level_position_is_legal_action():
    state = create_initial_state()
    state.set_occupant(0, 0, 0, Occupant.PLAYER1)
    state.set_occupant(0, 1, 0, Occupant.PLAYER2)
    state.set_occupant(0, 0, 1, Occupant.NEUTRAL)
    state.set_occupant(0, 1, 1, Occupant.PLAYER1)

    assert has_support(state, 1, 0, 0) is True
    assert PlaceAction(level=1, x=0, y=0) in legal_actions(state)


def test_upper_level_position_without_full_support_is_not_legal_action():
    state = create_initial_state()
    state.set_occupant(0, 0, 0, Occupant.PLAYER1)
    state.set_occupant(0, 1, 0, Occupant.PLAYER2)
    state.set_occupant(0, 0, 1, Occupant.NEUTRAL)

    assert has_support(state, 1, 0, 0) is False
    assert PlaceAction(level=1, x=0, y=0) not in legal_actions(state)


def test_occupied_positions_are_not_legal_actions():
    state = create_initial_state()
    state.set_occupant(0, 0, 0, Occupant.PLAYER1)

    actions = legal_actions(state)

    assert PlaceAction(level=0, x=0, y=0) not in actions
    assert PlaceAction(level=0, x=3, y=3) not in actions


def test_legal_actions_are_sorted_by_level_then_y_then_x():
    state = create_initial_state()
    state.set_occupant(0, 0, 0, Occupant.PLAYER1)
    state.set_occupant(0, 1, 0, Occupant.PLAYER2)
    state.set_occupant(0, 0, 1, Occupant.NEUTRAL)
    state.set_occupant(0, 1, 1, Occupant.PLAYER1)

    actions = legal_actions(state)

    sorted_actions = sorted(actions, key=lambda action: (action.level, action.y, action.x))
    assert actions == sorted_actions
    assert actions[0] == PlaceAction(level=0, x=2, y=0)
    assert PlaceAction(level=1, x=0, y=0) in actions
