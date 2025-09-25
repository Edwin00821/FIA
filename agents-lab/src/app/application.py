import time

from src.utils.map_loader import MapLoader

from src.app.config.config_manager import ConfigManager

from src.app.engines.pygame_graphics_engine import PygameGraphicsEngine

from src.app.events.event_bus import EventBus, AppEvent
from src.app.events.input_handler import InputHandler

from src.app.rendering.map_renderer import MapRenderer


class Application:
    """Motor principal de la aplicación que coordina todos los componentes."""

    def __init__(self):
        self._running = False
        self._last_frame_time = 0.0

        # Resolver dependencias principales
        self._config_manager = ConfigManager()

        self.graphics_engine = PygameGraphicsEngine()

        self.event_bus = EventBus()
        self.input_handler = InputHandler(self.event_bus)

        self.map_loader = MapLoader()

        self.map_renderer = None
        self.current_map = None

    def initialize(self) -> bool:
        """Inicializa el motor de la aplicación."""
        try:
            print("\nIniciando motor de aplicación...\n")

            self._setup_event_handlers()

            # Cargar mapa por defecto
            map_path = self._config_manager.app.DEFAULT_MAP_PATH
            self.current_map = self.map_loader.load_map(map_path)

            # Calcular tamaño de ventana e inicializar renderizado
            width, height = MapRenderer.calculate_window_size(
                self.current_map, self._config_manager.display
            )

            # Inicializar el motor gráfico
            self.graphics_engine.initialize(
                width + 1, height + 1, self._config_manager.app.WINDOW_TITLE)

            # Crear el renderer
            self.map_renderer = MapRenderer(
                self.graphics_engine, self._config_manager)

            print("\nMotor de aplicación inicializado correctamente\n")
            return True

        except Exception as e:
            print(f"Error inicializando motor de aplicación: {e}")
            return False

    def _setup_event_handlers(self) -> None:
        """Configura los handlers del bus de eventos."""
        self.event_bus.register_handler(AppEvent.EXIT, self._on_exit)
        self.event_bus.register_handler(AppEvent.RELOAD, self._on_reload)

    def _on_exit(self) -> None:
        """Maneja el evento de salir de la aplicación."""
        print("\nSaliendo de la aplicación...")
        self._running = False

    def _on_reload(self) -> None:
        """Maneja el evento de recargar la aplicación."""
        print("\nRecargando aplicación...")
        try:
            # Recargar el mapa
            map_path = self._config_manager.app.DEFAULT_MAP_PATH
            self.current_map = self.map_loader.load_map(map_path)

            # Recrear el renderer
            self.map_renderer = MapRenderer(
                self.graphics_engine, self._config_manager)

            print("Aplicación recargada exitosamente")
        except Exception as e:
            print(f"Error recargando aplicación: {e}")

    def run(self) -> None:
        """Ejecuta el ciclo principal de la aplicación."""
        if not self.initialize():
            return

        self._running = True
        self._last_frame_time = time.time()

        print("Iniciado ciclo principal ...")
        print("Controles:")
        print("  ESC - Salir")
        print("  R - Recargar applicación")
        print("  E - Modo edición")
        print("  V - Salir del modo edición")
        print("  Click - Inspeccionar celda")

        try:
            while self._running:
                current_time = time.time()
                delta_time = current_time - self._last_frame_time

                self._update(delta_time)
                self._render()

                # Control de FPS
                target_fps = self._config_manager.display.FPS
                frame_time = 1.0 / target_fps
                elapsed = time.time() - current_time

                if elapsed < frame_time:
                    time.sleep(frame_time - elapsed)

                self._last_frame_time = current_time

        except KeyboardInterrupt:
            print("\n\nAplicación interrumpida por el usuario.")
        except Exception as e:
            print(f"\nError en ciclo principal: {e}")
        finally:
            self._cleanup()

    def _update(self, delta_time: float) -> None:
        """Actualiza la lógica de la aplicación."""
        self.input_handler.process_events()

    def _render(self) -> None:
        """Renderiza un frame."""
        if self.current_map and self.map_renderer:
            self.map_renderer.render_map(self.current_map)

    def _cleanup(self) -> None:
        """Limpia recursos de la aplicación."""
        print("\nLimpiando recursos...")
        self.graphics_engine.cleanup()
        print("Aplicación terminada")
