from mosaic_ai.game_state import Occupant, create_initial_state
from mosaic_ai.serialization import state_from_dict, state_to_dict


def test_state_to_dict_preserves_basic_initial_state_information():
    state = create_initial_state()

    payload = state_to_dict(state)

    assert payload["current_player"] == 1
    assert payload["ply_index"] == 0
    assert payload["game_over"] is False
    assert payload["winner"] is None
    assert payload["players"][0]["remaining_pieces"] == 70
    assert payload["players"][1]["remaining_pieces"] == 70
    assert payload["board"]["levels"][0]["cells"][3][3] == Occupant.NEUTRAL.value


def test_state_serialization_round_trip_preserves_basic_fields():
    state = create_initial_state()
    serialized = state_to_dict(state)

    restored = state_from_dict(serialized)

    assert restored.current_player == state.current_player
    assert restored.ply_index == state.ply_index
    assert restored.game_over == state.game_over
    assert restored.winner == state.winner
    assert restored.players[1].remaining_pieces == state.players[1].remaining_pieces
    assert restored.players[2].remaining_pieces == state.players[2].remaining_pieces
    assert restored.occupant_at(0, 3, 3) == Occupant.NEUTRAL
