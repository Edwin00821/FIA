import time

from src.core.cell import CellMark
from src.core.agent import Agent
from src.core.agent_factory import AgentFactory
from src.core.actions import TurnLeft, TurnRight, MoveForward, MoveUp, MoveDown, MoveRight, MoveLeft


from src.utils.map_loader import MapLoader

from src.app.config.config_manager import ConfigManager

from src.utils.coordinate_system import MapCoordinate, CoordinateSystem

from src.app.engines.pygame_graphics_engine import PygameGraphicsEngine

from src.app.events.event_bus import EventBus, AppEvent
from src.app.events.input_handler import InputHandler

from src.app.services.map_editor import MapEditor

from src.app.rendering.map_renderer import MapRenderer


class Application:
    """Motor principal de la aplicación que coordina todos los componentes."""

    def __init__(self):
        self._running = False
        self._last_frame_time = 0.0
        self.coordinate_system = None

        # Resolver dependencias principales
        self._config_manager = ConfigManager()

        self.graphics_engine = PygameGraphicsEngine()

        self.event_bus = EventBus()
        self.input_handler = InputHandler(self.event_bus)

        self.map_editor = MapEditor()

        self.map_loader = MapLoader()

        self.map_renderer = None
        self.current_map = None

        self.current_agent: Agent = None

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

            self.coordinate_system = CoordinateSystem(self._config_manager)

            self.current_map.grid[9][0].add_mark(CellMark.INITIAL)
            self.current_map.grid[1][4].add_mark(CellMark.FINAL)
            self.current_map.mark_decision_points()

            self.current_agent = AgentFactory.create_agent(3, self.event_bus)

            self.current_agent.initialize_on_map(self.current_map)

            print("\nMotor de aplicación inicializado correctamente\n")
            return True

        except Exception as e:
            print(f"Error inicializando motor de aplicación: {e}")
            return False

    def _setup_event_handlers(self) -> None:
        """Configura los handlers del bus de eventos."""
        self.event_bus.register_handler(AppEvent.EXIT, self._on_exit)
        self.event_bus.register_handler(AppEvent.RELOAD, self._on_reload)
        self.event_bus.register_handler(
            AppEvent.CELL_INSPECTED, self._on_cell_inspected)

        self.event_bus.register_handler(
            AppEvent.CELL_CLICKED, self._on_cell_clicked)

        self.event_bus.register_handler(
            AppEvent.EDIT_MODE_TOGGLE, self._on_edit_mode_toggle)
        self.event_bus.register_handler(
            AppEvent.EDIT_MODE_EXIT, self._on_edit_mode_exit)
        self.event_bus.register_handler(
            AppEvent.CELL_EDIT_START, self._on_cell_edit_start)
        self.event_bus.register_handler(
            AppEvent.TERRAIN_CHANGE, self._on_terrain_change)

        self.event_bus.register_handler(
            AppEvent.AGENT_TURN_LEFT, self._on_agent_turn_left)
        self.event_bus.register_handler(
            AppEvent.AGENT_TURN_RIGHT, self._on_agent_turn_right)
        
        self.event_bus.register_handler(
            AppEvent.AGENT_MOVED, self._on_agent_moved)
        
        self.event_bus.register_handler(
            AppEvent.AGENT_MOVE_FORWARD, self._on_agent_move_forward)
        
        self.event_bus.register_handler(
            AppEvent.AGENT_MOVE_UP, self._on_agent_move_up)
        self.event_bus.register_handler(
            AppEvent.AGENT_MOVE_DOWN, self._on_agent_move_down)
        self.event_bus.register_handler(
            AppEvent.AGENT_MOVE_RIGHT, self._on_agent_move_right)
        self.event_bus.register_handler(
            AppEvent.AGENT_MOVE_LEFT, self._on_agent_move_left)

    def _on_cell_clicked(self, position) -> None:
        """Maneja el evento de click en una celda."""
        if not self.current_map or not self.coordinate_system:
            return

        x, y = position
        coordinate = self.coordinate_system.screen_to_map(
            x, y, self.current_map)

        if coordinate:
            if self.map_editor.is_edit_mode:
                # En modo edición, iniciar edición de celda
                self.event_bus.emit(AppEvent.CELL_EDIT_START,
                                    coordinate=coordinate)
            else:
                # En modo inspección, mostrar información
                self.event_bus.emit(AppEvent.CELL_INSPECTED,
                                    coordinate=coordinate)
        else:
            print("Click fuera del área del mapa")

    def _on_cell_inspected(self, coordinate: MapCoordinate) -> None:
        """Maneja el evento de inspección de celda."""
        cell = self.current_map.grid[coordinate.row][coordinate.col]

        print(f"Celda {coordinate.human_format}: {cell.get_display_info()}")

    def _on_edit_mode_toggle(self) -> None:
        """Maneja el evento de alternar modo edición."""
        self.map_editor.toggle_edit_mode()

    def _on_edit_mode_exit(self) -> None:
        """Maneja el evento de salir del modo edición."""
        self.map_editor.exit_edit_mode()

    def _on_cell_edit_start(self, coordinate) -> None:
        """Maneja el evento de iniciar edición de celda."""
        if not self.current_map:
            return

        success = self.map_editor.start_cell_edit(coordinate, self.current_map)
        if not success:
            print("No se puede editar la celda en este momento")

    def _on_terrain_change(self, terrain_value) -> None:
        """Maneja el evento de cambio de tipo de terreno."""
        if not self.current_map:
            return

        success = self.map_editor.apply_terrain_change(
            terrain_value, self.current_map)
        if not success and self.map_editor.has_pending_edit:
            print("No se pudo aplicar el cambio de terreno")

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

            self.current_map.grid[9][0].add_mark(CellMark.INITIAL)
            self.current_map.grid[1][4].add_mark(CellMark.FINAL)
            self.current_map.mark_decision_points()

            # Reinicializar agente en el nuevo mapa
            if self.current_agent:
                self.current_agent.reset()
                self.current_agent.initialize_on_map(self.current_map)

            print("Aplicación recargada exitosamente")
        except Exception as e:
            print(f"Error recargando aplicación: {e}")

    def _on_agent_moved(self, old_position, new_position, direction) -> None:
        """Maneja el evento de movimiento del agente."""
        if not self.current_map:
            return

        old_terrain = self.current_map.grid[old_position[0]
                                            ][old_position[1]].terrain.name.lower()
        new_terrain = self.current_map.grid[new_position[0]
                                            ][new_position[1]].terrain.name.lower()

        print(
            f"El agente se movió de ({old_position[0]}, {old_position[1]}, {old_terrain}) a ({new_position[0]}, {new_position[1]}, {new_terrain})")
        print(
            f"Total de movimientos realizados: {self.current_agent.movement_count}")

    def _on_agent_turn_left(self) -> None:
        """Maneja el evento de giro a la izquierda del agente."""
        if self.current_agent and self.current_map:
            action = TurnLeft()
            if self.current_agent.perform_action(action, self.current_map, AppEvent.AGENT_MOVED):
              print("_on_agent_turn_left\n")

    def _on_agent_turn_right(self) -> None:
        """Maneja el evento de giro a la derecha del agente."""
        if self.current_agent and self.current_map:
            action = TurnRight()
            if self.current_agent.perform_action(action, self.current_map, AppEvent.AGENT_MOVED):
              print("_on_agent_turn_right\n")

    def _on_agent_move_forward(self) -> None:
        """Maneja el evento de movimiento hacia adelante del agente."""
        if self.current_agent and self.current_map:
            action = MoveForward()
            if self.current_agent.perform_action(action, self.current_map, AppEvent.AGENT_MOVED):
              print("")

    def _on_agent_move_up(self) -> None:
        """Maneja el evento de movimiento hacia arriba del agente."""
        if self.current_agent and self.current_map:
            action = MoveUp()
            if self.current_agent.perform_action(action, self.current_map, AppEvent.AGENT_MOVED):
              print("_on_agent_move_up\n")

    def _on_agent_move_down(self) -> None:
        """Maneja el evento de movimiento hacia abajo del agente."""
        if self.current_agent and self.current_map:
            action = MoveDown()
            if self.current_agent.perform_action(action, self.current_map, AppEvent.AGENT_MOVED):
              print("_on_agent_move_down\n")

    def _on_agent_move_right(self) -> None:
        """Maneja el evento de movimiento hacia la derecha este del agente."""
        if self.current_agent and self.current_map:
            action = MoveRight()
            if self.current_agent.perform_action(action, self.current_map, AppEvent.AGENT_MOVED):
              print("_on_agent_move_right\n")

    def _on_agent_move_left(self) -> None:
        """Maneja el evento de movimiento hacia la izquierda del agente."""
        if self.current_agent and self.current_map:
            action = MoveLeft()
            if self.current_agent.perform_action(action, self.current_map, AppEvent.AGENT_MOVED):
              print("_on_agent_move_left\n")

    def run(self) -> None:
        """Ejecuta el ciclo principal de la aplicación."""
        if not self.initialize():
            return

        self._running = True
        self._last_frame_time = time.time()

        print("Controles:")
        print("  ESC - Salir")
        print("  R - Recargar aplicación")
        print("  E - Alternar modo edición")
        print("  V - Salir del modo edición")
        print("  Click - Inspeccionar celda (o editar en modo edición)")
        print("  0-9 - Cambiar tipo de terreno (en modo edición)")
        
        print("  Controles de Agente:")
        print("    J - Girar izquierda")
        print("    L - Girar derecha")
        print("    ESPACE - Mover enfrente")
        print("    WSAD - Mover en direcciones (Arriba/Abajo/Derecha/Izquierda)")
        print()

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

        if self.current_agent:
            self.current_agent.perceive(self.current_map)

    def _cleanup(self) -> None:
        """Limpia recursos de la aplicación."""
        print("\nLimpiando recursos...")
        self.graphics_engine.cleanup()
        print("Aplicación terminada")
