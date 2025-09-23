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

    def __str__(self) -> str:
        """Representación string básica del mapa."""
        return f"Map(rows={self.rows}, cols={self.cols})"

    def __repr__(self) -> str:
        """Representación para debug del mapa."""
        return f"Map(rows={self.rows}, cols={self.cols})"
