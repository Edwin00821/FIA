from abc import ABC, abstractmethod
from typing import Dict
from enum import Enum

from .cell import TerrainType


class BeingType(Enum):
    """Tipos de seres con diferentes costos de movimiento."""
    MONKEY = "monkey"
    OCTOPUS = "octopus"
    HUMAN = "human"


class CostStrategy(ABC):
    """
    Estrategia abstracta para calcular costos de movimiento por terreno.
    
    Implementa el patrón Strategy para permitir diferentes costos
    según el tipo de ser.
    """
    
    @abstractmethod
    def get_cost(self, terrain: TerrainType) -> float:
        """
        Obtiene el costo de moverse a través de un tipo de terreno.
        
        Args:
            terrain: Tipo de terreno
            
        Returns:
            Costo de movimiento (float('inf') si es intransitable)
        """
        pass
    
    @abstractmethod
    def can_traverse(self, terrain: TerrainType) -> bool:
        """
        Verifica si el ser puede atravesar un tipo de terreno.
        
        Args:
            terrain: Tipo de terreno
            
        Returns:
            True si puede atravesarlo, False en caso contrario
        """
        pass


class MonkeyCostStrategy(CostStrategy):
    """Estrategia de costos para el Mono."""
    
    COSTS: Dict[TerrainType, float] = {
        TerrainType.WALL: float('inf'),
        TerrainType.ROAD: 1,
        TerrainType.LAND: 2,
        TerrainType.WATER: 4,
        TerrainType.SAND: 3,
        TerrainType.FOREST: 1,
        TerrainType.MOUNTAIN: float('inf'),  # N/A
    }
    
    def get_cost(self, terrain: TerrainType) -> float:
        """Obtiene el costo para el mono."""
        return self.COSTS.get(terrain, float('inf'))
    
    def can_traverse(self, terrain: TerrainType) -> bool:
        """Verifica si el mono puede atravesar el terreno."""
        return self.get_cost(terrain) != float('inf')


class OctopusCostStrategy(CostStrategy):
    """Estrategia de costos para el Pulpo."""
    
    COSTS: Dict[TerrainType, float] = {
        TerrainType.WALL: float('inf'),
        TerrainType.ROAD: 1,
        TerrainType.LAND: 2,
        TerrainType.WATER: 1,
        TerrainType.SAND: float('inf'),  # N/A
        TerrainType.FOREST: 3,
        TerrainType.MOUNTAIN: float('inf'),  # N/A
    }
    
    def get_cost(self, terrain: TerrainType) -> float:
        """Obtiene el costo para el pulpo."""
        return self.COSTS.get(terrain, float('inf'))
    
    def can_traverse(self, terrain: TerrainType) -> bool:
        """Verifica si el pulpo puede atravesar el terreno."""
        return self.get_cost(terrain) != float('inf')


class HumanCostStrategy(CostStrategy):
    """Estrategia de costos para el Humano (todos los terrenos cuestan 1)."""
    
    def get_cost(self, terrain: TerrainType) -> float:
        """Obtiene el costo para el humano."""
        if terrain == TerrainType.WALL:
            return float('inf')
        return 1.0
    
    def can_traverse(self, terrain: TerrainType) -> bool:
        """Verifica si el humano puede atravesar el terreno."""
        return terrain != TerrainType.WALL


class CostStrategyFactory:
    """Fábrica para crear estrategias de costo según el tipo de ser."""
    
    _strategies: Dict[BeingType, type[CostStrategy]] = {
        BeingType.MONKEY: MonkeyCostStrategy,
        BeingType.OCTOPUS: OctopusCostStrategy,
        BeingType.HUMAN: HumanCostStrategy,
    }
    
    @classmethod
    def create(cls, being_type: BeingType) -> CostStrategy:
        """
        Crea una estrategia de costo para un tipo de ser.
        
        Args:
            being_type: Tipo de ser
            
        Returns:
            Instancia de CostStrategy
            
        Raises:
            ValueError: Si el tipo de ser no es válido
        """
        strategy_class = cls._strategies.get(being_type)
        if not strategy_class:
            raise ValueError(f"Tipo de ser desconocido: {being_type}")
        return strategy_class()
    
    @classmethod
    def from_string(cls, being_type_str: str) -> CostStrategy:
        """
        Crea una estrategia de costo desde un string.
        
        Args:
            being_type_str: String del tipo de ser ("monkey", "octopus", "human")
            
        Returns:
            Instancia de CostStrategy
        """
        try:
            being_type = BeingType(being_type_str.lower())
            return cls.create(being_type)
        except ValueError:
            raise ValueError(f"Tipo de ser desconocido: {being_type_str}")
