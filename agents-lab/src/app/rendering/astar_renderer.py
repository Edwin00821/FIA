from typing import Optional

from src.core.map import Map
from src.core.cell import CellMark
from src.app.config.config_manager import ConfigManager
from src.app.engines.graphics_engine import IGraphicsEngine
from src.app.services.astar_visualization_state import AStarVisualizationState

from .base_renderer import BaseRenderer


class AStarRenderer(BaseRenderer):
    """
    Renderizador especializado para visualización de A*.

    Muestra marcas O (open), X (closed) y costos f(n) en cada celda.
    """

    def __init__(self, graphics_engine: IGraphicsEngine, config_manager: ConfigManager):
        """
        Inicializa el renderizador de A*.

        Args:
            graphics_engine: Motor gráfico para operaciones de renderizado
            config_manager: Gestor de configuración de visualización
        """
        super().__init__(graphics_engine, config_manager)
        self.color_open = (144, 238, 144)    # Verde claro para open
        self.color_closed = (169, 169, 169)  # Gris para closed

    def render(self, map_obj: Map, viz_state: Optional[AStarVisualizationState] = None) -> None:
        """
        Renderiza el estado de A* sobre el mapa.

        Args:
            map_obj: El mapa base
            viz_state: Estado de visualización de A*
        """
        if not viz_state or not viz_state.is_active:
            return

        # Renderizar marcas y costos en cada celda
        for position, node_info in viz_state.nodes_info.items():
            self._render_node(map_obj, position, node_info)

    def _render_node(self, map_obj: Map, position, node_info) -> None:
        """
        Renderiza un nodo individual con su marca y costo.

        Args:
            map_obj: El mapa
            position: Posición del nodo
            node_info: Información del nodo
        """
        row, col = position

        # Verificar que la celda sea visible
        cell = map_obj.grid[row][col]
        if not cell.is_visible():
            return
        
        x, y = self._cell_position(row, col)
        cell_width, cell_height = self._cell_size()
        
        cost_text = f"{node_info.f_cost:.0f}"

        # Dibujar marca (O o X)
        mark_y = y + cell_height // 4
        if node_info.is_open:
            # cell.add_mark(CellMark.OPEN)
            self.graphics_engine.draw_text(
                f"O({cost_text})", x + cell_width // 2, mark_y, (0, 128, 0))
        elif node_info.is_closed:
            # cell.add_mark(CellMark.CLOSED)
            self.graphics_engine.draw_text(
                f"X({cost_text})", x + cell_width // 2, mark_y, (128, 0, 0))
