import pytest
from unittest.mock import mock_open, patch
from pathlib import Path
from src.utils.map_loader import TxtMapLoader


@pytest.fixture
def txt_loader():
    return TxtMapLoader()


def test_inconsistent_row_lengths_txt(txt_loader):
    content = "0,1,0\n1,0\n1,0,1,0"
    with patch("builtins.open", mock_open(read_data=content)):
        with patch.object(Path, "exists", return_value=True):
            map_obj = txt_loader.load("test.txt")
            assert map_obj.rows == 3
            assert len(map_obj.grid[0]) == 3
            assert len(map_obj.grid[1]) == 2
            assert len(map_obj.grid[2]) == 4


def test_single_line_file(txt_loader):
    content = "0,1,0,1"
    with patch("builtins.open", mock_open(read_data=content)):
        with patch.object(Path, "exists", return_value=True):
            map_obj = txt_loader.load("single_line.txt")
            assert map_obj.rows == 1
            assert map_obj.cols == 4
