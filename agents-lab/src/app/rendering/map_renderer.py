from typing import Tuple

from src.core.map import Map

from src.app.config.config_manager import ConfigManager, DisplayConfig

from src.app.engines.graphics_engine import IGraphicsEngine

from .header_renderer import HeaderRenderer
from .grid_renderer import GridRenderer
from .terrain_renderer import TerrainRenderer
from .marks_renderer import MarksRenderer


class MapRenderer:
    """
    Renderizador responsable de dibujar mapas en una superficie de pygame.

    Utiliza el patrón Strategy al separar la lógica de renderizado
    de la lógica del mapa.
    """

    def __init__(self, graphics_engine: IGraphicsEngine, config_manager: ConfigManager):
        """
        Inicializar el renderizador con el motor gráfico y la configuración.

        Args:
            graphics_engine: Motor gráfico para operaciones de renderizado.
            config_manager: Gestor de configuración de visualización.
        """
        self.gfx = graphics_engine
        self.disp = config_manager.display
        self.config_manager = config_manager

        self.header_renderer = HeaderRenderer(graphics_engine, config_manager)
        
        self.grid_renderer = GridRenderer(graphics_engine, config_manager)
        
        self.terrain_renderer = TerrainRenderer(
            graphics_engine, config_manager)
        
        self.marks_renderer = MarksRenderer(graphics_engine, config_manager)

    def render_map(self, map_obj: Map) -> None:
        """
        Renderizar completamente un mapa en la pantalla.

        Args:
            map_obj: El mapa a renderizar.
        """
        self._clear_screen()

        self.header_renderer.render(map_obj)
        self.grid_renderer.render(map_obj)
        self.terrain_renderer.render(map_obj)
        self.marks_renderer.render(map_obj)

        self.gfx.present()

    def _clear_screen(self) -> None:
        """Limpiar la pantalla con el color de fondo."""
        self.gfx.clear_screen(self.disp.COLOR_BG)

    @staticmethod
    def calculate_window_size(map_obj: Map, display_config: DisplayConfig) -> Tuple[int, int]:
        """
        Calcular el tamaño necesario de la ventana para mostrar el mapa completo.

        Args:
            map_obj: El mapa para calcular dimensiones.
            display_config: Configuración de visualización.

        Returns:
            (ancho, alto) en píxeles.
        """
        width = display_config.HEADER_WIDTH + \
            map_obj.cols * display_config.CELL_WIDTH + 20
        height = display_config.HEADER_HEIGHT + \
            map_obj.rows * display_config.CELL_HEIGHT + 20
        return width, height
