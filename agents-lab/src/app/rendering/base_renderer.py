from abc import ABC, abstractmethod
from typing import Tuple

from src.core.map import Map

from src.app.config.config_manager import ConfigManager

from src.app.engines.graphics_engine import IGraphicsEngine


class BaseRenderer(ABC):
    """
    Clase base para todos los renderizadores especializados.

    Proporciona métodos comunes para cálculos de layout y posicionamiento,
    evitando dependencias directas del ConfigManager en cada renderizador.
    """

    def __init__(self, graphics_engine: IGraphicsEngine, config_manager: ConfigManager):
        """
        Inicializa el renderizador base.

        Args:
            graphics_engine: Motor gráfico para operaciones de renderizado
            config_manager: Gestor de configuración de visualización.
        """
        self.graphics_engine = graphics_engine
        self.config = config_manager
        self.disp = config_manager.display

    @abstractmethod
    def render(self, map_obj: Map) -> None:
        """
        Método abstracto que debe implementar cada renderizador especializado.

        Args:
            map_obj: El mapa a renderizar
        """
        pass

    # Métodos de utilidad para cálculos de layout

    def _cell_size(self) -> Tuple[int, int]:
        """
        Obtiene el tamaño de una celda.

        Returns:
            Tupla (ancho, alto) de una celda en píxeles
        """
        cell_width = self.disp.CELL_WIDTH
        cell_height = self.disp.CELL_HEIGHT

        return cell_width, cell_height

    def _header_size(self) -> Tuple[int, int]:
        """
        Obtiene el tamaño del área de encabezados.

        Returns:
            Tupla (ancho, alto) del área de encabezados en píxeles
        """
        header_width = self.disp.HEADER_WIDTH
        header_height = self.disp.HEADER_HEIGHT

        return header_width, header_height

    def _border_width(self) -> int:
        """
        Obtiene el grosor del borde.
        
        Returns:
            Grosor del borde en píxeles
        """
        return self.disp.BORDER_WIDTH

    def _cell_position(self, row: int, col: int) -> Tuple[int, int]:
        """
        Calcula la posición de una celda en píxeles (esquina superior izquierda).

        Args:
            row: Fila de la celda
            col: Columna de la celda

        Returns:
            Tupla (x, y) de la posición en píxeles
        """
        x = self.disp.HEADER_WIDTH + col * self.disp.CELL_WIDTH + self.disp.BORDER_WIDTH
        y = self.disp.HEADER_HEIGHT + row * self.disp.CELL_HEIGHT + self.disp.BORDER_WIDTH
        return x, y

    def _header_position(self, index: int, axis: str) -> Tuple[int, int]:
        """
        Calcula la posición de un encabezado de fila o columna.

        Args:
            index: Índice de la fila o columna
            axis: "col" para columnas, "row" para filas

        Returns:
            Tupla (x, y) de la posición central del encabezado
        """
        if axis == "col":
            x = index * self.disp.CELL_WIDTH + \
                self.disp.HEADER_WIDTH + self.disp.CELL_WIDTH // 2
            y = self.disp.HEADER_HEIGHT // 2
        else:  # "row"
            x = self.disp.HEADER_WIDTH // 2
            y = self.disp.HEADER_HEIGHT + index * \
                self.disp.CELL_HEIGHT + self.disp.CELL_HEIGHT // 2
        return x, y

    def _grid_dimensions(self, map_obj: Map) -> Tuple[int, int]:
        """
        Calcula las dimensiones totales del área de la grilla.

        Args:
            map_obj: El mapa para calcular dimensiones

        Returns:
            Tupla (ancho, alto) del área total de la grilla
        """
        width = self.disp.HEADER_WIDTH + map_obj.cols * self.disp.CELL_WIDTH
        height = self.disp.HEADER_HEIGHT + map_obj.rows * self.disp.CELL_HEIGHT
        return width, height

    def _content_cell_size(self) -> Tuple[int, int]:
        """
        Obtiene el tamaño del contenido de una celda (sin bordes).

        Returns:
            Tupla (ancho, alto) del contenido de la celda
        """
        return (
            self.disp.CELL_WIDTH - self.disp.BORDER_WIDTH,
            self.disp.CELL_HEIGHT - self.disp.BORDER_WIDTH
        )
