from typing import List, Set, Tuple, Dict
from collections import defaultdict

from .cell import Cell, CellMark


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
        self.discovered_cells: Set[Tuple[int, int]] = set()
        self.mark_index: Dict[CellMark, List[Tuple[int, int]]] = defaultdict(list)
        self._index_built = False

    def mask_all(self) -> None:
        """Enmascara todo el mapa (marca todas las celdas como no descubiertas)."""
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col].mask()
        self.discovered_cells.clear()

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
            self.discovered_cells.add((row, col))
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

    def _build_mark_index(self) -> None:
        """Construye el índice de marcas si no está construido."""
        if self._index_built:
            return
        self.mark_index.clear()
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                for mark in cell.marks:
                    self.mark_index[mark].append((row, col))
        self._index_built = True

    def get_positions_with_mark(self, mark: CellMark) -> List[Tuple[int, int]]:
        """
        Obtiene todas las posiciones con una marca específica.

        Args:
            mark: Marca a buscar

        Returns:
            Lista de tuplas (row, col)
        """
        self._build_mark_index()
        return self.mark_index[mark].copy()

    def mark_decision_points(self) -> None:
        """
        Marca las celdas que son puntos de decisión.

        Un punto de decisión es una celda transitable que tiene más de 2 vecinos transitables.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if not cell.is_passable():
                    continue

                # Contar vecinos transitables
                passable_neighbors = 0
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.grid[nr][nc].is_passable():
                            passable_neighbors += 1

                if passable_neighbors > 2:
                    cell.add_mark(CellMark.DECISION)

    def __str__(self) -> str:
        """Representación string básica del mapa."""
        return f"Map(rows={self.rows}, cols={self.cols})"

    def __repr__(self) -> str:
        """Representación para debug del mapa."""
        return f"Map(rows={self.rows}, cols={self.cols})"
