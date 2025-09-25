from src.core.map import Map

from src.app.config.config_manager import ConfigManager

from src.app.engines.graphics_engine import IGraphicsEngine

from .base_renderer import BaseRenderer


class HeaderRenderer(BaseRenderer):
    """
    Renderizador especializado para los encabezados del mapa.

    Se encarga únicamente de dibujar las etiquetas de filas (números) 
    y columnas (letras) que permiten identificar las coordenadas.
    """

    def __init__(self, graphics_engine: IGraphicsEngine, config_manager: ConfigManager):
        """
        Inicializa el renderizador de encabezados.

        Args:
            graphics_engine: Motor gráfico para operaciones de renderizado
            config_manager: Gestor de configuración de visualización.
        """
        self.gfx = graphics_engine
        self.config_manager = config_manager
        self.disp = config_manager.display

    def render(self, map_obj: Map) -> None:
        """
        Renderiza los encabezados de filas y columnas para el mapa.

        Args:
            map_obj: El mapa para obtener dimensiones
        """
        self._draw_column_headers(map_obj)
        self._draw_row_headers(map_obj)

    def _draw_column_headers(self, map_obj: Map) -> None:
        """
        Dibuja los encabezados de columnas (A, B, C, ...).

        Args:
            map_obj: El mapa para obtener dimensiones
        """
        for col in range(map_obj.cols):
            letter = chr(ord('A') + col)

            x, y = self._header_position(col, axis="col")

            self.gfx.draw_text(letter, x, y, self.disp.COLOR_TEXT)

    def _draw_row_headers(self, map_obj: Map) -> None:
        """
        Dibuja los encabezados de filas (1, 2, 3, ...).

        Args:
            map_obj: El mapa para obtener dimensiones
        """
        for row in range(map_obj.rows):
            number = str(row + 1)

            x, y = self._header_position(row, axis="row")

            self.gfx.draw_text(number, x, y, self.disp.COLOR_TEXT)
