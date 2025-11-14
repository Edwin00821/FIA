from typing import Optional, Tuple, Dict
from .sensors import Sensor, Direction
from .map import Map

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cost_strategy import CostStrategy
    from .cell import TerrainType


class Being:
    """
    Clase base para seres que pueden percibir el entorno.

    Los seres tienen sensores para percibir su entorno y pueden ser colocados en el mapa.
    """

    def __init__(self, sensor: Sensor):
        """
        Inicializa un nuevo ser.

        Args:
            sensor: Sensor para percepción del entorno
        """
        self.sensor = sensor
        self.position: Optional[Tuple[int, int]] = None
        self.direction: Direction = Direction.UP  # Siempre inicia hacia arriba

    def place_on_map(self, map_obj: Map, coordinate: str) -> bool:
        """
        Coloca al ser en una coordenada específica del mapa.

        Args:
            map_obj: El mapa donde colocar al ser
            coordinate: Coordenada en formato "filaColumna" (e.g., "3B")

        Returns:
            True si se colocó exitosamente
        """
        try:
            row_str, col_str = coordinate[:-1], coordinate[-1]
            row = int(row_str) - 1  # Asumiendo filas empezando en 1
            col = ord(col_str.upper()) - ord('A')  # Columnas A=0, B=1, etc.

            if 0 <= row < map_obj.rows and 0 <= col < map_obj.cols:
                self.position = (row, col)
                # Descubrir la celda inicial
                map_obj.discover_cell(row, col)
                return True
            else:
                print(f"Coordenada {coordinate} fuera de los límites del mapa")
                return False
        except (ValueError, IndexError):
            print(f"Coordenada inválida: {coordinate}")
            return False

    def perceive(self, map_obj: Map) -> Dict[str, bool]:
        """
        Percibe el entorno usando el sensor del ser.

        Args:
            map_obj: El mapa del entorno

        Returns:
            Diccionario con la información percibida
        """
        if self.position is None:
            return {}
        return self.sensor.perceive(map_obj, self.position, self.direction)

    def get_state(self) -> Dict:
        """
        Obtiene el estado actual del ser.

        Returns:
            Diccionario con información del estado
        """
        return {
            'position': self.position,
            'direction': self.direction.value if self.direction else None
        }

    def set_sensor(self, sensor: Sensor) -> None:
        """
        Cambia el sensor del ser.

        Args:
            sensor: Nuevo sensor a usar
        """
        self.sensor = sensor

    def reset(self) -> None:
        """Reinicia el estado del ser."""
        self.position = None
        self.direction = Direction.UP

    def set_cost_strategy(self, cost_strategy: 'CostStrategy') -> None:
        """
        Establece la estrategia de costos del ser.

        Args:
            cost_strategy: Estrategia de costos a usar
        """
        self.cost_strategy = cost_strategy

    def get_movement_cost(self, terrain: 'TerrainType') -> float:
        """
        Obtiene el costo de moverse a través de un terreno.

        Args:
            terrain: Tipo de terreno

        Returns:
            Costo de movimiento
        """
        if hasattr(self, 'cost_strategy') and self.cost_strategy:
            return self.cost_strategy.get_cost(terrain)
        # Costo por defecto si no hay estrategia
        return 1.0 if terrain != TerrainType.WALL else float('inf')

    def discover_adjacent_cells(self, map_obj: Map, position: Tuple[int, int]) -> None:
        """
        Descubre las celdas adyacentes a una posición (4-conectividad).

        Args:
            map_obj: El mapa donde descubrir celdas
            position: Posición central desde donde descubrir
        """
        row, col = position

        # 4 direcciones: arriba, derecha, abajo, izquierda
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Verificar límites
            if 0 <= new_row < map_obj.rows and 0 <= new_col < map_obj.cols:
                map_obj.discover_cell(new_row, new_col)

    def __str__(self) -> str:
        """Representación string del ser."""
        pos_str = f"({self.position[0]}, {self.position[1]})" if self.position else "None"
        return f"Being(position={pos_str}, direction={self.direction.value})"

    def __repr__(self) -> str:
        """Representación detallada para debug."""
        return self.__str__()
