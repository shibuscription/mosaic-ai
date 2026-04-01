from mosaic_ai.coordinates import BASE_SIZE, level_size
from mosaic_ai.game_state import (
    INITIAL_CURRENT_PLAYER,
    INITIAL_REMAINING_PIECES,
    Occupant,
    create_initial_state,
)


def test_initial_state_has_expected_number_of_levels():
    state = create_initial_state()

    assert len(state.board) == BASE_SIZE
    assert [len(level_rows) for level_rows in state.board] == [level_size(level) for level in range(BASE_SIZE)]


def test_initial_state_places_neutral_piece_in_center_of_bottom_level():
    state = create_initial_state()

    center = BASE_SIZE // 2
    assert state.occupant_at(0, center, center) == Occupant.NEUTRAL


def test_initial_state_sets_players_and_turn_metadata():
    state = create_initial_state()

    assert state.players[1].remaining_pieces == INITIAL_REMAINING_PIECES
    assert state.players[2].remaining_pieces == INITIAL_REMAINING_PIECES
    assert state.current_player == INITIAL_CURRENT_PLAYER
    assert state.ply_index == 0
    assert state.game_over is False
    assert state.winner is None
