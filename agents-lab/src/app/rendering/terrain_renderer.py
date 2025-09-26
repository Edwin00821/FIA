from src.core.map import Map

from src.app.config.config_manager import ConfigManager

from src.app.engines.graphics_engine import IGraphicsEngine

from .base_renderer import BaseRenderer


class TerrainRenderer(BaseRenderer):
    """
    Renderizador especializado para el terreno de las celdas del mapa.

    Se encarga únicamente de dibujar las celdas con sus respectivos colores
    según el tipo de terreno.
    """

    def __init__(self, graphics_engine: IGraphicsEngine, config_manager: ConfigManager):
        """
        Inicializa el renderizador de terreno.

        Args:
            graphics_engine: Motor gráfico para operaciones de renderizado
            config_manager: Gestor de configuración de visualización.
        """
        self.gfx = graphics_engine
        self.config_manager = config_manager
        self.disp = config_manager.display

    def render(self, map_obj: Map) -> None:
        """
        Renderiza el terreno de todas las celdas del mapa.

        Args:
            map_obj: El mapa a renderizar
        """
        for row in range(map_obj.rows):
            for col in range(map_obj.cols):
                self._draw_cell(map_obj, row, col)

    def _draw_cell(self, map_obj: Map, row: int, col: int) -> None:
        """
        Dibuja una celda individual del mapa.

        Args:
            map_obj: El mapa que contiene la celda
            row: Fila de la celda
            col: Columna de la celda
        """
        cell = map_obj.grid[row][col]

        border = self._border_width()
        cell_width, cell_height = self._cell_size()

        x, y = self._cell_position(row, col)

        # Determinar color y tamaño de la celda
        if cell.is_visible():
            color = self.config_manager.get_terrain_color(cell.terrain)
            draw_width = cell_width - border
            draw_height = cell_height - border
        else:
            color = self.disp.COLOR_UNKNOWN
            draw_width = cell_width
            draw_height = cell_height

        # Dibujar la celda
        self.gfx.draw_rectangle(x, y, draw_width, draw_height, color)
