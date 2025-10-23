from enum import Enum
from typing import Dict, Callable, Any


class AppEvent(Enum):
    """Eventos de la aplicación."""
    EXIT = "exit"
    RELOAD = "reload"

    CELL_INSPECTED = "cell_inspected"

    CELL_CLICKED = "cell_clicked"

    EDIT_MODE_TOGGLE = "edit_mode_toggle"
    EDIT_MODE_EXIT = "edit_mode_exit"
    CELL_EDIT_START = "cell_edit_start"
    TERRAIN_CHANGE = "terrain_change"
    EDIT_CANCEL = "edit_cancel"

    AGENT_MOVED = "agent_moved"

    AGENT_TURN_LEFT = "agent_turn_left"
    AGENT_TURN_RIGHT = "agent_turn_right"

    AGENT_MOVE_FORWARD = "agent_move_forward"
    AGENT_MOVE_UP = "agent_move_up"
    AGENT_MOVE_DOWN = "agent_move_down"
    AGENT_MOVE_RIGHT = "agent_move_right"
    AGENT_MOVE_LEFT = "agent_move_left"

    SWITCH_GAME_MODE = "switch_game_mode"

    SEARCH_START = "search_start"
    SEARCH_STEP = "search_step"
    SEARCH_COMPLETE = "search_complete"
    SEARCH_CANCEL = "search_cancel"

    PLAYBACK_START = "playback_start"
    PLAYBACK_STEP = "playback_step"
    PLAYBACK_COMPLETE = "playback_complete"
    PLAYBACK_PAUSE = "playback_pause"
    PLAYBACK_RESUME = "playback_resume"
    PLAYBACK_STOP = "playback_stop"

    RUN_BFS = "run_bfs"
    RUN_DFS = "run_dfs"
    TOGGLE_PLAYBACK_MODE = "toggle_playback_mode"


class EventBus:
    """
    Bus de eventos centralizado para la aplicación.

    Permite registrar handlers para eventos específicos y emitirlos
    de manera desacoplada entre componentes.
    """

    def __init__(self):
        """Inicializa el bus de eventos."""
        self._handlers: Dict[AppEvent, Callable[..., Any]] = {}

    def register_handler(self, event: AppEvent, handler: Callable[..., Any]) -> None:
        """
        Registra un handler para un evento específico.

        Args:
            event: Tipo de evento
            handler: Función a ejecutar cuando ocurra el evento

        Raises:
            ValueError: Si ya existe un handler para el evento
        """
        if event in self._handlers:
            raise ValueError(
                f"Ya existe un handler registrado para el evento {event.value}")

        self._handlers[event] = handler

    def unregister_handler(self, event: AppEvent) -> None:
        """
        Desregistra un handler para un evento específico.

        Args:
            event: Tipo de evento a desregistrar
        """
        self._handlers.pop(event, None)

    def emit(self, event: AppEvent, **kwargs) -> bool:
        """
        Emite un evento ejecutando su handler si existe.

        Args:
            event: Tipo de evento a emitir
            **kwargs: Argumentos adicionales para el handler

        Returns:
            True si se ejecutó el handler, False si no existe
        """
        handler = self._handlers.get(event)
        if handler:
            try:
                handler(**kwargs)
                return True
            except Exception as e:
                print(f"Error ejecutando handler para {event.value}: {e}")
                return False
        return False

    def has_handler(self, event: AppEvent) -> bool:
        """
        Verifica si existe un handler para el evento.

        Args:
            event: Tipo de evento a verificar

        Returns:
            True si existe handler, False en caso contrario
        """
        return event in self._handlers

    def get_registered_events(self) -> list[AppEvent]:
        """
        Obtiene la lista de eventos registrados.

        Returns:
            Lista de eventos que tienen handlers registrados
        """
        return list(self._handlers.keys())
