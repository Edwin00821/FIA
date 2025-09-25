from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from src.core.map import Map
from src.core.cell import Cell, TerrainType

from src.utils.coordinate_system import MapCoordinate


class ICommand(ABC):
    """Interfaz base para el patrón Command."""

    @abstractmethod
    def execute(self) -> bool:
        """
        Ejecuta el comando.

        Returns:
            bool: True si la ejecución fue exitosa
        """
        pass

    @abstractmethod
    def undo(self) -> bool:
        """
        Deshace el comando.

        Returns:
            bool: True si el deshacer fue exitoso
        """
        pass


@dataclass
class EditCellCommand(ICommand):
    """
    Comando para editar una celda del mapa.

    Implementa el patrón Command para encapsular la modificación
    de una celda, permitiendo deshacer la operación.
    """
    map_obj: Map
    coordinate: MapCoordinate
    new_terrain: TerrainType
    old_terrain: Optional[TerrainType] = None

    def execute(self) -> bool:
        """
        Ejecuta la modificación de la celda.

        Returns:
            bool: True si la modificación fue exitosa
        """
        try:
            # Validar coordenadas
            if not self._validate_coordinates():
                return False

            # Guardar el terreno actual para poder deshacerlo
            current_cell = self.map_obj.grid[self.coordinate.row][self.coordinate.col]
            self.old_terrain = current_cell.terrain

            # Crear nueva celda con el terreno especificado
            new_cell = Cell(self.new_terrain)

            # Aplicar el cambio
            self.map_obj.grid[self.coordinate.row][self.coordinate.col] = new_cell

            return True

        except Exception as e:
            print(f"Error ejecutando comando de edición: {e}")
            return False

    def undo(self) -> bool:
        """
        Deshace la modificación de la celda.

        Returns:
            bool: True si se pudo deshacer
        """
        if self.old_terrain is None:
            return False

        try:
            # Restaurar el terreno anterior
            old_cell = Cell(self.old_terrain)
            self.map_obj.grid[self.coordinate.row][self.coordinate.col] = old_cell
            return True

        except Exception as e:
            print(f"Error deshaciendo comando de edición: {e}")
            return False

    def _validate_coordinates(self) -> bool:
        """
        Valida que las coordenadas estén dentro de los límites del mapa.

        Returns:
            bool: True si las coordenadas son válidas
        """
        return (0 <= self.coordinate.row < self.map_obj.rows and
                0 <= self.coordinate.col < self.map_obj.cols)
