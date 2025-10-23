from typing import Tuple, Set, List

from src.core.map import Map
from src.app.config.config_manager import ConfigManager
from src.app.engines.graphics_engine import IGraphicsEngine
from src.app.services.visualization_state import VisualizationState

from .base_renderer import BaseRenderer


class SearchRenderer(BaseRenderer):
    """
    Renderizador especializado para visualizar el estado de búsqueda.

    Se encarga de dibujar la frontera, celdas visitadas, camino actual
    y camino solución sobre el mapa.
    """

    def __init__(self, graphics_engine: IGraphicsEngine, config_manager: ConfigManager):
        """
        Inicializa el renderizador de búsqueda.

        Args:
            graphics_engine: Motor gráfico para operaciones de renderizado
            config_manager: Gestor de configuración de visualización
        """
        super().__init__(graphics_engine, config_manager)

        # Colores para visualización
        self.color_frontier = (255, 255, 0)      # Amarillo para frontera
        self.color_visited = (200, 200, 255)     # Azul claro para visitadas
        self.color_current_path = (255, 200, 0)  # Naranja para camino actual
        self.color_solution = (0, 255, 0)        # Verde para solución
        self.color_start = (0, 255, 255)         # Cyan para inicio
        self.color_goal = (255, 0, 255)          # Magenta para objetivo

    def render(self, map_obj: Map, viz_state: VisualizationState) -> None:
        """
        Renderiza el estado de búsqueda sobre el mapa.

        Args:
            map_obj: El mapa base
            viz_state: Estado de visualización actual
        """
        if not viz_state.current_step and not viz_state.search_result:
            return

        # Renderizar en capas (de atrás hacia adelante)
        if viz_state.show_visited:
            self._render_visited(viz_state.visited_positions)

        if viz_state.show_frontier:
            self._render_frontier(viz_state.frontier_positions)

        if viz_state.show_path and viz_state.current_path:
            self._render_current_path(viz_state.current_path)

        # Renderizar solución si existe
        if viz_state.has_solution() and not viz_state.is_playing:
            self._render_solution_path(viz_state.solution_path)

    def _render_visited(self, visited: Set[Tuple[int, int]]) -> None:
        """
        Renderiza las celdas visitadas.

        Args:
            visited: Conjunto de posiciones visitadas
        """
        for position in visited:
            self._draw_cell_overlay(position, self.color_visited, alpha=0.3)

    def _render_frontier(self, frontier: Set[Tuple[int, int]]) -> None:
        """
        Renderiza la frontera (celdas en cola/pila).

        Args:
            frontier: Conjunto de posiciones en la frontera
        """
        for position in frontier:
            self._draw_cell_overlay(position, self.color_frontier, alpha=0.5)

    def _render_current_path(self, path: List[Tuple[int, int]]) -> None:
        """
        Renderiza el camino actual siendo explorado.

        Args:
            path: Lista de posiciones del camino
        """
        # Dibujar línea conectando el camino
        if len(path) > 1:
            points = [self._get_cell_center(pos) for pos in path]
            self._draw_path_line(points, self.color_current_path, width=3)

        # Destacar la posición actual (última del camino)
        if path:
            current = path[-1]
            self._draw_cell_border(current, self.color_current_path, width=3)

    def _render_solution_path(self, path: List[Tuple[int, int]]) -> None:
        """
        Renderiza el camino solución.

        Args:
            path: Lista de posiciones del camino solución
        """
        if len(path) > 1:
            points = [self._get_cell_center(pos) for pos in path]
            self._draw_path_line(points, self.color_solution, width=4)

        # Marcar inicio y final
        if path:
            self._draw_cell_border(path[0], self.color_start, width=3)
            self._draw_cell_border(path[-1], self.color_goal, width=3)

    def _draw_cell_overlay(
        self,
        position: Tuple[int, int],
        color: Tuple[int, int, int],
        alpha: float = 0.5
    ) -> None:
        """
        Dibuja una capa semi-transparente sobre una celda.

        Args:
            position: Posición de la celda (row, col)
            color: Color RGB
            alpha: Transparencia (0.0 a 1.0)
        """
        row, col = position
        x, y = self._cell_position(row, col)
        width, height = self._content_cell_size()

        # Simular transparencia mezclando con blanco
        blended_color = tuple(int(c * alpha + 255 * (1 - alpha))
                              for c in color)

        self.graphics_engine.draw_rectangle(x, y, width, height, blended_color)

    def _draw_cell_border(
        self,
        position: Tuple[int, int],
        color: Tuple[int, int, int],
        width: int = 2
    ) -> None:
        """
        Dibuja un borde alrededor de una celda.

        Args:
            position: Posición de la celda (row, col)
            color: Color RGB del borde
            width: Grosor del borde
        """
        row, col = position
        x, y = self._cell_position(row, col)
        cell_width, cell_height = self._content_cell_size()

        # Dibujar 4 líneas para formar el borde
        # Superior
        self.graphics_engine.draw_line(
            (x, y),
            (x + cell_width, y),
            color, width
        )
        # Inferior
        self.graphics_engine.draw_line(
            (x, y + cell_height),
            (x + cell_width, y + cell_height),
            color, width
        )
        # Izquierda
        self.graphics_engine.draw_line(
            (x, y),
            (x, y + cell_height),
            color, width
        )
        # Derecha
        self.graphics_engine.draw_line(
            (x + cell_width, y),
            (x + cell_width, y + cell_height),
            color, width
        )

    def _draw_path_line(
        self,
        points: List[Tuple[int, int]],
        color: Tuple[int, int, int],
        width: int = 2
    ) -> None:
        """
        Dibuja una línea conectando múltiples puntos.

        Args:
            points: Lista de puntos (x, y) a conectar
            color: Color RGB de la línea
            width: Grosor de la línea
        """
        for i in range(len(points) - 1):
            self.graphics_engine.draw_line(
                points[i],
                points[i + 1],
                color,
                width
            )

    def _get_cell_center(self, position: Tuple[int, int]) -> Tuple[int, int]:
        """
        Obtiene el centro de una celda en coordenadas de pantalla.

        Args:
            position: Posición de la celda (row, col)

        Returns:
            Tupla (x, y) del centro en píxeles
        """
        row, col = position
        x, y = self._cell_position(row, col)
        width, height = self._content_cell_size()

        return (x + width // 2, y + height // 2)
