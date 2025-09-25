from typing import Dict, Optional

from src.core.map import Map
from src.core.cell import TerrainType

from src.utils.coordinate_system import MapCoordinate


class CellInfo:
    """
    Información completa sobre una celda del mapa.

    Encapsula toda la información relevante de una celda específica
    para su presentación al usuario.
    """

    def __init__(self, coordinate: MapCoordinate, terrain: TerrainType, is_passable: bool):
        """
        Inicializa la información de la celda.

        Args:
            coordinate: Coordenada de la celda
            terrain: Tipo de terreno
            is_passable: Si la celda es transitable
        """
        self.coordinate = coordinate
        self.terrain = terrain
        self.is_passable = is_passable

    def __str__(self) -> str:
        """Representación string legible para el usuario."""
        passable_status = "transitable" if self.is_passable else "no transitable"
        return (f"Celda {self.coordinate.human_format}: "
                f"{self.terrain.name.lower()} ({passable_status})")


class CellInspector:
    """
    Servicio para consultar y obtener información detallada de celdas del mapa.

    Implementa la lógica de negocio para inspeccionar celdas,
    proporcionando información formateada y fácil de entender.
    """

    def __init__(self):
        """Inicializa el inspector de celdas."""
        self._terrain_descriptions: Dict[TerrainType, str] = {
            TerrainType.WALL: "muro u obstáculo infranqueable",
            TerrainType.ROAD: "camino o sendero transitable",
            TerrainType.WATER: "superficie acuática navegable",
            TerrainType.SAND: "terreno arenoso de difícil tránsito",
            TerrainType.FOREST: "área boscosa con vegetación densa",
            TerrainType.MOUNTAIN: "terreno montañoso de gran elevación",
        }

    def inspect_cell(self, map_obj: Map, coordinate: MapCoordinate) -> Optional[CellInfo]:
        """
        Inspecciona una celda específica del mapa.

        Args:
            map_obj: Mapa a inspeccionar
            coordinate: Coordenada de la celda a inspeccionar

        Returns:
            CellInfo con la información de la celda, None si está fuera de límites
        """
        if not self._is_valid_coordinate(map_obj, coordinate):
            return None

        cell = map_obj.grid[coordinate.row][coordinate.col]

        return CellInfo(
            coordinate=coordinate,
            terrain=cell.terrain,
            is_passable=cell.is_passable()
        )

    def get_terrain_description(self, terrain: TerrainType) -> str:
        """
        Obtiene una descripción legible del tipo de terreno.

        Args:
            terrain: Tipo de terreno

        Returns:
            Descripción en texto del terreno
        """
        return self._terrain_descriptions.get(terrain, "terreno desconocido")

    def print_cell_info(self, cell_info: Optional[CellInfo]) -> None:
        """
        Imprime información de la celda en la consola.

        Args:
            cell_info: Información de la celda a imprimir
        """
        if cell_info is None:
            print("❌ Coordenada inválida o fuera del mapa")
            return

        print(f"🔍 {cell_info}")

        # Información adicional
        description = self.get_terrain_description(cell_info.terrain)
        print(f"   Descripción: {description}")

        if cell_info.is_passable:
            print("   ✅ Esta celda puede ser atravesada por agentes")
        else:
            print("   🚫 Esta celda bloquea el movimiento de agentes")

    def _is_valid_coordinate(self, map_obj: Map, coordinate: MapCoordinate) -> bool:
        """
        Valida si una coordenada está dentro de los límites del mapa.

        Args:
            map_obj: Mapa para validar
            coordinate: Coordenada a validar

        Returns:
            True si la coordenada es válida, False en caso contrario
        """
        return (0 <= coordinate.row < map_obj.rows and
                0 <= coordinate.col < map_obj.cols)
