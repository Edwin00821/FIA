from src.utils.map_loader import MapLoaderError


def test_map_loader_error_creation():
    error = MapLoaderError("Mensaje de error")
    assert str(error) == "Mensaje de error"
    assert isinstance(error, Exception)
