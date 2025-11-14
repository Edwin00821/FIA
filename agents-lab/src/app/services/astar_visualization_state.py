from typing import Dict, Tuple, Set, Optional
from dataclasses import dataclass


@dataclass
class AStarNodeInfo:
    """Información de un nodo para visualización de A*."""
    position: Tuple[int, int]
    g_cost: float  # c(I,A) - costo desde inicio
    h_cost: float  # d(A,M) - distancia a meta (heurística)
    f_cost: float  # h(A,I,M) - costo total
    is_open: bool  # ¿Está en open set?
    is_closed: bool  # ¿Está en closed set?


class AStarVisualizationState:
    """
    Estado de visualización para el algoritmo A*.
    
    Mantiene información sobre nodos abiertos, cerrados y sus costos
    para renderizar en el mapa.
    """
    
    def __init__(self):
        """Inicializa el estado de visualización."""
        self.nodes_info: Dict[Tuple[int, int], AStarNodeInfo] = {}
        self.open_set: Set[Tuple[int, int]] = set()
        self.closed_set: Set[Tuple[int, int]] = set()
        self.current_position: Optional[Tuple[int, int]] = None
        self.is_active: bool = False
    
    def add_node(
        self,
        position: Tuple[int, int],
        g_cost: float,
        h_cost: float,
        f_cost: float,
        is_open: bool = False,
        is_closed: bool = False
    ) -> None:
        """
        Agrega o actualiza información de un nodo.
        
        Args:
            position: Posición del nodo
            g_cost: Costo acumulado desde inicio
            h_cost: Heurística a meta
            f_cost: Costo total
            is_open: Si está en open set
            is_closed: Si está en closed set
        """
        self.nodes_info[position] = AStarNodeInfo(
            position=position,
            g_cost=g_cost,
            h_cost=h_cost,
            f_cost=f_cost,
            is_open=is_open,
            is_closed=is_closed
        )
        
        if is_open:
            self.open_set.add(position)
            self.closed_set.discard(position)
        elif is_closed:
            self.closed_set.add(position)
            self.open_set.discard(position)
    
    def mark_as_closed(self, position: Tuple[int, int]) -> None:
        """
        Marca un nodo como cerrado.
        
        Args:
            position: Posición del nodo
        """
        if position in self.nodes_info:
            self.nodes_info[position].is_closed = True
            self.nodes_info[position].is_open = False
        
        self.closed_set.add(position)
        self.open_set.discard(position)
    
    def get_node_info(self, position: Tuple[int, int]) -> Optional[AStarNodeInfo]:
        """
        Obtiene información de un nodo.
        
        Args:
            position: Posición del nodo
            
        Returns:
            AStarNodeInfo si existe, None en caso contrario
        """
        return self.nodes_info.get(position)
    
    def clear(self) -> None:
        """Limpia todo el estado."""
        self.nodes_info.clear()
        self.open_set.clear()
        self.closed_set.clear()
        self.current_position = None
        self.is_active = False
    
    def activate(self) -> None:
        """Activa la visualización."""
        self.is_active = True
    
    def deactivate(self) -> None:
        """Desactiva la visualización."""
        self.is_active = False
