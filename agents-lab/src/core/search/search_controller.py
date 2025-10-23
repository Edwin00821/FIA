from typing import Optional
from enum import Enum

from src.core.map import Map
from .search_result import SearchResult
from .bfs import BreadthFirstSearch
from .dfs import DepthFirstSearch


class SearchAlgorithmType(Enum):
    """Tipos de algoritmos de búsqueda disponibles."""
    BFS = "bfs"
    DFS = "dfs"


class SearchController:
    """
    Controlador para gestionar la ejecución de algoritmos de búsqueda.

    Proporciona una interfaz unificada para ejecutar diferentes algoritmos
    y gestionar sus resultados.
    """

    def __init__(self):
        """Inicializa el controlador de búsqueda."""
        self.current_result: Optional[SearchResult] = None
        self.is_searching = False

    def execute_search(
        self,
        algorithm_type: SearchAlgorithmType,
        map_obj: Map,
        start_pos: tuple,
        goal_pos: tuple,
        **kwargs
    ) -> SearchResult:
        """
        Ejecuta un algoritmo de búsqueda.

        Args:
            algorithm_type: Tipo de algoritmo a ejecutar
            map_obj: Mapa donde buscar
            start_pos: Posición inicial
            goal_pos: Posición objetivo
            **kwargs: Argumentos adicionales específicos del algoritmo

        Returns:
            SearchResult con el resultado
        """
        self.is_searching = True

        try:
            if algorithm_type == SearchAlgorithmType.BFS:
                algorithm = BreadthFirstSearch(map_obj, start_pos, goal_pos)
            elif algorithm_type == SearchAlgorithmType.DFS:
                direction_priority = kwargs.get('direction_priority', None)
                algorithm = DepthFirstSearch(
                    map_obj, start_pos, goal_pos, direction_priority
                )
            else:
                raise ValueError(
                    f"Tipo de algoritmo desconocido: {algorithm_type}")

            self.current_result = algorithm.search()
            return self.current_result

        finally:
            self.is_searching = False

    def get_last_result(self) -> Optional[SearchResult]:
        """
        Obtiene el último resultado de búsqueda.

        Returns:
            SearchResult del último algoritmo ejecutado, o None
        """
        return self.current_result

    def clear_result(self) -> None:
        """Limpia el resultado actual."""
        self.current_result = None

    def has_result(self) -> bool:
        """
        Verifica si hay un resultado disponible.

        Returns:
            True si hay un resultado
        """
        return self.current_result is not None
