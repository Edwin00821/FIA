from typing import Tuple, Optional
from dataclasses import dataclass

from src.core.map import Map
from src.app.config.config_manager import ConfigManager


@dataclass
class MapCoordinate:
    """
    Representa una coordenada en el mapa.

    Attributes:
        row: Fila (0-indexada)
        col: Columna (0-indexada)
        human_format: Formato humano legible (ej. "7,A")
    """
    row: int
    col: int
    human_format: str


class CoordinateSystem:
    """
    Sistema de conversión entre diferentes tipos de coordenadas del mapa.

    Maneja las conversiones entre:
    - Coordenadas de pantalla (píxeles)
    - Coordenadas de mapa (row, col)
    - Formato humano (número, letra)
    """

    def __init__(self, config_manager: ConfigManager):
        """
        Inicializa el sistema de coordenadas.

        Args:
            config_manager: Gestor de configuración para obtener dimensiones
        """
        self.config = config_manager
        self.disp = config_manager.display

    def screen_to_map(self, screen_x: int, screen_y: int, map_obj: Map) -> Optional[MapCoordinate]:
        """
        Convierte coordenadas de pantalla a coordenadas del mapa.

        Args:
            screen_x: Posición X en píxeles
            screen_y: Posición Y en píxeles
            map_obj: Mapa para validar límites

        Returns:
            MapCoordinate si las coordenadas están dentro del mapa, None en caso contrario
        """
        # Verificar si el click está dentro del área de celdas (no en headers)
        if (screen_x < self.disp.HEADER_WIDTH or
                screen_y < self.disp.HEADER_HEIGHT):
            return None

        # Calcular coordenadas del mapa
        col = (screen_x - self.disp.HEADER_WIDTH) // self.disp.CELL_WIDTH
        row = (screen_y - self.disp.HEADER_HEIGHT) // self.disp.CELL_HEIGHT

        # Validar límites
        if (0 <= row < map_obj.rows and 0 <= col < map_obj.cols):
            human_format = self._to_human_format(row, col)
            return MapCoordinate(row, col, human_format)

        return None

    def map_to_screen(self, row: int, col: int) -> Tuple[int, int]:
        """
        Convierte coordenadas del mapa a coordenadas de pantalla (centro de la celda).

        Args:
            row: Fila del mapa
            col: Columna del mapa

        Returns:
            Tupla (x, y) del centro de la celda en píxeles
        """
        x = (self.disp.HEADER_WIDTH +
             col * self.disp.CELL_WIDTH +
             self.disp.CELL_WIDTH // 2)
        y = (self.disp.HEADER_HEIGHT +
             row * self.disp.CELL_HEIGHT +
             self.disp.CELL_HEIGHT // 2)

        return x, y

    def human_to_map(self, human_coord: str, map_obj: Map) -> Optional[MapCoordinate]:
        """
        Convierte formato humano a coordenadas del mapa.

        Args:
            human_coord: Coordenada en formato humano (ej. "7,A" o "7A")
            map_obj: Mapa para validar límites

        Returns:
            MapCoordinate si es válida, None en caso contrario
        """
        try:
            # Limpiar la entrada
            coord_str = human_coord.strip().upper().replace(" ", "")

            # Separar por coma si existe
            if "," in coord_str:
                parts = coord_str.split(",")
                if len(parts) != 2:
                    return None
                row_str, col_str = parts[0].strip(), parts[1].strip()
            else:
                # Separar número y letra
                row_str = ""
                col_str = ""
                for char in coord_str:
                    if char.isdigit():
                        row_str += char
                    elif char.isalpha():
                        col_str += char
                        break

                if not row_str or not col_str:
                    return None

            # Convertir a índices 0-indexados
            row = int(row_str) - 1  # Convertir de 1-indexado a 0-indexado
            col = ord(col_str[0]) - ord('A')  # Convertir letra a índice

            # Validar límites
            if (0 <= row < map_obj.rows and 0 <= col < map_obj.cols):
                human_format = self._to_human_format(row, col)
                return MapCoordinate(row, col, human_format)

            return None

        except (ValueError, IndexError):
            return None

    def _to_human_format(self, row: int, col: int) -> str:
        """
        Convierte índices del mapa a formato humano legible.

        Args:
            row: Fila (0-indexada)
            col: Columna (0-indexada)

        Returns:
            Coordenada en formato humano (ej. "7,A")
        """
        human_row = row + 1  # Convertir a 1-indexado
        human_col = chr(ord('A') + col)  # Convertir a letra
        return f"({human_row},{human_col})"
