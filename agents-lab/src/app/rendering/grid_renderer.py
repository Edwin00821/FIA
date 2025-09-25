from src.core.map import Map

from src.app.config.config_manager import ConfigManager

from src.app.engines.graphics_engine import IGraphicsEngine

from .base_renderer import BaseRenderer


class GridRenderer(BaseRenderer):
    """
    Renderizador especializado para las líneas de la grilla del mapa.

    Se encarga únicamente de dibujar las líneas que forman la cuadrícula
    sobre la cual se visualiza el mapa.
    """

    def __init__(self, graphics_engine: IGraphicsEngine, config_manager: ConfigManager):
        """
        Inicializa el renderizador de grilla.

        Args:
            graphics_engine: Motor gráfico para operaciones de renderizado
            config_manager: Gestor de configuración de visualización.
        """
        self.gfx = graphics_engine
        self.config_manager = config_manager
        self.disp = config_manager.display

    def render(self, map_obj: Map) -> None:
        """
        Renderiza las líneas de la grilla para el mapa.

        Args:
            map_obj: El mapa para obtener dimensiones
        """
        self._draw_vertical_lines(map_obj)
        self._draw_horizontal_lines(map_obj)

    def _draw_vertical_lines(self, map_obj: Map) -> None:
        """
        Dibuja las líneas verticales de la grilla.

        Args:
            map_obj: El mapa para obtener dimensiones
        """
        _header_width, header_height = self._header_size()
        cell_width, cell_height = self._cell_size()

        height = header_height + map_obj.rows * cell_height

        for col in range(map_obj.cols + 2):

            x = col * cell_width

            self.gfx.draw_line(
                (x, 0),
                (x, height),
                self.disp.COLOR_BORDER,
                self.disp.BORDER_WIDTH
            )

    def _draw_horizontal_lines(self, map_obj: Map) -> None:
        """
        Dibuja las líneas horizontales de la grilla.

        Args:
            map_obj: El mapa para obtener dimensiones
        """
        header_width, _header_height = self._header_size()
        cell_width, cell_height = self._cell_size()

        width = header_width + map_obj.cols * cell_width

        for row in range(map_obj.rows + 2):
            y = row * cell_height

            self.gfx.draw_line(
                (0, y),
                (width, y),
                self.disp.COLOR_BORDER,
                self.disp.BORDER_WIDTH
            )
