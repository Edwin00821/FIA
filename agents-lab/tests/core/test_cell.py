import unittest
from src.core.cell import TerrainType, Cell


class TestTerrainType(unittest.TestCase):
    """Casos de prueba para el enum TerrainType."""

    def test_terrain_values(self):
        """Verifica que los tipos de terreno tienen valores numéricos correctos."""
        self.assertEqual(TerrainType.WALL.value, 0)
        self.assertEqual(TerrainType.ROAD.value, 1)

    def test_from_value_valid(self):
        """Prueba from_value con valores numéricos válidos."""
        self.assertEqual(TerrainType.from_value(0), TerrainType.WALL)
        self.assertEqual(TerrainType.from_value(1), TerrainType.ROAD)

    def test_from_value_invalid(self):
        """Prueba que from_value lanza ValueError para valores inválidos."""
        with self.assertRaises(ValueError) as context:
            TerrainType.from_value(999)

        self.assertIn("Valor de terreno desconocido: 999",
                      str(context.exception))

    def test_from_value_negative(self):
        """Prueba from_value con valores negativos."""
        with self.assertRaises(ValueError):
            TerrainType.from_value(-1)

    def test_terrain_names(self):
        """Verifica que los tipos de terreno tienen nombres correctos."""
        self.assertEqual(TerrainType.WALL.name, "WALL")
        self.assertEqual(TerrainType.ROAD.name, "ROAD")


class TestCell(unittest.TestCase):
    """Casos de prueba para la clase Cell."""

    def test_cell_creation_wall(self):
        """Prueba crear una celda con terreno de muro."""
        cell = Cell(TerrainType.WALL)
        self.assertEqual(cell.terrain, TerrainType.WALL)
        self.assertFalse(cell.is_passable())

    def test_cell_creation_road(self):
        """Prueba crear una celda con terreno de camino."""
        cell = Cell(TerrainType.ROAD)
        self.assertEqual(cell.terrain, TerrainType.ROAD)
        self.assertTrue(cell.is_passable())

    def test_cell_creation_invalid_terrain(self):
        """Prueba que crear una celda con terreno inválido lanza TypeError."""
        with self.assertRaises(TypeError) as context:
            Cell("not_a_terrain")

        self.assertIn(
            "terrain debe ser una instancia de TerrainType", str(context.exception))

    def test_cell_creation_none_terrain(self):
        """Prueba que crear una celda con terreno None lanza TypeError."""
        with self.assertRaises(TypeError):
            Cell(None)

    def test_cell_equality_same_terrain(self):
        """Prueba que celdas con el mismo terreno son iguales."""
        cell1 = Cell(TerrainType.WALL)
        cell2 = Cell(TerrainType.WALL)
        self.assertEqual(cell1, cell2)

    def test_cell_equality_different_terrain(self):
        """Prueba que celdas con diferente terreno no son iguales."""
        cell1 = Cell(TerrainType.WALL)
        cell2 = Cell(TerrainType.ROAD)
        self.assertNotEqual(cell1, cell2)

    def test_cell_equality_with_non_cell(self):
        """Prueba que una celda no es igual a objetos que no son celdas."""
        cell = Cell(TerrainType.WALL)
        self.assertNotEqual(cell, "not_a_cell")
        self.assertNotEqual(cell, 42)
        self.assertNotEqual(cell, None)

    def test_is_passable_wall(self):
        """Prueba que las celdas de muro no son transitables."""
        cell = Cell(TerrainType.WALL)
        self.assertFalse(cell.is_passable())

    def test_is_passable_road(self):
        """Prueba que las celdas de camino son transitables."""
        cell = Cell(TerrainType.ROAD)
        self.assertTrue(cell.is_passable())

    def test_str_representation(self):
        """Prueba la representación string de las celdas."""
        wall_cell = Cell(TerrainType.WALL)
        road_cell = Cell(TerrainType.ROAD)

        self.assertEqual(str(wall_cell), "Cell(WALL)")
        self.assertEqual(str(road_cell), "Cell(ROAD)")

    def test_repr_representation(self):
        """Prueba la representación string detallada de las celdas."""
        wall_cell = Cell(TerrainType.WALL)
        road_cell = Cell(TerrainType.ROAD)

        self.assertEqual(repr(wall_cell), "Cell(terrain=TerrainType.WALL)")
        self.assertEqual(repr(road_cell), "Cell(terrain=TerrainType.ROAD)")


if __name__ == '__main__':
    unittest.main(verbosity=2)
