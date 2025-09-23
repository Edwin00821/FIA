import pytest
from unittest.mock import mock_open, patch
from pathlib import Path
from src.utils.map_loader import MapLoader, MapLoaderError


def test_complete_workflow_error_recovery():
    loader = MapLoader()

    with pytest.raises(MapLoaderError):
        loader.load_map("nonexistent.txt")

    content = "0,1\n1,0"
    with patch("builtins.open", mock_open(read_data=content)):
        with patch.object(Path, "exists", return_value=True):
            map_obj = loader.load_map("valid.txt")
            assert map_obj.rows == 2
            assert map_obj.cols == 2
