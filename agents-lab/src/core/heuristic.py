from typing import Tuple, Callable
from enum import Enum


class HeuristicType(Enum):
    """Tipos de funciones heurísticas disponibles."""
    MANHATTAN = "manhattan"
    EUCLIDEAN = "euclidean"
    CHEBYSHEV = "chebyshev"


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    Calcula la distancia Manhattan entre dos posiciones.
    
    La distancia Manhattan es la suma de las diferencias absolutas
    de las coordenadas. Es admisible para movimiento en grid sin diagonales.
    
    Args:
        pos1: Primera posición (row, col)
        pos2: Segunda posición (row, col)
        
    Returns:
        Distancia Manhattan
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def euclidean_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    Calcula la distancia Euclidiana entre dos posiciones.
    
    La distancia Euclidiana es la línea recta entre dos puntos.
    Es admisible pero puede no ser óptima para grids sin diagonales.
    
    Args:
        pos1: Primera posición (row, col)
        pos2: Segunda posición (row, col)
        
    Returns:
        Distancia Euclidiana
    """
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5


def chebyshev_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    Calcula la distancia Chebyshev entre dos posiciones.
    
    La distancia Chebyshev es el máximo de las diferencias absolutas.
    Es admisible para movimiento con diagonales.
    
    Args:
        pos1: Primera posición (row, col)
        pos2: Segunda posición (row, col)
        
    Returns:
        Distancia Chebyshev
    """
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))


class HeuristicFactory:
    """Fábrica para obtener funciones heurísticas."""
    
    _heuristics = {
        HeuristicType.MANHATTAN: manhattan_distance,
        HeuristicType.EUCLIDEAN: euclidean_distance,
        HeuristicType.CHEBYSHEV: chebyshev_distance,
    }
    
    @classmethod
    def get(cls, heuristic_type: HeuristicType) -> Callable[[Tuple[int, int], Tuple[int, int]], float]:
        """
        Obtiene una función heurística.
        
        Args:
            heuristic_type: Tipo de heurística
            
        Returns:
            Función heurística
            
        Raises:
            ValueError: Si el tipo no es válido
        """
        heuristic = cls._heuristics.get(heuristic_type)
        if not heuristic:
            raise ValueError(f"Tipo de heurística desconocido: {heuristic_type}")
        return heuristic
    
    @classmethod
    def from_string(cls, heuristic_str: str) -> Callable[[Tuple[int, int], Tuple[int, int]], float]:
        """
        Obtiene una función heurística desde un string.
        
        Args:
            heuristic_str: String del tipo de heurística
            
        Returns:
            Función heurística
        """
        try:
            heuristic_type = HeuristicType(heuristic_str.lower())
            return cls.get(heuristic_type)
        except ValueError:
            raise ValueError(f"Tipo de heurística desconocido: {heuristic_str}")
