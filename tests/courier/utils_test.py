import pytest

from courier.config import get_config
from courier.utils import corrected_page_number, flatten, get_filenames, get_stats

CONFIG = get_config()


def test_flatten_returns_expected_values():
    assert flatten([[1, 2, 3], (4, 5, 6), [7, 8]]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert flatten((('a', 'b'), [1, 2])) == ['a', 'b', 1, 2]


def test_get_stats(monkeypatch):
    monkeypatch.setattr(CONFIG, 'pdf_dir', CONFIG.test_files_dir)
    stats = get_stats()
    assert stats['files'] == 1
    assert stats['mean'] == 8
    assert stats['median'] == 8
    assert stats['pages'] == 8


def test_get_filenames_returns_only_files_with_expected_extension(tmp_path):

    pdf_file = tmp_path / 'test.pdf'
    pdf_file.touch()
    txt_file = tmp_path / 'test.txt'
    txt_file.touch()

    assert pdf_file in get_filenames(tmp_path)
    assert txt_file not in get_filenames(tmp_path)
    assert txt_file in get_filenames(tmp_path, 'txt')

    assert get_filenames(txt_file) == []
    assert get_filenames(pdf_file) == get_filenames(tmp_path) == [pdf_file]


@pytest.mark.parametrize(
    'courier_id, page_number, expected',
    [
        ('012656', 10, 10),
        ('012656', 20, 19),
        ('069916', 25, 22),
        ('033144', 65, 65),
    ],
)
def test_corrected_page_number_returns_expected(courier_id, page_number, expected):
    result = corrected_page_number(courier_id, page_number)
    assert result == expected
