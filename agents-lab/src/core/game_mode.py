from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Dict, Any


class GameMode(Enum):
    """Modos de juego disponibles."""
    MAZE = "maze"
    MAP = "map"


@dataclass
class GameConfig:
    """
    Configuración específica de un modo de juego.

    Attributes:
        mode: Modo de juego activo
        map_path: Ruta al archivo del mapa
        initial_position: Posición inicial (row, col)
        goal_position: Posición del objetivo (row, col)
        entity_type: Tipo de entidad a crear ("1", "2", "3", etc. para agentes o "human", "monkey", etc. para beings)
        entity_config: Configuración adicional específica de la entidad
    """
    mode: GameMode
    map_path: str
    initial_position: Tuple[int, int]
    goal_position: Tuple[int, int]
    entity_type: str
    entity_config: Dict[str, Any] = None

    def __post_init__(self):
        """Inicializa entity_config si es None."""
        if self.entity_config is None:
            self.entity_config = {}
