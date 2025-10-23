from typing import Optional, Callable
import time

from src.core.map import Map
from src.core.search import (
    SearchController,
    SearchAlgorithmType,
    SearchResult,
    SearchStep
)
from src.app.events.event_bus import EventBus, AppEvent


class SearchService:
    """
    Servicio para gestionar la ejecución de algoritmos de búsqueda.

    Maneja la ejecución de búsquedas, reproducción de pasos y
    comunicación con la aplicación a través del event bus.
    """

    def __init__(self, event_bus: EventBus):
        """
        Inicializa el servicio de búsqueda.

        Args:
            event_bus: Bus de eventos para comunicación
        """
        self.event_bus = event_bus
        self.controller = SearchController()

        # Estado de reproducción
        self.is_playing = False
        self.is_paused = False
        self.current_step_index = 0
        self.playback_mode = "step"  # "step" o "decision"
        self.playback_speed = 0.5  # segundos entre pasos

    def run_search(
        self,
        algorithm_type: SearchAlgorithmType,
        map_obj: Map,
        start_pos: tuple,
        goal_pos: tuple,
        visualize_realtime: bool = False,
        **kwargs
    ) -> SearchResult:
        """
        Ejecuta un algoritmo de búsqueda.

        Args:
            algorithm_type: Tipo de algoritmo (BFS o DFS)
            map_obj: Mapa donde buscar
            start_pos: Posición inicial
            goal_pos: Posición objetivo
            visualize_realtime: Si se debe visualizar en tiempo real
            **kwargs: Argumentos adicionales para el algoritmo

        Returns:
            SearchResult con el resultado de la búsqueda
        """
        # Emitir evento de inicio
        self.event_bus.emit(AppEvent.SEARCH_START,
                            algorithm_type=algorithm_type)

        # Ejecutar búsqueda
        result = self.controller.execute_search(
            algorithm_type,
            map_obj,
            start_pos,
            goal_pos,
            **kwargs
        )

        # Si se pide visualización en tiempo real, reproducir pasos
        if visualize_realtime:
            self._visualize_search_realtime(result)

        # Emitir evento de finalización
        self.event_bus.emit(
            AppEvent.SEARCH_COMPLETE,
            result=result,
            algorithm_type=algorithm_type
        )

        return result

    def _visualize_search_realtime(self, result: SearchResult) -> None:
        """
        Visualiza la búsqueda en tiempo real emitiendo eventos de paso.

        Args:
            result: Resultado de la búsqueda con pasos
        """
        for step in result.steps:
            self.event_bus.emit(AppEvent.SEARCH_STEP, step=step)
            time.sleep(self.playback_speed)

    def start_playback(self, mode: str = None) -> bool:
        """
        Inicia la reproducción de la última búsqueda.

        Args:
            mode: Modo de reproducción ("step" o "decision")

        Returns:
            True si se inició la reproducción
        """
        if not self.controller.has_result():
            print("No hay resultado de búsqueda para reproducir")
            return False

        if mode:
            self.playback_mode = mode

        self.is_playing = True
        self.is_paused = False
        self.current_step_index = 0

        self.event_bus.emit(
            AppEvent.PLAYBACK_START,
            mode=self.playback_mode
        )

        return True

    def get_playback_steps(self) -> list:
        """
        Obtiene los pasos a reproducir según el modo actual.

        Returns:
            Lista de pasos a reproducir
        """
        result = self.controller.get_last_result()
        if not result:
            return []

        if self.playback_mode == "decision":
            return result.get_decision_steps()
        else:
            return result.steps

    def next_playback_step(self) -> Optional[SearchStep]:
        """
        Avanza al siguiente paso de reproducción.

        Returns:
            SearchStep siguiente, o None si terminó
        """
        if not self.is_playing or self.is_paused:
            return None

        steps = self.get_playback_steps()

        if self.current_step_index >= len(steps):
            self.stop_playback()
            self.event_bus.emit(AppEvent.PLAYBACK_COMPLETE)
            return None

        step = steps[self.current_step_index]
        self.current_step_index += 1

        self.event_bus.emit(AppEvent.PLAYBACK_STEP, step=step)

        return step

    def pause_playback(self) -> None:
        """Pausa la reproducción."""
        if self.is_playing:
            self.is_paused = True
            self.event_bus.emit(AppEvent.PLAYBACK_PAUSE)

    def resume_playback(self) -> None:
        """Reanuda la reproducción."""
        if self.is_playing and self.is_paused:
            self.is_paused = False
            self.event_bus.emit(AppEvent.PLAYBACK_RESUME)

    def stop_playback(self) -> None:
        """Detiene la reproducción."""
        self.is_playing = False
        self.is_paused = False
        self.current_step_index = 0
        self.event_bus.emit(AppEvent.PLAYBACK_STOP)

    def toggle_playback_mode(self) -> str:
        """
        Alterna entre modos de reproducción.

        Returns:
            Nuevo modo de reproducción
        """
        self.playback_mode = "decision" if self.playback_mode == "step" else "step"
        print(f"Modo de reproducción: {self.playback_mode}")
        return self.playback_mode

    def set_playback_speed(self, speed: float) -> None:
        """
        Establece la velocidad de reproducción.

        Args:
            speed: Segundos entre pasos
        """
        self.playback_speed = max(0.1, min(5.0, speed))

    def cancel_search(self) -> None:
        """Cancela la búsqueda actual."""
        if self.controller.is_searching:
            self.event_bus.emit(AppEvent.SEARCH_CANCEL)
        self.stop_playback()

    def get_current_result(self) -> Optional[SearchResult]:
        """
        Obtiene el resultado actual de búsqueda.

        Returns:
            SearchResult o None
        """
        return self.controller.get_last_result()

    def clear(self) -> None:
        """Limpia el estado del servicio."""
        self.controller.clear_result()
        self.stop_playback()
