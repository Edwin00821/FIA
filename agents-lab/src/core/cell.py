from enum import Enum, Flag
from typing import Set, TYPE_CHECKING

if TYPE_CHECKING:
    from .cost_strategy import CostStrategy


class TerrainType(Enum):
    """
    Tipos básicos de terreno para celdas del mapa.

    Cada tipo de terreno tiene un valor numérico que corresponde a
    su representación en los archivos de mapa.
    """
    WALL = 0        # Muro o obstáculo infranqueable
    ROAD = 1        # Camino o sendero transitable
    LAND = 2        # Tierra
    WATER = 3       # Agua
    SAND = 4        # Arena
    FOREST = 5      # Bosque
    MOUNTAIN = 6    # Montaña

    @classmethod
    def from_value(cls, value: int) -> 'TerrainType':
        """
        Obtiene el tipo de terreno desde un valor numérico.

        Args:
            value: Valor numérico del archivo de mapa

        Returns:
            TerrainType: Tipo de terreno correspondiente

        Raises:
            ValueError: Si el valor no es un tipo de terreno válido
        """
        for terrain in cls:
            if terrain.value == value:
                return terrain
        raise ValueError(f"Valor de terreno desconocido: {value}")


class CellMark(Flag):
    """
    Marcas que pueden aplicarse a una celda del mapa.

    Usa Flag para permitir combinaciones de marcas simultáneas.
    """
    NONE = 0
    INITIAL = 1      # I: Punto inicial
    CURRENT = 2      # X: Posición actual
    VISITED = 4      # V: Visitado
    DECISION = 8     # O: Punto de decisión
    FINAL = 16       # F: Punto final
    OPEN = 32        # O: En open set (A*)
    CLOSED = 64      # X: En closed set (A*)


class Cell:
    """
    Celda individual del mapa que almacena el tipo de terreno.

    Esta es la unidad básica de una grilla de mapa, conteniendo información
    sobre el tipo de terreno en una posición específica.
    """

    def __init__(self, terrain: TerrainType):
        """
        Inicializa una nueva celda.

        Args:
            terrain: El tipo de terreno para esta celda

        Raises:
            TypeError: Si terrain no es una instancia de TerrainType
        """
        if not isinstance(terrain, TerrainType):
            raise TypeError("terrain debe ser una instancia de TerrainType")

        self.terrain = terrain
        self.marks: Set[CellMark] = set()

        self.is_discovered: bool = False

    def discover(self) -> None:
        """Marca la celda como descubierta por un agente."""
        self.is_discovered = True

    def mask(self) -> None:
        """Enmascara la celda (la marca como no descubierta)."""
        self.is_discovered = False

    def is_visible(self) -> bool:
        """
        Verifica si la celda es visible para el agente.

        Returns:
            bool: True si la celda ha sido descubierta
        """
        return self.is_discovered

    def is_passable(self) -> bool:
        """
        Verifica si esta celda puede ser atravesada.

        Returns:
            bool: True si la celda puede ser transitada
        """
        return self.terrain != TerrainType.WALL

    def get_display_info(self) -> str:
        """
        Obtiene información formateada para mostrar al usuario.

        Returns:
            String con información legible sobre la celda
        """
        passable_status = "transitable" if self.is_passable() else "no transitable"
        base_info = f"{self.terrain.name.lower()} ({passable_status})"

        if self.marks:
            marks_display = self.get_marks_display()
            base_info += f" - Marcas: {marks_display}"

        return base_info

    def add_mark(self, mark: CellMark) -> bool:
        """
        Agrega una marca a la celda si es transitable.

        Args:
            mark: Marca a agregar

        Returns:
            bool: True si se pudo agregar la marca
        """
        if not self.is_passable():
            return False

        if mark != CellMark.NONE:
            self.marks.add(mark)
        return True

    def remove_mark(self, mark: CellMark) -> bool:
        """
        Remueve una marca de la celda.

        Args:
            mark: Marca a remover

        Returns:
            bool: True si la marca existía y se removió
        """
        if mark in self.marks:
            self.marks.remove(mark)
            return True
        return False

    def has_mark(self, mark: CellMark) -> bool:
        """
        Verifica si la celda tiene una marca específica.

        Args:
            mark: Marca a verificar

        Returns:
            bool: True si la celda tiene la marca
        """
        return mark in self.marks

    def clear_marks(self) -> None:
        """Limpia todas las marcas de la celda."""
        self.marks.clear()

    def get_marks_count(self) -> int:
        """
        Obtiene el número de marcas en la celda.

        Returns:
            int: Cantidad de marcas activas
        """
        return len(self.marks)

    def get_marks_display(self) -> str:
        """
        Obtiene una representación visual de las marcas.

        Returns:
            str: Marcas concatenadas para mostrar
        """
        mark_symbols = {
            CellMark.INITIAL: 'I',
            CellMark.CURRENT: 'X',
            CellMark.VISITED: 'V',
            CellMark.DECISION: 'O',
            CellMark.FINAL: 'F',
            CellMark.OPEN: 'O()',
            CellMark.CLOSED: 'X()'
        }

        symbols = [mark_symbols[mark]
                   for mark in self.marks if mark in mark_symbols]

        return ','.join(symbols)

    def get_movement_cost(self, cost_strategy: 'CostStrategy') -> float:
        """
        Obtiene el costo de movimiento para esta celda según una estrategia.
        
        Args:
            cost_strategy: Estrategia de costos a aplicar
            
        Returns:
            Costo de movimiento para esta celda
        """
        return cost_strategy.get_cost(self.terrain)
    
    def __eq__(self, other) -> bool:
        """Verifica igualdad con otra celda."""
        if not isinstance(other, Cell):
            return False
        return self.terrain == other.terrain

    def __str__(self) -> str:
        """Representación string de la celda."""
        return f"Cell({self.terrain.name})"

    def __repr__(self) -> str:
        """Representación string detallada para debug."""
        return f"Cell(terrain={self.terrain})"
