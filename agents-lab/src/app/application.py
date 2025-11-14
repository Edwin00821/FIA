import time

from src.core.cell import CellMark, TerrainType
from src.core.agent import Agent
from src.core.agent_factory import AgentFactory
from src.core.actions import TurnLeft, TurnRight, MoveForward, MoveUp, MoveDown, MoveRight, MoveLeft
from src.core.game_mode import GameMode
from src.core.search import SearchAlgorithmType

from src.utils.map_loader import MapLoader
from src.utils.game_config_loader import GameConfigLoader, GameConfigLoaderError

from src.app.config.config_manager import ConfigManager

from src.utils.coordinate_system import MapCoordinate, CoordinateSystem

from src.app.engines.pygame_graphics_engine import PygameGraphicsEngine

from src.app.events.event_bus import EventBus, AppEvent
from src.app.events.input_handler import InputHandler

from src.app.services.map_editor import MapEditor
from src.app.services.search_service import SearchService
from src.app.services.visualization_state import VisualizationState

from src.app.rendering.map_renderer import MapRenderer
from src.app.rendering.tree_console_renderer import TreeConsoleRenderer

from src.core.search.astar import AStarSearch
from src.core.heuristic import manhattan_distance
from src.core.cost_strategy import CostStrategyFactory, BeingType
from src.core.being import Being
from src.core.sensors import AllDirectionsSensor


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

        self.game_config_loader = GameConfigLoader(
            self._config_manager.app.DATA_DIRECTORY)

        self.game_mode: GameMode = GameMode.MAP

        self.map_renderer = None
        self.current_map = None

        self.current_agent: Agent = None
        self.search_service = SearchService(self.event_bus)
        self.viz_state = VisualizationState()
        self.tree_console_renderer = TreeConsoleRenderer()

    def initialize(self) -> bool:
        """Inicializa el motor de la aplicación."""
        try:
            print("\nIniciando motor de aplicación...\n")

            self._setup_event_handlers()

            # Cargar configuración del modo inicial
            try:
                self.current_game_config = self.game_config_loader.load_config(
                    self.game_mode
                )
            except GameConfigLoaderError as e:
                print(f"Error cargando configuración del juego: {e}")
                return False

            # Cargar estado del juego según configuración
            if not self._load_game_state(self.game_mode):
                return False

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
            AppEvent.SWITCH_GAME_MODE, self._on_switch_game_mode)

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

        # Handlers de búsqueda
        self.event_bus.register_handler(
            AppEvent.RUN_BFS, self._on_run_bfs)
        self.event_bus.register_handler(
            AppEvent.RUN_DFS, self._on_run_dfs)
        self.event_bus.register_handler(
            AppEvent.SEARCH_COMPLETE, self._on_search_complete)
        self.event_bus.register_handler(
            AppEvent.SEARCH_CANCEL, self._on_search_cancel)
        self.event_bus.register_handler(
            AppEvent.RUN_ASTAR, self._on_run_astar)

        # Handlers de reproducción
        self.event_bus.register_handler(
            AppEvent.PLAYBACK_START, self._on_playback_start)
        self.event_bus.register_handler(
            AppEvent.PLAYBACK_STEP, self._on_playback_step)
        self.event_bus.register_handler(
            AppEvent.PLAYBACK_STOP, self._on_playback_stop)
        self.event_bus.register_handler(
            AppEvent.TOGGLE_PLAYBACK_MODE, self._on_toggle_playback_mode)

        self.event_bus.register_handler(
            AppEvent.TOGGLE_TREE_VIEW, self._on_toggle_tree_view)

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
            # Recargar configuración del modo actual
            self.current_game_config = self.game_config_loader.load_config(
                self.game_mode
            )

            # Recargar estado del juego
            if self.current_agent:
                self.current_agent.reset()

            if self._load_game_state(self.game_mode):
                print("Aplicación recargada exitosamente")
            else:
                print("Error recargando aplicación")

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

    def _on_switch_game_mode(self) -> None:
        """Maneja el evento de cambiar modo de juego."""
        # Alternar entre MAZE y MAP
        new_mode = GameMode.MAP if self.game_mode == GameMode.MAZE else GameMode.MAZE
        self.switch_game_mode(new_mode)

    def _load_game_state(self, mode: GameMode) -> bool:
        """
        Carga el estado del juego según el modo especificado.

        Args:
            mode: Modo de juego a cargar

        Returns:
            bool: True si la carga fue exitosa
        """
        try:
            config = self.current_game_config

            # Cargar mapa
            self.current_map = self.map_loader.load_map(config.map_path)

            # Calcular tamaño de ventana
            width, height = MapRenderer.calculate_window_size(
                self.current_map, self._config_manager.display
            )

            # Inicializar el motor gráfico
            if self.graphics_engine._screen:
                self.graphics_engine.resize(width + 1, height + 1)
            else:
                self.graphics_engine.initialize(
                    width + 1, height + 1, self._config_manager.app.WINDOW_TITLE)

            # Crear el renderer
            self.map_renderer = MapRenderer(
                self.graphics_engine, self._config_manager
            )

            self.coordinate_system = CoordinateSystem(self._config_manager)

            # Marcar posiciones inicial y final
            initial_row, initial_col = config.initial_position
            goal_row, goal_col = config.goal_position

            self.current_map.grid[initial_row][initial_col].add_mark(
                CellMark.INITIAL)
            self.current_map.grid[goal_row][goal_col].add_mark(CellMark.FINAL)

            # Aplicar fog of war según modo
            if mode == GameMode.MAZE:
                self.current_map.mask_all()

                # Marcar puntos de decisión
                self.current_map.mark_decision_points()

                # Crear entidad según tipo
                # Por ahora solo soportamos agentes (entity_type = "1", "2", "3", etc.)
                self.current_agent = AgentFactory.create_agent(
                    config.entity_type, self.event_bus
                )

                # Inicializar agente en el mapa
                self.current_agent.initialize_on_map(self.current_map)
                
                print("Modo MAZE: Fog of War activado")
            else:  # MAP
                # Descubrir todo el mapa
                self.current_map.mask_all()

            return True

        except Exception as e:
            print(f"Error cargando estado del juego: {e}")
            return False

    def switch_game_mode(self, new_mode: GameMode) -> bool:
        """
        Cambia el modo de juego actual.

        Args:
            new_mode: Nuevo modo de juego

        Returns:
            bool: True si el cambio fue exitoso
        """
        if new_mode == self.game_mode:
            print(f"Ya estás en modo {new_mode.value.upper()}")
            return False

        try:
            print(
                f"\nCambiando de modo {self.game_mode.value.upper()} → {new_mode.value.upper()}...")

            # Cargar configuración del nuevo modo
            self.current_game_config = self.game_config_loader.load_config(
                new_mode)

            # Actualizar modo actual
            self.game_mode = new_mode

            # Reiniciar agente si existe
            if self.current_agent:
                self.current_agent.reset()

            # Cargar estado del nuevo modo
            if self._load_game_state(new_mode):
                print(f"Modo {new_mode.value.upper()} cargado exitosamente\n")
                return True
            else:
                print(f"Error cargando modo {new_mode.value.upper()}")
                return False

        except GameConfigLoaderError as e:
            print(f"Error cambiando modo de juego: {e}")
            return False

    def _on_run_bfs(self) -> None:
        """Maneja el evento de ejecutar BFS."""
        if not self.current_map or not self.current_game_config:
            print("No hay mapa cargado")
            return

        start_pos = self.current_game_config.initial_position
        goal_pos = self.current_game_config.goal_position

        result = self.search_service.run_search(
            SearchAlgorithmType.BFS,
            self.current_map,
            start_pos,
            goal_pos,
            visualize_realtime=False
        )

        if result.success:
            tree_output = self.tree_console_renderer.render_all_trees(result)
            print("\n" + tree_output)
        else:
            print("No se encontró camino")

    def _on_run_dfs(self) -> None:
        """Maneja el evento de ejecutar DFS."""
        if not self.current_map or not self.current_game_config:
            print("No hay mapa cargado")
            return

        start_pos = self.current_game_config.initial_position
        goal_pos = self.current_game_config.goal_position

        # Prioridad direccional por defecto
        direction_priority = ['up', 'right', 'down', 'left']

        result = self.search_service.run_search(
            SearchAlgorithmType.DFS,
            self.current_map,
            start_pos,
            goal_pos,
            visualize_realtime=False,
            direction_priority=direction_priority
        )

        if result.success:
            tree_output = self.tree_console_renderer.render_all_trees(result)
            print("\n" + tree_output)
        else:
            print("No se encontró camino")

    def _on_run_astar(self) -> None:
        """Maneja el evento de ejecutar A*."""
        if not self.current_map or not self.current_game_config:
            print("No hay mapa cargado")
            return

        start_pos = self.current_game_config.initial_position
        goal_pos = self.current_game_config.goal_position

        # Determinar el tipo de being según entity_type
        entity_type = self.current_game_config.entity_type

        # Crear being con sensor y estrategia de costos
        being = Being(AllDirectionsSensor())
        
        monkey = CostStrategyFactory.create(BeingType.MONKEY)
        octopus = CostStrategyFactory.create(BeingType.OCTOPUS)
        human = CostStrategyFactory.create(BeingType.HUMAN)
        
        # Terrenos a probar
        terrains = [
            TerrainType.LAND,
            TerrainType.WATER,
            TerrainType.SAND,
            TerrainType.FOREST,
            TerrainType.MOUNTAIN,
        ]
        
        print(f"{'Terreno':<12} | {'Monkey':<8} | {'Octopus':<8} | {'Human':<8}")
        print("-" * 50)
        
        for terrain in terrains:
            monkey_cost = monkey.get_cost(terrain)
            octopus_cost = octopus.get_cost(terrain)
            human_cost = human.get_cost(terrain)
            
            # Formatear infinito como "N/A"
            m_str = "N/A" if monkey_cost == float('inf') else str(int(monkey_cost))
            o_str = "N/A" if octopus_cost == float('inf') else str(int(octopus_cost))
            h_str = "N/A" if human_cost == float('inf') else str(int(human_cost))
            
            print(f"{terrain.name:<12} | {m_str:<8} | {o_str:<8} | {h_str:<8}")

        # Establecer estrategia de costos si es un tipo conocido
        try:
            cost_strategy = CostStrategyFactory.from_string(entity_type)
            being.set_cost_strategy(cost_strategy)
        except ValueError:
            print(
                f"Tipo de entidad '{entity_type}' no tiene costos definidos, usando costos por defecto")
            cost_strategy = None

        astar = AStarSearch(
            heuristic_func=manhattan_distance,
            cost_strategy=cost_strategy,
            being=being,
            use_fog_of_war=True
        )
        # Ejecutar A* con fog of war
        result = astar.search(
            self.current_map, start_pos, goal_pos)

        if result.success:
            tree_output = self.tree_console_renderer.render_all_trees(result)
            print("\n" + tree_output)
        else:
            print("No se encontró camino")

    def _on_search_complete(self, result, algorithm_type) -> None:
        """Maneja el evento de búsqueda completada."""
        print(
            f"\n=================== Búsqueda {algorithm_type.value.upper()} completada ===================")
        self.viz_state.update_from_result(result)

    def _on_search_cancel(self) -> None:
        """Maneja el evento de cancelar búsqueda."""
        print("\nBúsqueda cancelada")
        self.search_service.cancel_search()
        self.viz_state.clear()

    def _on_playback_start(self, mode) -> None:
        """Maneja el evento de iniciar reproducción."""
        print(f"\n=== Reproducción iniciada (modo: {mode}) ===")
        self.viz_state.is_playing = True
        self.viz_state.playback_mode = mode

    def _on_playback_step(self, step) -> None:
        """Maneja el evento de paso de reproducción."""
        self.viz_state.update_from_step(step)

    def _on_playback_stop(self) -> None:
        """Maneja el evento de detener reproducción."""
        print("\n=== Reproducción detenida ===")
        self.viz_state.is_playing = False

    def _on_toggle_playback_mode(self) -> None:
        """Maneja el evento de alternar modo de reproducción."""
        new_mode = self.search_service.toggle_playback_mode()
        self.viz_state.playback_mode = new_mode

    def _on_toggle_tree_view(self) -> None:
        """Maneja el evento de alternar vista del árbol."""
        self.viz_state.toggle_tree_view()
        state = "activada" if self.viz_state.show_tree else "desactivada"
        print(f"Vista del árbol: {state}")

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
        print("  M - Cambiar modo de juego (MAZE - MAP)")
        print("  Click - Inspeccionar celda (o editar en modo edición)")
        print("  0-9 - Cambiar tipo de terreno (en modo edición)")

        print("  Controles de Agente:")
        print("    J - Girar izquierda")
        print("    L - Girar derecha")
        print("    SPACE - Mover enfrente")
        print("    WASD - Mover en direcciones (Arriba/Abajo/Derecha/Izquierda)")

        print("  Controles de Búsqueda:")
        print("    B - Ejecutar BFS")
        print("    F - Ejecutar DFS")
        print("    H - Ejecutar A*")
        print("    P - Iniciar reproducción")
        print("    T - Alternar modo reproducción (paso a paso / decisión)")
        print("    G - Alternar vista del árbol de búsqueda")
        print("    C - Cancelar búsqueda/reproducción")
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

        # Actualizar reproducción si está activa
        if self.search_service.is_playing and not self.search_service.is_paused:
            # Verificar si es momento de avanzar al siguiente paso
            if not hasattr(self, '_last_playback_time'):
                self._last_playback_time = 0

            self._last_playback_time += delta_time

            if self._last_playback_time >= self.search_service.playback_speed:
                self._last_playback_time = 0
                self.search_service.next_playback_step()

    def _render(self) -> None:
        """Renderiza un frame."""
        if self.current_map and self.map_renderer:
            self.map_renderer.render_map(self.current_map, self.viz_state)

        if self.current_agent:
            self.current_agent.perceive(self.current_map)

    def _cleanup(self) -> None:
        """Limpia recursos de la aplicación."""
        print("\nLimpiando recursos...")
        self.graphics_engine.cleanup()
        print("Aplicación terminada")
