import pytest

from src.utils.map_loader import MapLoader, MapLoaderError


@pytest.fixture
def loader():
    return MapLoader()


def test_unsupported_format(loader):
    with pytest.raises(MapLoaderError, match="Formato de archivo no soportado: .json"):
        loader.load_map("test.json")
