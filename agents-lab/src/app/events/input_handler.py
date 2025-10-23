import pygame

from typing import Dict, Tuple

from .event_bus import EventBus, AppEvent


class InputHandler:
    """
    Manejador de entrada que convierte eventos de pygame a eventos de aplicación.

    Se encarga de capturar eventos del sistema (teclado, mouse, etc.) y
    convertirlos a eventos de aplicación que se emiten a través del EventBus.
    """

    def __init__(self, event_bus: EventBus):
        """
        Inicializa el manejador de entrada.

        Args:
            event_bus: Bus de eventos donde emitir los eventos de aplicación
        """
        self.event_bus = event_bus

        # Mapeo de teclas a eventos de aplicación
        self._key_mappings: Dict[int, AppEvent] = {
            pygame.K_ESCAPE: AppEvent.EXIT,
            pygame.K_r: AppEvent.RELOAD,
            pygame.K_e: AppEvent.EDIT_MODE_TOGGLE,
            pygame.K_v: AppEvent.EDIT_MODE_EXIT,
            pygame.K_m: AppEvent.SWITCH_GAME_MODE,

            # Controles de agente
            pygame.K_j: AppEvent.AGENT_TURN_LEFT,
            pygame.K_l: AppEvent.AGENT_TURN_RIGHT,

            pygame.K_SPACE: AppEvent.AGENT_MOVE_FORWARD,

            pygame.K_w: AppEvent.AGENT_MOVE_UP,
            pygame.K_s: AppEvent.AGENT_MOVE_DOWN,
            pygame.K_d: AppEvent.AGENT_MOVE_RIGHT,
            pygame.K_a: AppEvent.AGENT_MOVE_LEFT,

            pygame.K_b: AppEvent.RUN_BFS,
            pygame.K_f: AppEvent.RUN_DFS,
            pygame.K_p: AppEvent.PLAYBACK_START,
            pygame.K_t: AppEvent.TOGGLE_PLAYBACK_MODE,
            pygame.K_c: AppEvent.SEARCH_CANCEL,
        }

    def process_events(self) -> None:
        """
        Procesa todos los eventos pendientes de pygame.

        Convierte eventos de pygame a eventos de aplicación y los emite
        a través del EventBus.
        """
        for event in pygame.event.get():
            self._handle_pygame_event(event)

    def _handle_pygame_event(self, event: pygame.event.Event) -> None:
        """
        Maneja un evento específico de pygame.

        Args:
            event: Evento de pygame a procesar
        """
        if event.type == pygame.QUIT:
            self.event_bus.emit(AppEvent.EXIT)

        elif event.type == pygame.KEYDOWN:
            self._handle_key_down(event.key)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event.pos, event.button)

    def _handle_mouse_click(self, position: Tuple[int, int], button: int) -> None:
        """
        Maneja eventos de click del mouse.

        Args:
            position: Posición (x, y) del click
            button: Botón del mouse presionado
        """
        if button == 1:  # Click izquierdo
            self.event_bus.emit(AppEvent.CELL_CLICKED, position=position)

    def _handle_key_down(self, key: int) -> None:
        """
        Maneja eventos de teclas presionadas.

        Args:
            key: Código de la tecla presionada
        """
        # Verificar si es una tecla numérica
        self._handle_number_key(key)

        # Verificar mapeos de aplicación
        app_event = self._key_mappings.get(key)
        if app_event:
            self.event_bus.emit(app_event)

    def _handle_number_key(self, key: int) -> None:
        """
        Maneja eventos de teclas numéricas para cambio de terreno.

        Args:
            key: Código de la tecla presionada
        """
        # Mapeo de teclas numéricas a valores
        number_keys = {
            pygame.K_0: 0, pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
            pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7,
            pygame.K_8: 8, pygame.K_9: 9
        }

        if key in number_keys:
            terrain_value = number_keys[key]
            self.event_bus.emit(AppEvent.TERRAIN_CHANGE,
                                terrain_value=terrain_value)

    def add_key_mapping(self, key: int, event: AppEvent) -> None:
        """
        Agrega un mapeo de tecla a evento.

        Args:
            key: Código de tecla de pygame
            event: Evento de aplicación a mapear
        """
        self._key_mappings[key] = event

    def remove_key_mapping(self, key: int) -> None:
        """
        Remueve un mapeo de tecla.

        Args:
            key: Código de tecla a remover
        """
        self._key_mappings.pop(key, None)
