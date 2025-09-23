import pytest
from unittest.mock import mock_open, patch
from pathlib import Path
from src.utils.map_loader import TxtMapLoader, MapLoaderError
from src.core.cell import TerrainType


@pytest.fixture
def txt_loader():
    return TxtMapLoader()


def test_trailing_commas(txt_loader):
    content = "0,1,0,\n1,0,1,"
    with patch("builtins.open", mock_open(read_data=content)):
        with patch.object(Path, "exists", return_value=True):
            with pytest.raises(MapLoaderError):
                txt_loader.load("trailing_commas.txt")


def test_mixed_whitespace_separators(txt_loader):
    content = " 0 ,\t1\t, 0 \n\t1\t,0, 1 "
    with patch("builtins.open", mock_open(read_data=content)):
        with patch.object(Path, "exists", return_value=True):
            map_obj = txt_loader.load("whitespace.txt")
            assert map_obj.rows == 2
            assert map_obj.grid[0][0].terrain == TerrainType.WALL
            assert map_obj.grid[0][1].terrain == TerrainType.ROAD


def test_empty_file_error_message(txt_loader):
    with patch("builtins.open", mock_open(read_data="")):
        with patch.object(Path, "exists", return_value=True):
            with pytest.raises(MapLoaderError, match="vacío o no contiene datos válidos"):
                txt_loader.load("empty.txt")


def test_io_error_handling(txt_loader):
    with patch("builtins.open", side_effect=PermissionError("Acceso denegado")):
        with patch.object(Path, "exists", return_value=True):
            with pytest.raises(MapLoaderError, match="Error al leer el archivo"):
                txt_loader.load("no_permission.txt")
