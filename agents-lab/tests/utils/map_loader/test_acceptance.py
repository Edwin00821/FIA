import pytest
import tempfile
import os
from pathlib import Path
from src.utils.map_loader import MapLoader
from src.core.cell import TerrainType


@pytest.fixture
def loader():
    return MapLoader()


def test_load_real_maze_txt(loader):
    maze_path = Path(__file__).parent.parent.parent.parent / "data" / "maze.txt"
    if not maze_path.exists():
        pytest.skip("Archivo de prueba no encontrado: maze.txt")

    map_obj = loader.load_map(str(maze_path))
    assert map_obj.rows == 14
    assert map_obj.cols == 14
    assert map_obj.grid[0][0].terrain == TerrainType.WALL
    assert map_obj.grid[0][8].terrain == TerrainType.ROAD
    assert map_obj.grid[9][0].terrain == TerrainType.ROAD


def test_create_and_load_temporary_file(loader):
    test_content = "0,1,0\n1,1,1\n0,1,0"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp_file:
        tmp_file.write(test_content)
        tmp_path = tmp_file.name

    try:
        map_obj = loader.load_map(tmp_path)
        assert map_obj.rows == 3
        assert map_obj.cols == 3
        assert map_obj.grid[1][1].terrain == TerrainType.ROAD
        assert map_obj.grid[0][0].terrain == TerrainType.WALL
    finally:
        os.unlink(tmp_path)
