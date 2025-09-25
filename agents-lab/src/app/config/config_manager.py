from dataclasses import dataclass
from typing import Tuple, Dict

from src.core.cell import TerrainType


@dataclass
class AppConfig:
    """Configuración general de la aplicación."""
    DEFAULT_MAP_PATH: str = "data/maze.txt"
    DATA_DIRECTORY: str = "data"
    WINDOW_TITLE: str = "FIA - Fundamentos de Inteligencia Artificial"


@dataclass
class DisplayConfig:
    """Configuración de la pantalla y visualización."""
    HEADER_WIDTH: int = 60
    HEADER_HEIGHT: int = 40
    CELL_WIDTH: int = 60
    CELL_HEIGHT: int = 40

    FONT_SIZE: int = 16
    FPS: int = 30
    BORDER_WIDTH: int = 1

    # Colores de interfaz
    COLOR_BG: Tuple[int, int, int] = (168, 168, 168)
    COLOR_BORDER: Tuple[int, int, int] = (0, 0, 0)
    COLOR_TEXT: Tuple[int, int, int] = (0, 0, 0)
    COLOR_HEADER: Tuple[int, int, int] = (200, 200, 200)


class ConfigManager:
    """
    Gestor centralizado de configuración usando el patrón Singleton.

    Proporciona acceso unificado a todas las configuraciones de la aplicación.
    """

    _instance = None

    def __new__(cls) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.app = AppConfig()
        self.display = DisplayConfig()

        # Mapeo de tipos de terreno a colores
        self.terrain_colors: Dict[TerrainType, Tuple[int, int, int]] = {
            TerrainType.WALL: (128, 128, 128),  # Gris para muros
            TerrainType.ROAD: (255, 255, 255),  # Blanco para caminos
        }

        self._initialized = True

    def get_terrain_color(self, terrain_type: TerrainType) -> Tuple[int, int, int]:
        """
        Obtiene el color asociado a un tipo de terreno.

        Args:
            terrain_type: Tipo de terreno

        Returns:
            Tuple con color RGB
        """
        return self.terrain_colors.get(terrain_type, (0, 0, 0))
