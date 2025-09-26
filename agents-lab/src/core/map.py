from typing import List

from .cell import Cell


class Map:
    """
    Mapa en forma de grilla que representa un entorno discreto.

    El mapa consiste en una grilla 2D de celdas, donde cada celda
    contiene información sobre el terreno en esa posición.
    """

    def __init__(self, grid: List[List[Cell]]):
        """
        Inicializa un nuevo mapa con la grilla proporcionada.

        Args:
            grid: Grilla 2D de celdas
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def mask_all(self) -> None:
        """Enmascara todo el mapa (marca todas las celdas como no descubiertas)."""
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].mask()

    def discover_cell(self, row: int, col: int) -> bool:
        """
        Descubre una celda específica.

        Args:
            row: Fila de la celda
            col: Columna de la celda

        Returns:
            bool: True si la celda existe y se descubrió
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col].discover()
            return True
        return False

    def mask_cell(self, row: int, col: int) -> bool:
        """
        Enmascara una celda específica.

        Args:
            row: Fila de la celda
            col: Columna de la celda

        Returns:
            bool: True si la celda existe y se enmascaró
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col].mask()
            return True
        return False

    def get_discovered_count(self) -> int:
        """
        Obtiene el número de celdas descubiertas.

        Returns:
            int: Cantidad de celdas descubiertas
        """
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col].is_visible():
                    count += 1
        return count

    def __str__(self) -> str:
        """Representación string básica del mapa."""
        return f"Map(rows={self.rows}, cols={self.cols})"

    def __repr__(self) -> str:
        """Representación para debug del mapa."""
        return f"Map(rows={self.rows}, cols={self.cols})"
