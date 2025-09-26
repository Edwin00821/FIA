from src.core.map import Map
from src.core.cell import Cell

from src.app.config.config_manager import ConfigManager
from src.app.engines.graphics_engine import IGraphicsEngine

from .base_renderer import BaseRenderer


class MarksRenderer(BaseRenderer):
    """
    Renderizador especializado para las marcas de las celdas.

    Se encarga únicamente de dibujar las marcas superpuestas
    sobre el terreno de las celdas.
    """

    def __init__(self, graphics_engine: IGraphicsEngine, config_manager: ConfigManager):
        """
        Inicializa el renderizador de marcas.

        Args:
            graphics_engine: Motor gráfico para operaciones de renderizado
            config_manager: Gestor de configuración de visualización
        """
        self.gfx = graphics_engine
        self.config_manager = config_manager
        self.disp = config_manager.display

    def render(self, map_obj: Map) -> None:
        """
        Renderiza las marcas de todas las celdas del mapa.

        Args:
            map_obj: El mapa a renderizar
        """
        for row in range(map_obj.rows):
            for col in range(map_obj.cols):
                cell = map_obj.grid[row][col]
                if cell.marks:
                    self._draw_cell_marks(cell, row, col)

    def _draw_cell_marks(self, cell: Cell, row: int, col: int) -> None:
        """
        Dibuja las marcas de una celda específica.

        Args:
            cell: Celda con las marcas
            row: Fila de la celda
            col: Columna de la celda
        """
        x, y = self._cell_position(row, col)
        cell_width, cell_height = self._cell_size()

        center_x = x + cell_width // 2
        center_y = y + cell_height // 2

        self.gfx.draw_text(cell.get_marks_display(), center_x,
                           center_y, self.disp.COLOR_TEXT)
