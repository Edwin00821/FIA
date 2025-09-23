import pytest

from src.core.cell import TerrainType, Cell
from src.core.map import Map
from src.utils.map_loader import BaseMapLoader, MapLoaderError


class DummyLoader(BaseMapLoader):
    def load(self, file_path: str) -> Map:
        return Map([[Cell(TerrainType.ROAD)]])


@pytest.fixture
def loader():
    return DummyLoader()


def test_validate_file_exists_invalid_file(loader):
    with pytest.raises(MapLoaderError, match="no existe"):
        loader._validate_file_exists("archivo_inexistente.txt")


@pytest.mark.parametrize("value,expected", [
    ("0", TerrainType.WALL),
    ("1", TerrainType.ROAD),
    (" 1 ", TerrainType.ROAD),
])
def test_parse_terrain_value_valid(loader, value, expected):
    assert loader._parse_terrain_value(value) == expected


@pytest.mark.parametrize("value", ["999", "abc"])
def test_parse_terrain_value_invalid(loader, value):
    with pytest.raises(MapLoaderError):
        loader._parse_terrain_value(value)
