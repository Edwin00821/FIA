from enum import Enum


class TerrainType(Enum):
    """
    Tipos básicos de terreno para celdas del mapa.
    
    Cada tipo de terreno tiene un valor numérico que corresponde a
    su representación en los archivos de mapa.
    """
    WALL = 0  # Muro o obstáculo infranqueable
    ROAD = 1  # Camino o sendero transitable

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
    
    def is_passable(self) -> bool:
        """
        Verifica si esta celda puede ser atravesada.
        
        Returns:
            bool: True si la celda puede ser transitada
        """
        return self.terrain != TerrainType.WALL
    
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
