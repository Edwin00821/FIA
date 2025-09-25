from typing import Optional, List
from enum import Enum

from src.core.map import Map
from src.core.cell import TerrainType

from src.utils.coordinate_system import MapCoordinate

from .edit_command import EditCellCommand, ICommand


class EditorMode(Enum):
    """Estados del editor de mapas."""
    INSPECT = "inspect"  # Modo inspección (default)
    EDIT = "edit"       # Modo edición


class MapEditor:
    """
    Servicio para la edición de mapas.

    Maneja la lógica de modificación de celdas usando el patrón Command
    y mantiene el estado del modo de edición.
    """

    def __init__(self):
        """Inicializa el editor de mapas."""
        self._mode = EditorMode.INSPECT
        self._command_history: List[ICommand] = []
        self._current_command_index = -1
        self._pending_edit: Optional[MapCoordinate] = None

    @property
    def mode(self) -> EditorMode:
        """Obtiene el modo actual del editor."""
        return self._mode

    @property
    def is_edit_mode(self) -> bool:
        """Verifica si está en modo edición."""
        return self._mode == EditorMode.EDIT

    @property
    def has_pending_edit(self) -> bool:
        """Verifica si hay una edición pendiente."""
        return self._pending_edit is not None

    @property
    def pending_coordinate(self) -> Optional[MapCoordinate]:
        """Obtiene la coordenada de edición pendiente."""
        return self._pending_edit

    def toggle_edit_mode(self) -> EditorMode:
        """
        Alterna entre modo inspección y edición.

        Returns:
            EditorMode: El nuevo modo activo
        """
        if self._mode == EditorMode.INSPECT:
            self._mode = EditorMode.EDIT
            print("\nModo edición activado")
            print("   - Click en una celda para editarla")
            print("   - Presiona números (0,1...) para cambiar el terreno")
            print("   - V para salir del modo edición")
            print("   Tipos disponibles:")
            for terrain in TerrainType:
                print(f"\t{terrain.value} - {terrain.name}")
        else:
            self._mode = EditorMode.INSPECT
            self._pending_edit = None
            print("\nModo inspección activado...")

        return self._mode

    def exit_edit_mode(self) -> EditorMode:
        """
        Sale del modo edición y regresa a inspección.

        Returns:
            EditorMode: El nuevo modo activo
        """
        if self._mode == EditorMode.EDIT:
            self._mode = EditorMode.INSPECT
            self._pending_edit = None
            print("\nSaliendo del modo edición...\n")

        return self._mode

    def start_cell_edit(self, coordinate: MapCoordinate, map_obj: Map) -> bool:
        """
        Inicia la edición de una celda específica.

        Args:
            coordinate: Coordenada de la celda a editar
            map_obj: Mapa que contiene la celda

        Returns:
            bool: True si se puede iniciar la edición
        """
        if not self.is_edit_mode:
            return False

        # Validar coordenadas
        if not self._validate_coordinate(coordinate, map_obj):
            return False

        self._pending_edit = coordinate

        # Mostrar información de la celda actual
        current_cell = map_obj.grid[coordinate.row][coordinate.col]
        print(f"\nEditando celda {coordinate.human_format}")
        print(
            f"  Terreno actual: {current_cell.terrain.name} ({current_cell.terrain.value})")

        return True

    def apply_terrain_change(self, terrain_value: int, map_obj: Map) -> bool:
        """
        Aplica un cambio de terreno a la celda pendiente.

        Args:
            terrain_value: Valor numérico del nuevo tipo de terreno
            map_obj: Mapa a modificar

        Returns:
            bool: True si el cambio se aplicó correctamente
        """
        if not self.has_pending_edit:
            return False

        try:
            # Validar el tipo de terreno
            new_terrain = TerrainType.from_value(terrain_value)
        except ValueError:
            print(f"Tipo de terreno inválido: {terrain_value}")
            return False

        # Crear y ejecutar el comando
        command = EditCellCommand(
            map_obj=map_obj,
            coordinate=self._pending_edit,
            new_terrain=new_terrain
        )

        if command.execute():
            # Guardar en el historial
            self._add_command_to_history(command)

            print(
                f"  Terreno nuevo: {new_terrain.name} ({new_terrain.value})")
            self._pending_edit = None
            return True
        else:
            print(
                f"Error al modificar celda {self._pending_edit.human_format}")
            return False

    def cancel_pending_edit(self) -> bool:
        """
        Cancela la edición pendiente.

        Returns:
            bool: True si había una edición pendiente que se canceló
        """
        if self.has_pending_edit:
            print(f"Edición de {self._pending_edit.human_format} cancelada")
            self._pending_edit = None
            return True
        return False

    def undo_last_command(self) -> bool:
        """
        Deshace el último comando ejecutado.

        Returns:
            bool: True si se pudo deshacer un comando
        """
        if self._current_command_index >= 0:
            command = self._command_history[self._current_command_index]
            if command.undo():
                self._current_command_index -= 1
                print("↶ Último cambio deshecho")
                return True
            else:
                print("No se pudo deshacer el último cambio")
        else:
            print("No hay cambios para deshacer")

        return False

    def get_command_history_size(self) -> int:
        """
        Obtiene el número de comandos en el historial.

        Returns:
            int: Número de comandos ejecutados
        """
        return len(self._command_history)

    def clear_history(self) -> None:
        """Limpia el historial de comandos."""
        self._command_history.clear()
        self._current_command_index = -1
        print("Historial de edición limpiado")

    def _validate_coordinate(self, coordinate: MapCoordinate, map_obj: Map) -> bool:
        """
        Valida que una coordenada esté dentro del mapa.

        Args:
            coordinate: Coordenada a validar
            map_obj: Mapa para verificar límites

        Returns:
            bool: True si la coordenada es válida
        """
        return (0 <= coordinate.row < map_obj.rows and
                0 <= coordinate.col < map_obj.cols)

    def _add_command_to_history(self, command: ICommand) -> None:
        """
        Agrega un comando al historial.

        Args:
            command: Comando a agregar
        """
        # Remover comandos posteriores al índice actual (para redo futuro)
        self._command_history = self._command_history[:self._current_command_index + 1]

        # Agregar nuevo comando
        self._command_history.append(command)
        self._current_command_index += 1
