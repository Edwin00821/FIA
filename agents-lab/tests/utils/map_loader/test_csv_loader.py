import pytest
from unittest.mock import mock_open, patch
from pathlib import Path
from src.utils.map_loader import CsvMapLoader


@pytest.fixture
def csv_loader():
    return CsvMapLoader()


def test_inconsistent_row_lengths_csv(csv_loader):
    content = "0,1,0\n1,0\n1,0,1,0"
    with patch("builtins.open", mock_open(read_data=content)):
        with patch.object(Path, "exists", return_value=True):
            map_obj = csv_loader.load("test.csv")
            assert map_obj.rows == 3
            assert len(map_obj.grid[0]) == 3
            assert len(map_obj.grid[1]) == 2
            assert len(map_obj.grid[2]) == 4
