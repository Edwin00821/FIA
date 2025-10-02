from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Tuple
from .map import Map


class Direction(Enum):
    """Direcciones para el ser."""
    UP = "Arriba"
    DOWN = "Abajo"
    RIGHT = "Derecha"
    LEFT = "Izquirda"


class Sensor(ABC):
    """
    Interfaz abstracta para sensores de agentes.

    Los sensores permiten a los agentes percibir el entorno circundante.
    """

    @abstractmethod
    def perceive(self, map_obj: Map, position: Tuple[int, int], direction: Direction) -> Dict[str, bool]:
        """
        Percibe el entorno desde una posición y dirección dadas.

        Args:
            map_obj: El mapa del entorno
            position: Tupla (row, col) de la posición del agente
            direction: Dirección hacia la que mira el agente

        Returns:
            Dict con información percibida (e.g., {'front': True, 'left': False})
        """
        pass

    def _is_valid_position(self, map_obj: Map, position: Tuple[int, int]) -> bool:
        """Verifica si una posición está dentro de los límites del mapa."""
        row, col = position
        return 0 <= row < map_obj.rows and 0 <= col < map_obj.cols


class FrontSensor(Sensor):
    """
    Sensor que solo percibe la celda frontal.

    Ideal para agentes con percepción limitada.
    """

    def perceive(self, map_obj: Map, position: Tuple[int, int], direction: Direction) -> Dict[str, bool]:
        """
        Percibe solo la celda directamente al frente.

        Returns:
            {'front': True} si la celda frontal es transitable, False si no o fuera del mapa
        """
        row, col = position
        front_pos = self._get_front_position(row, col, direction)

        if self._is_valid_position(map_obj, front_pos):
            cell = map_obj.grid[front_pos[0]][front_pos[1]]
            cell.discover()

            return {'front': cell.is_passable()}
        else:
            return {'front': False}

    def _get_front_position(self, row: int, col: int, direction: Direction) -> Tuple[int, int]:
        """Calcula la posición frontal basada en la dirección."""
        if direction == Direction.UP:
            return (row - 1, col)
        elif direction == Direction.DOWN:
            return (row + 1, col)
        elif direction == Direction.RIGHT:
            return (row, col + 1)
        elif direction == Direction.LEFT:
            return (row, col - 1)


class AllDirectionsSensor(Sensor):
    """
    Sensor que percibe en todas las direcciones cardinales.

    Proporciona percepción completa del entorno inmediato.
    """

    def perceive(self, map_obj: Map, position: Tuple[int, int], direction: Direction) -> Dict[str, bool]:
        """
        Percibe las celdas en todas las direcciones cardinales.

        Returns:
            {'up': bool, 'down': bool, 'right': bool, 'left': bool}
            True si la celda es transitable, False si no o fuera del mapa
        """
        row, col = position
        perceptions = {}

        for dir_enum in Direction:
            adjacent_pos = self._get_adjacent_position(row, col, dir_enum)
            if self._is_valid_position(map_obj, adjacent_pos):
                cell = map_obj.grid[adjacent_pos[0]][adjacent_pos[1]]
                cell.discover()
                perceptions[dir_enum.value.lower()] = cell.is_passable()
            else:
                perceptions[dir_enum.value.lower()] = False

        return perceptions

    def _get_adjacent_position(self, row: int, col: int, direction: Direction) -> Tuple[int, int]:
        """Calcula la posición adyacente en una dirección dada."""
        if direction == Direction.UP:
            return (row - 1, col)
        elif direction == Direction.DOWN:
            return (row + 1, col)
        elif direction == Direction.RIGHT:
            return (row, col + 1)
        elif direction == Direction.LEFT:
            return (row, col - 1)
