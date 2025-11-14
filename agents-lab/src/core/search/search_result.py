from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .search_node import SearchNode


class SearchStepType(Enum):
    """Tipos de pasos en la búsqueda."""
    EXPLORE = "explore"  # Explorar nueva celda
    BACKTRACK = "backtrack"  # Retroceder
    DECISION = "decision"  # Punto de decisión
    GOAL_FOUND = "goal_found"  # Meta encontrada
    DEAD_END = "dead_end"  # Callejón sin salida


@dataclass
class SearchStep:
    """
    Representa un paso individual en el algoritmo de búsqueda.

    Usado para reproducir la búsqueda paso a paso.
    """
    node: SearchNode
    step_type: SearchStepType
    frontier: List[Tuple[int, int]]  # Estado de la frontera en este paso
    visited: List[Tuple[int, int]]  # Celdas visitadas hasta este paso
    current_path: List[Tuple[int, int]]  # Camino actual desde inicio

    def is_decision_step(self) -> bool:
        """Verifica si este es un paso de decisión."""
        return self.step_type == SearchStepType.DECISION or self.node.is_decision_point


@dataclass
class SearchResult:
    """
    Resultado de ejecutar un algoritmo de búsqueda.

    Contiene toda la información sobre la búsqueda: camino solución,
    árbol generado, estadísticas y pasos para reproducción.
    """
    success: bool
    solution_path: Optional[List[Tuple[int, int]]] = None
    root_node: Optional[SearchNode] = None
    steps: List[SearchStep] = None
    nodes_expanded: int = 0
    max_frontier_size: int = 0
    
    goal_node: Optional[SearchNode] = None
    path_cost: float = 0.0

    def __post_init__(self):
        """Inicializa listas si son None."""
        if self.steps is None:
            self.steps = []

    def get_decision_steps(self) -> List[SearchStep]:
        """
        Obtiene solo los pasos de decisión para reproducción de alto nivel.

        Returns:
            Lista de pasos donde se tomaron decisiones
        """
        return [step for step in self.steps if step.is_decision_step()]

    def get_all_visited_positions(self) -> List[Tuple[int, int]]:
        """
        Obtiene todas las posiciones visitadas durante la búsqueda.

        Returns:
            Lista de posiciones visitadas
        """
        if not self.steps:
            return []
        return self.steps[-1].visited

    def get_tree_nodes(self) -> List[SearchNode]:
        """
        Obtiene todos los nodos del árbol de búsqueda en orden BFS.

        Returns:
            Lista de todos los nodos
        """
        if not self.root_node:
            return []

        nodes = []
        queue = [self.root_node]

        while queue:
            node = queue.pop(0)
            nodes.append(node)
            queue.extend(node.children)

        return nodes

    def __str__(self) -> str:
        """Representación string del resultado."""
        status = "Éxito" if self.success else "Fallo"
        path_len = len(self.solution_path) if self.solution_path else 0
        return (f"SearchResult(status={status}, path_length={path_len}, "
                f"nodes_expanded={self.nodes_expanded}, steps={len(self.steps)})")
