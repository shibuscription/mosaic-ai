import pytest

from mosaic_ai.coordinates import BASE_SIZE, MAX_LEVEL, is_valid_coordinate, level_size, level_sizes


def test_level_sizes_match_standard_7x7_pyramid():
    assert level_sizes() == [7, 6, 5, 4, 3, 2, 1]
    assert level_size(0) == 7
    assert level_size(MAX_LEVEL) == 1


@pytest.mark.parametrize(
    ("level", "x", "y", "expected"),
    [
        (0, 0, 0, True),
        (0, 6, 6, True),
        (1, 5, 5, True),
        (6, 0, 0, True),
        (0, 7, 0, False),
        (1, 6, 0, False),
        (6, 1, 0, False),
        (-1, 0, 0, False),
        (BASE_SIZE, 0, 0, False),
    ],
)
def test_coordinate_validation(level, x, y, expected):
    assert is_valid_coordinate(level, x, y) is expected
