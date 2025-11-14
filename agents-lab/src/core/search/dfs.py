from typing import Tuple, List

from src.core.map import Map
from .search_algorithm import SearchAlgorithm
from .search_result import SearchResult, SearchStepType
from .search_node import SearchNode


class DepthFirstSearch(SearchAlgorithm):
    """
    Implementación del algoritmo de Búsqueda en Profundidad (DFS).

    DFS explora en profundidad siguiendo un camino hasta el final
    antes de retroceder. Utiliza prioridad direccional definida.
    """

    def __init__(
        self,
        map_obj: Map,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        direction_priority: List[str] = None
    ):
        """
        Inicializa DFS.

        Args:
            map_obj: Mapa donde buscar
            start: Posición inicial (row, col)
            goal: Posición objetivo (row, col)
            direction_priority: Prioridad de direcciones para explorar
                               (e.g., ['up', 'right', 'down', 'left'])
        """
        super().__init__(map_obj, start, goal)
        self.stack: List[SearchNode] = []

        # Prioridad por defecto: arriba, derecha, abajo, izquierda
        self.direction_priority = direction_priority or [
            'up', 'right', 'down', 'left']

        # Mapeo de direcciones a deltas
        self.direction_deltas = {
            'up': (-1, 0),
            'down': (1, 0),
            'right': (0, 1),
            'left': (0, -1)
        }

    def _get_neighbors_ordered(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Obtiene los vecinos ordenados según la prioridad direccional.

        Args:
            position: Posición actual (row, col)

        Returns:
            Lista de posiciones vecinas ordenadas por prioridad
        """
        row, col = position
        neighbors = []

        for direction in self.direction_priority:
            dr, dc = self.direction_deltas[direction]
            new_pos = (row + dr, col + dc)
            if self._is_valid_position(new_pos):
                neighbors.append(new_pos)

        return neighbors

    def search(self) -> SearchResult:
        """
        Ejecuta DFS para encontrar un camino.

        Returns:
            SearchResult con el resultado de la búsqueda
        """
        # Inicializar
        root = SearchNode(position=self.start, depth=0)
        self.stack.append(root)
        self.visited.add(self.start)

        # Crear paso inicial
        step = self._create_search_step(
            root,
            SearchStepType.EXPLORE,
            [self.start]
        )
        self.steps.append(step)

        # DFS loop
        while self.stack:
            # Actualizar estadísticas
            self.max_frontier_size = max(
                self.max_frontier_size, len(self.stack))

            # Obtener nodo actual (peek, no pop todavía)
            current_node = self.stack[-1]
            self.nodes_expanded += 1

            # Verificar si llegamos al objetivo
            if current_node.position == self.goal:
                step = self._create_search_step(
                    current_node,
                    SearchStepType.GOAL_FOUND,
                    [node.position for node in self.stack]
                )
                self.steps.append(step)

                return SearchResult(
                    success=True,
                    solution_path=self._reconstruct_path(current_node),
                    root_node=root,
                    steps=self.steps,
                    nodes_expanded=self.nodes_expanded,
                    max_frontier_size=self.max_frontier_size,
                    goal_node=current_node,
                    path_cost=float(len(current_node.get_path_positions()) - 1)
                )

            # Obtener vecinos ordenados por prioridad
            neighbors = self._get_neighbors_ordered(current_node.position)
            unvisited_neighbors = [
                n for n in neighbors if n not in self.visited]

            # Marcar punto de decisión si hay múltiples caminos
            if len(unvisited_neighbors) > 1:
                current_node.is_decision_point = True

            # Si hay vecinos no visitados, explorar el primero
            if unvisited_neighbors:
                next_pos = unvisited_neighbors[0]

                # Crear nodo hijo
                next_node = SearchNode(position=next_pos)
                current_node.add_child(next_node)

                # Marcar como visitado y agregar al stack
                self.visited.add(next_pos)
                self.stack.append(next_node)

                # Crear paso de búsqueda
                step_type = (SearchStepType.DECISION
                             if self._is_decision_point(next_pos)
                             else SearchStepType.EXPLORE)

                step = self._create_search_step(
                    next_node,
                    step_type,
                    [node.position for node in self.stack]
                )
                self.steps.append(step)
            else:
                # No hay vecinos: backtrack (retroceder)
                self.stack.pop()
                current_node.is_dead_end = True

                if self.stack:  # Si aún hay nodos en el stack
                    step = self._create_search_step(
                        self.stack[-1],  # Nodo al que retrocedemos
                        SearchStepType.BACKTRACK,
                        [node.position for node in self.stack]
                    )
                    self.steps.append(step)

        # No se encontró solución
        return SearchResult(
            success=False,
            root_node=root,
            steps=self.steps,
            nodes_expanded=self.nodes_expanded,
            max_frontier_size=self.max_frontier_size,
            goal_node=None,
            path_cost=float('inf')
        )
