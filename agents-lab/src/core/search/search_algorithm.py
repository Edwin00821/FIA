from abc import ABC, abstractmethod
from typing import Tuple, List, Set

from src.core.map import Map
from .search_result import SearchResult, SearchStep, SearchStepType
from .search_node import SearchNode


class SearchAlgorithm(ABC):
    """
    Clase base abstracta para algoritmos de búsqueda.

    Define la interfaz común que deben implementar todos los algoritmos
    de búsqueda (BFS, DFS, etc.).
    """

    def __init__(self, map_obj: Map, start: Tuple[int, int], goal: Tuple[int, int]):
        """
        Inicializa el algoritmo de búsqueda.

        Args:
            map_obj: Mapa donde buscar
            start: Posición inicial (row, col)
            goal: Posición objetivo (row, col)
        """
        self.map = map_obj
        self.start = start
        self.goal = goal

        # Estadísticas
        self.nodes_expanded = 0
        self.max_frontier_size = 0

        # Estado de la búsqueda
        self.visited: Set[Tuple[int, int]] = set()
        self.steps: List[SearchStep] = []

    @abstractmethod
    def search(self) -> SearchResult:
        """
        Ejecuta el algoritmo de búsqueda.

        Returns:
            SearchResult con el resultado de la búsqueda
        """
        pass

    def _is_valid_position(self, position: Tuple[int, int]) -> bool:
        """
        Verifica si una posición es válida y transitable.

        Args:
            position: Posición a verificar (row, col)

        Returns:
            True si la posición es válida y transitable
        """
        row, col = position

        # Verificar límites
        if not (0 <= row < self.map.rows and 0 <= col < self.map.cols):
            return False

        # Verificar que sea transitable
        return self.map.grid[row][col].is_passable()

    def _get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Obtiene los vecinos válidos de una posición.

        Args:
            position: Posición actual (row, col)

        Returns:
            Lista de posiciones vecinas válidas
        """
        row, col = position
        directions = [
            (-1, 0),  # Arriba
            (0, 1),   # Derecha
            (1, 0),   # Abajo
            (0, -1),  # Izquierda
        ]

        neighbors = []
        for dr, dc in directions:
            new_pos = (row + dr, col + dc)
            if self._is_valid_position(new_pos):
                neighbors.append(new_pos)

        return neighbors

    def _is_decision_point(self, position: Tuple[int, int]) -> bool:
        """
        Verifica si una posición es un punto de decisión.

        Un punto de decisión es donde hay más de 2 vecinos transitables
        (bifurcación) o es el inicio/objetivo.

        Args:
            position: Posición a verificar

        Returns:
            True si es punto de decisión
        """
        if position == self.start or position == self.goal:
            return True

        neighbors = self._get_neighbors(position)
        return len(neighbors) > 2

    def _reconstruct_path(self, node: SearchNode) -> List[Tuple[int, int]]:
        """
        Reconstruye el camino desde el inicio hasta el nodo dado.

        Args:
            node: Nodo final

        Returns:
            Lista de posiciones desde inicio hasta el nodo
        """
        return node.get_path_positions()

    def _create_search_step(
        self,
        node: SearchNode,
        step_type: SearchStepType,
        frontier_positions: List[Tuple[int, int]]
    ) -> SearchStep:
        """
        Crea un paso de búsqueda para tracking.

        Args:
            node: Nodo actual
            step_type: Tipo de paso
            frontier_positions: Posiciones en la frontera

        Returns:
            SearchStep creado
        """
        return SearchStep(
            node=node,
            step_type=step_type,
            frontier=frontier_positions.copy(),
            visited=list(self.visited),
            current_path=self._reconstruct_path(node)
        )
