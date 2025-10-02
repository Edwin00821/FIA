from abc import ABC, abstractmethod
from typing import Tuple

from .map import Map
from .sensors import Direction


class Action(ABC):
    """
    Interfaz abstracta para acciones que puede realizar un agente.

    Las acciones modifican el estado del agente (posición y dirección).
    """

    @abstractmethod
    def execute(self, position: Tuple[int, int], direction: Direction) -> Tuple[Tuple[int, int], Direction]:
        """
        Ejecuta la acción desde una posición y dirección dadas.

        Args:
            position: Tupla (row, col) actual del agente
            direction: Dirección actual del agente

        Returns:
            Tupla (nueva_posición, nueva_dirección)
        """
        pass

    @abstractmethod
    def is_valid(self, position: Tuple[int, int], direction: Direction, map_obj: Map) -> bool:
        """
        Verifica si la acción es válida en el contexto actual.

        Args:
            position: Posición actual
            direction: Dirección actual
            map_obj: El mapa para verificar límites y terreno

        Returns:
            True si la acción puede ejecutarse
        """
        pass


class TurnLeft(Action):
    """Acción para girar 90 grados a la izquierda."""

    def execute(self, position: Tuple[int, int], direction: Direction) -> Tuple[Tuple[int, int], Direction]:
        """Gira a la izquierda manteniendo la posición."""
        new_direction = self._get_left_direction(direction)
        return (position, new_direction)

    def is_valid(self, position: Tuple[int, int], direction: Direction, map_obj: Map) -> bool:
        """Siempre válido, solo cambia dirección."""
        return True

    def _get_left_direction(self, direction: Direction) -> Direction:
        """Obtiene la dirección resultante de girar a la izquierda."""
        directions = [Direction.UP, Direction.RIGHT,
                      Direction.DOWN, Direction.LEFT]
        current_index = directions.index(direction)
        return directions[(current_index - 1) % 4]


class TurnRight(Action):
    """Acción para girar 90 grados a la derecha."""

    def execute(self, position: Tuple[int, int], direction: Direction) -> Tuple[Tuple[int, int], Direction]:
        """Gira a la derecha manteniendo la posición."""
        new_direction = self._get_right_direction(direction)
        return (position, new_direction)

    def is_valid(self, position: Tuple[int, int], direction: Direction, map_obj: Map) -> bool:
        """Siempre válido, solo cambia dirección."""
        return True

    def _get_right_direction(self, direction: Direction) -> Direction:
        """Obtiene la dirección resultante de girar a la derecha."""
        directions = [Direction.UP, Direction.RIGHT,
                      Direction.DOWN, Direction.LEFT]
        current_index = directions.index(direction)
        return directions[(current_index + 1) % 4]


class MoveForward(Action):
    """Acción para moverse hacia adelante en la dirección actual."""

    def execute(self, position: Tuple[int, int], direction: Direction) -> Tuple[Tuple[int, int], Direction]:
        """Se mueve una celda hacia adelante."""
        row, col = position
        if direction == Direction.UP:
            new_position = (row - 1, col)
        elif direction == Direction.DOWN:
            new_position = (row + 1, col)
        elif direction == Direction.RIGHT:
            new_position = (row, col + 1)
        elif direction == Direction.LEFT:
            new_position = (row, col - 1)
        return (new_position, direction)

    def is_valid(self, position: Tuple[int, int], direction: Direction, map_obj: Map) -> bool:
        """Verifica que la celda frontal sea transitable."""
        row, col = position
        if direction == Direction.UP:
            target = (row - 1, col)
        elif direction == Direction.DOWN:
            target = (row + 1, col)
        elif direction == Direction.RIGHT:
            target = (row, col + 1)
        elif direction == Direction.LEFT:
            target = (row, col - 1)

        # Verificar límites del mapa
        if not (0 <= target[0] < map_obj.rows and 0 <= target[1] < map_obj.cols):
            return False

        # Verificar que la celda sea transitable
        cell = map_obj.grid[target[0]][target[1]]
        return cell.is_passable()


class MoveUp(Action):
    """Acción para moverse hacia el arriba."""

    def execute(self, position: Tuple[int, int], direction: Direction) -> Tuple[Tuple[int, int], Direction]:
        """Se mueve una celda hacia el arriba."""
        row, col = position
        return ((row - 1, col), direction)

    def is_valid(self, position: Tuple[int, int], direction: Direction, map_obj: Map) -> bool:
        """Verifica que la celda de arriba sea transitable."""
        row, col = position
        target = (row - 1, col)
        if not (0 <= target[0] < map_obj.rows and 0 <= target[1] < map_obj.cols):
            return False
        cell = map_obj.grid[target[0]][target[1]]
        return cell.is_passable()


class MoveDown(Action):
    """Acción para moverse hacia abajo."""

    def execute(self, position: Tuple[int, int], direction: Direction) -> Tuple[Tuple[int, int], Direction]:
        """Se mueve una celda hacia abajo."""
        row, col = position
        return ((row + 1, col), direction)

    def is_valid(self, position: Tuple[int, int], direction: Direction, map_obj: Map) -> bool:
        """Verifica que la celda sur sea transitable."""
        row, col = position
        target = (row + 1, col)
        if not (0 <= target[0] < map_obj.rows and 0 <= target[1] < map_obj.cols):
            return False
        cell = map_obj.grid[target[0]][target[1]]
        return cell.is_passable()


class MoveRight(Action):
    """Acción para moverse hacia la derecha."""

    def execute(self, position: Tuple[int, int], direction: Direction) -> Tuple[Tuple[int, int], Direction]:
        """Se mueve una celda hacia la derecha."""
        row, col = position
        return ((row, col + 1), direction)

    def is_valid(self, position: Tuple[int, int], direction: Direction, map_obj: Map) -> bool:
        """Verifica que la celda a la derecha sea transitable."""
        row, col = position
        target = (row, col + 1)
        if not (0 <= target[0] < map_obj.rows and 0 <= target[1] < map_obj.cols):
            return False
        cell = map_obj.grid[target[0]][target[1]]
        return cell.is_passable()


class MoveLeft(Action):
    """Acción para moverse hacia la izquierda."""

    def execute(self, position: Tuple[int, int], direction: Direction) -> Tuple[Tuple[int, int], Direction]:
        """Se mueve una celda hacia la izquierda."""
        row, col = position
        return ((row, col - 1), direction)

    def is_valid(self, position: Tuple[int, int], direction: Direction, map_obj: Map) -> bool:
        """Verifica que la celda a la izquierda sea transitable."""
        row, col = position
        target = (row, col - 1)
        if not (0 <= target[0] < map_obj.rows and 0 <= target[1] < map_obj.cols):
            return False
        cell = map_obj.grid[target[0]][target[1]]
        return cell.is_passable()
