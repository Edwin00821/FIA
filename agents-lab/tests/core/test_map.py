import unittest

from src.core.cell import TerrainType, Cell
from src.core.map import Map


class TestMap(unittest.TestCase):
    def test_map_creation_square(self):
        """Prueba la creación de un mapa cuadrado."""
        grid = [
            [Cell(TerrainType.WALL), Cell(TerrainType.ROAD)],
            [Cell(TerrainType.ROAD), Cell(TerrainType.WALL)]
        ]
        map_obj = Map(grid)

        self.assertEqual(map_obj.rows, 2)
        self.assertEqual(map_obj.cols, 2)
        self.assertEqual(len(map_obj.grid), 2)
        self.assertEqual(len(map_obj.grid[0]), 2)

    def test_map_creation_rectangular(self):
        """Prueba la creación de un mapa rectangular."""
        # Mapa de 2 filas x 4 columnas
        grid = [
            [Cell(TerrainType.WALL), Cell(TerrainType.ROAD),
             Cell(TerrainType.WALL), Cell(TerrainType.ROAD)],
            [Cell(TerrainType.ROAD), Cell(TerrainType.WALL),
             Cell(TerrainType.ROAD), Cell(TerrainType.WALL)]
        ]
        map_obj = Map(grid)

        self.assertEqual(map_obj.rows, 2)
        self.assertEqual(map_obj.cols, 4)

    def test_map_creation_different_dimensions(self):
        """Prueba la creación de un mapa con dimensiones diferentes."""
        # Mapa de 3 filas x 2 columnas
        grid = [
            [Cell(TerrainType.WALL), Cell(TerrainType.ROAD)],
            [Cell(TerrainType.ROAD), Cell(TerrainType.WALL)],
            [Cell(TerrainType.WALL), Cell(TerrainType.WALL)]
        ]
        map_obj = Map(grid)

        self.assertEqual(map_obj.rows, 3)
        self.assertEqual(map_obj.cols, 2)

    def test_map_creation_empty(self):
        """Prueba la creación de un mapa vacío."""
        grid = []
        map_obj = Map(grid)

        self.assertEqual(map_obj.rows, 0)
        self.assertEqual(map_obj.cols, 0)

    def test_map_grid_access(self):
        """Prueba el acceso directo a la grilla."""
        grid = [
            [Cell(TerrainType.WALL), Cell(TerrainType.ROAD)],
            [Cell(TerrainType.ROAD), Cell(TerrainType.WALL)]
        ]
        map_obj = Map(grid)

        # Verificar que podemos acceder a las celdas
        self.assertEqual(map_obj.grid[0][0].terrain, TerrainType.WALL)
        self.assertEqual(map_obj.grid[0][1].terrain, TerrainType.ROAD)
        self.assertEqual(map_obj.grid[1][0].terrain, TerrainType.ROAD)
        self.assertEqual(map_obj.grid[1][1].terrain, TerrainType.WALL)

    def test_str_representation(self):
        """Prueba la representación string del mapa."""
        grid = [
            [Cell(TerrainType.WALL), Cell(TerrainType.ROAD)],
            [Cell(TerrainType.ROAD), Cell(TerrainType.WALL)]
        ]
        map_obj = Map(grid)

        string_repr = str(map_obj)
        self.assertEqual(string_repr, "Map(rows=2, cols=2)")

    def test_repr_representation(self):
        """Prueba la representación repr del mapa."""
        grid = [
            [Cell(TerrainType.WALL)]
        ]
        map_obj = Map(grid)

        repr_str = repr(map_obj)
        self.assertEqual(repr_str, "Map(rows=1, cols=1)")


if __name__ == '__main__':
    unittest.main(verbosity=2)
