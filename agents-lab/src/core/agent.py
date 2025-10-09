from typing import List, Dict, Tuple

from .being import Being
from .sensors import Sensor
from .actions import Action
from .map import Map
from .cell import CellMark

from ..app.events.event_bus import EventBus, AppEvent


class Agent(Being):
    """
    Clase base para agentes con capacidades de percepción y acción.

    Los agentes pueden percibir su entorno, realizar acciones y mantener estado.
    """

    def __init__(self, sensor: Sensor, available_actions: List[Action], event_bus: EventBus):
        """
        Inicializa un nuevo agente.

        Args:
            sensor: Sensor para percepción del entorno
            available_actions: Lista de acciones disponibles para el agente
            event_bus: Bus de eventos para comunicación
        """
        super().__init__(sensor)
        self.available_actions = available_actions
        self.event_bus = event_bus

        # Estado adicional del agente
        self.movement_count: int = 0

    def set_available_actions(self, actions: List[Action]) -> None:
        """
        Cambia las acciones disponibles para el agente.

        Args:
            actions: Nueva lista de acciones disponibles
        """
        self.available_actions = actions

    def initialize_on_map(self, map_obj: Map) -> bool:
        """
        Inicializa el agente en el punto inicial ('I') del mapa.

        Args:
            map_obj: El mapa donde colocar al agente

        Returns:
            True si se encontró y configuró el punto inicial
        """
        initial_positions = map_obj.get_positions_with_mark(CellMark.INITIAL)
        if initial_positions:
            row, col = initial_positions[0]  # Asumiendo un solo punto inicial
            self.position = (row, col)
            # Marcar la posición inicial como visitada
            map_obj.grid[row][col].add_mark(CellMark.CURRENT)
            # Descubrir la celda inicial
            map_obj.discover_cell(row, col)
            return True
        return False

    def can_perform_action(self, action: Action, map_obj: Map) -> bool:
        """
        Verifica si el agente puede realizar una acción específica.

        Args:
            action: La acción a verificar
            map_obj: El mapa para validación

        Returns:
            True si la acción es válida y está disponible
        """

        if type(action) not in [type(a) for a in self.available_actions]:
            return False
        if self.position is None:
            return False
        return action.is_valid(self.position, self.direction, map_obj)

    def perform_action(self, action: Action, map_obj: Map, event: AppEvent) -> bool:
        """
        Ejecuta una acción si es posible.

        Args:
            action: La acción a ejecutar
            map_obj: El mapa donde se ejecuta la acción

        Returns:
            True si la acción se ejecutó exitosamente
        """
        if not self.can_perform_action(action, map_obj):
            return False

        # Ejecutar la acción
        new_position, new_direction = action.execute(
            self.position, self.direction)

        # Actualizar estado
        old_position = self.position
        self.position = new_position
        self.direction = new_direction

        # Si la posición cambió, es un movimiento
        if old_position != new_position:
            self.movement_count += 1
            self._handle_movement(map_obj, old_position, new_position)

        # Emitir evento de movimiento
        self.event_bus.emit(event, old_position=old_position,
                            new_position=self.position, direction=self.direction)

        return True

    def _handle_movement(self, map_obj: Map, old_position: Tuple[int, int], new_position: Tuple[int, int]) -> None:
        """
        Maneja la lógica de movimiento: marcar celdas como visitadas y actuales.

        Args:
            map_obj: El mapa
            old_position: Posición anterior
            new_position: Nueva posición
        """
        # Marcar la posición anterior como visitada (si no es inicial)
        old_cell = map_obj.grid[old_position[0]][old_position[1]]

        old_cell.add_mark(CellMark.VISITED)
        old_cell.remove_mark(CellMark.CURRENT)

        # Marcar la nueva posición como actual y visitada
        new_cell = map_obj.grid[new_position[0]][new_position[1]]
        new_cell.add_mark(CellMark.CURRENT)
        new_cell.add_mark(CellMark.VISITED)

        # Descubrir la nueva celda
        map_obj.discover_cell(new_position[0], new_position[1])

    def get_state(self) -> Dict:
        """
        Obtiene el estado actual del agente.

        Returns:
            Diccionario con información del estado
        """
        state = super().get_state()
        state['movement_count'] = self.movement_count
        return state

    def reset(self) -> None:
        """Reinicia el estado del agente."""
        super().reset()
        self.movement_count = 0

    def __str__(self) -> str:
        """Representación string del agente."""
        pos_str = f"({self.position[0]}, {self.position[1]})" if self.position else "None"
        return f"Agent(position={pos_str}, direction={self.direction.value}, movements={self.movement_count})"

    def __repr__(self) -> str:
        """Representación detallada para debug."""
        return self.__str__()
