from collections import deque
from typing import Tuple

from src.core.map import Map
from .search_algorithm import SearchAlgorithm
from .search_result import SearchResult, SearchStepType
from .search_node import SearchNode


class BreadthFirstSearch(SearchAlgorithm):
    """
    Implementación del algoritmo de Búsqueda por Amplitud (BFS).

    BFS explora el grafo nivel por nivel, garantizando encontrar
    el camino más corto en términos de número de celdas.
    """

    def __init__(self, map_obj: Map, start: Tuple[int, int], goal: Tuple[int, int]):
        """
        Inicializa BFS.

        Args:
            map_obj: Mapa donde buscar
            start: Posición inicial (row, col)
            goal: Posición objetivo (row, col)
        """
        super().__init__(map_obj, start, goal)
        self.queue: deque[SearchNode] = deque()

    def search(self) -> SearchResult:
        """
        Ejecuta BFS para encontrar el camino más corto.

        Returns:
            SearchResult con el resultado de la búsqueda
        """
        # Inicializar
        root = SearchNode(position=self.start, depth=0)
        self.queue.append(root)
        self.visited.add(self.start)

        # Crear paso inicial
        step = self._create_search_step(
            root,
            SearchStepType.EXPLORE,
            [self.start]
        )
        self.steps.append(step)

        # BFS loop
        while self.queue:
            # Actualizar estadísticas
            self.max_frontier_size = max(
                self.max_frontier_size, len(self.queue))

            # Obtener siguiente nodo
            current_node = self.queue.popleft()
            self.nodes_expanded += 1

            # Verificar si llegamos al objetivo
            if current_node.position == self.goal:
                step = self._create_search_step(
                    current_node,
                    SearchStepType.GOAL_FOUND,
                    [node.position for node in self.queue]
                )
                self.steps.append(step)

                return SearchResult(
                    success=True,
                    solution_path=self._reconstruct_path(current_node),
                    root_node=root,
                    steps=self.steps,
                    nodes_expanded=self.nodes_expanded,
                    max_frontier_size=self.max_frontier_size
                )

            # Explorar vecinos
            neighbors = self._get_neighbors(current_node.position)
            unvisited_neighbors = [
                n for n in neighbors if n not in self.visited]

            # Marcar punto de decisión si hay múltiples caminos
            if len(unvisited_neighbors) > 1:
                current_node.is_decision_point = True

            # Si no hay vecinos no visitados, es un callejón sin salida
            if len(unvisited_neighbors) == 0 and current_node.position != self.goal:
                current_node.is_dead_end = True
                step = self._create_search_step(
                    current_node,
                    SearchStepType.DEAD_END,
                    [node.position for node in self.queue]
                )
                self.steps.append(step)
                continue

            # Expandir vecinos
            for neighbor_pos in unvisited_neighbors:
                if neighbor_pos not in self.visited:
                    # Crear nodo hijo
                    neighbor_node = SearchNode(position=neighbor_pos)
                    current_node.add_child(neighbor_node)

                    # Marcar como visitado y agregar a la cola
                    self.visited.add(neighbor_pos)
                    self.queue.append(neighbor_node)

                    # Crear paso de búsqueda
                    step_type = (SearchStepType.DECISION
                                 if self._is_decision_point(neighbor_pos)
                                 else SearchStepType.EXPLORE)

                    step = self._create_search_step(
                        neighbor_node,
                        step_type,
                        [node.position for node in self.queue]
                    )
                    self.steps.append(step)

        # No se encontró solución
        return SearchResult(
            success=False,
            root_node=root,
            steps=self.steps,
            nodes_expanded=self.nodes_expanded,
            max_frontier_size=self.max_frontier_size
        )
