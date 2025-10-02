from src.core.agent import Agent
from src.core.sensors import FrontSensor, AllDirectionsSensor, Direction
from src.core.actions import TurnLeft, TurnRight, MoveForward, MoveUp, MoveDown, MoveRight, MoveLeft
from src.core.cell import CellMark

from src.app.events.event_bus import EventBus


class ContinuousMover:
    """
    Mixin que proporciona funcionalidad de movimiento continuo.

    Contiene métodos para realizar movimientos continuos hasta puntos de decisión o final.
    """

    def _perform_continuous_move(self, direction, map_obj, event):
        """
        Realiza movimiento continuo en la dirección dada hasta punto de decisión o final.
        """
        initial_pos = self.position
        current_pos = self.position

        # Si ya estamos en FINAL, no mover
        if map_obj.grid[current_pos[0]][current_pos[1]].has_mark(CellMark.FINAL):
            return False

        while True:
            # Calcular siguiente posición
            next_pos = self._get_next_position(current_pos, direction)
            if not self._is_valid_position(next_pos, map_obj):
                break

            next_cell = map_obj.grid[next_pos[0]][next_pos[1]]

            # Si la siguiente celda no es transitable, parar
            if not next_cell.is_passable():
                break

            # Mover a la siguiente posición
            old_pos = current_pos
            current_pos = next_pos
            self.position = current_pos
            self.movement_count += 1

            # Marcar como visitada la posición anterior (excepto inicial)
            old_cell = map_obj.grid[old_pos[0]][old_pos[1]]
            old_cell.add_mark(CellMark.VISITED)
            old_cell.remove_mark(CellMark.CURRENT)

            # Marcar nueva posición como actual y visitada
            next_cell.add_mark(CellMark.CURRENT)
            next_cell.add_mark(CellMark.VISITED)

            # Descubrir la celda
            map_obj.discover_cell(current_pos[0], current_pos[1])

            # Si es punto de decisión o final, parar
            if next_cell.has_mark(CellMark.DECISION) or next_cell.has_mark(CellMark.FINAL):
                break

        # Emitir evento de movimiento
        self.event_bus.emit(event, old_position=initial_pos,
                            new_position=self.position, direction=direction)

        return True

    def _get_next_position(self, position, direction):
        """Calcula la siguiente posición en la dirección dada."""
        row, col = position
        if direction == Direction.UP:
            return (row - 1, col)
        elif direction == Direction.RIGHT:
            return (row, col + 1)
        elif direction == Direction.DOWN:
            return (row + 1, col)
        elif direction == Direction.LEFT:
            return (row, col - 1)

    def _is_valid_position(self, position, map_obj):
        """Verifica si la posición es válida en el mapa."""
        row, col = position
        return 0 <= row < map_obj.rows and 0 <= col < map_obj.cols


class Agent1(Agent):
    """
    Agente Tipo 1: Percepción frontal limitada + acciones básicas.

    - Sensor: Solo frontal (FrontSensor)
    - Acciones disponibles: Girar izquierda, mover adelante
    - Ideal para navegación simple con percepción limitada
    """

    def __init__(self, event_bus: EventBus):
        """
        Inicializa el Agente Tipo 1.

        Args:
            event_bus: Bus de eventos para comunicación
        """
        sensor = FrontSensor()
        actions = [TurnLeft(), MoveForward()]
        super().__init__(sensor, actions, event_bus)


class Agent2(Agent):
    """
    Agente Tipo 2: Percepción frontal + giros completos.

    - Sensor: Solo frontal (FrontSensor)
    - Acciones disponibles: Girar izquierda/derecha, mover adelante
    - Mayor flexibilidad de movimiento con percepción limitada
    """

    def __init__(self, event_bus: EventBus):
        """
        Inicializa el Agente Tipo 2.

        Args:
            event_bus: Bus de eventos para comunicación
        """
        sensor = FrontSensor()
        actions = [TurnLeft(), TurnRight(), MoveForward()]
        super().__init__(sensor, actions, event_bus)


class Agent3(Agent):
    """
    Agente Tipo 3: Percepción completa + movimiento libre.

    - Sensor: Todas las direcciones (AllDirectionsSensor)
    - Acciones disponibles: Mover en las 4 direcciones cardinales
    - Máxima libertad de movimiento con percepción completa
    """

    def __init__(self, event_bus: EventBus):
        """
        Inicializa el Agente Tipo 3.

        Args:
            event_bus: Bus de eventos para comunicación
        """
        sensor = AllDirectionsSensor()
        actions = [MoveUp(), MoveDown(), MoveRight(), MoveLeft()]
        super().__init__(sensor, actions, event_bus)


class Agent4(Agent, ContinuousMover):
    """
    Agente Tipo 4: Movimiento continuo hasta puntos de decisión.

    - Sensor: Todas las direcciones (AllDirectionsSensor)
    - Acciones disponibles: Girar izquierda/derecha, mover continuo adelante
    - Se mueve continuamente en la dirección actual hasta encontrar un punto de decisión o final
    """

    def __init__(self, event_bus: EventBus):
        """
        Inicializa el Agente Tipo 4.

        Args:
            event_bus: Bus de eventos para comunicación
        """
        sensor = AllDirectionsSensor()
        actions = [TurnLeft(), TurnRight(), MoveForward()]
        super().__init__(sensor, actions, event_bus)

    def perform_action(self, action, map_obj, event):
        """
        Ejecuta una acción, con movimiento continuo para MoveForward.
        """
        if not self.can_perform_action(action, map_obj):
            return False

        if isinstance(action, MoveForward):
            return self._perform_continuous_move(self.direction, map_obj, event)
        else:
            # Para otras acciones (giros), comportamiento normal
            return super().perform_action(action, map_obj, event)


class Agent5(Agent, ContinuousMover):
    """
    Agente Tipo 5: Movimiento continuo en 4 direcciones hasta puntos de decisión.

    - Sensor: Todas las direcciones (AllDirectionsSensor)
    - Acciones disponibles: Mover continuo en las 4 direcciones cardinales
    - Se mueve continuamente en la dirección elegida hasta encontrar un punto de decisión o final
    """

    def __init__(self, event_bus: EventBus):
        """
        Inicializa el Agente Tipo 5.

        Args:
            event_bus: Bus de eventos para comunicación
        """
        sensor = AllDirectionsSensor()
        actions = [MoveUp(), MoveDown(), MoveRight(), MoveLeft()]
        super().__init__(sensor, actions, event_bus)

    def perform_action(self, action, map_obj, event):
        """
        Ejecuta una acción, con movimiento continuo para todas las direcciones.
        """
        if not self.can_perform_action(action, map_obj):
            return False

        if isinstance(action, (MoveUp, MoveDown, MoveRight, MoveLeft)):
            # Determinar dirección basada en la acción
            if isinstance(action, MoveUp):
                direction = Direction.UP
            elif isinstance(action, MoveDown):
                direction = Direction.DOWN
            elif isinstance(action, MoveRight):
                direction = Direction.RIGHT
            elif isinstance(action, MoveLeft):
                direction = Direction.LEFT
            return self._perform_continuous_move(direction, map_obj, event)
        else:
            # No hay otras acciones
            return False
