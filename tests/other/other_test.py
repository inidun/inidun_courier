from courier.config import get_config
from courier.utils import flatten

CONFIG = get_config()


def test_utils_flatten_returns_expected_values():
    assert flatten([[1, 2, 3], (4, 5, 6), [7, 8]]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert flatten((('a', 'b'), [1, 2])) == ['a', 'b', 1, 2]
