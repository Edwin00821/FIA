from typing import Optional, List, Tuple
from dataclasses import dataclass, field


@dataclass
class SearchNode:
    """
    Nodo en el árbol de búsqueda.
    
    Representa un estado en el espacio de búsqueda con información
    sobre su posición, padre, hijos y costos (para A*).
    """
    
    position: Tuple[int, int]
    parent: Optional['SearchNode'] = None
    children: List['SearchNode'] = field(default_factory=list)
    depth: int = 0
    
    # Atributos para algoritmos informados (A*)
    g_cost: float = 0.0  # Costo acumulado desde el inicio
    h_cost: float = 0.0  # Heurística al objetivo
    f_cost: float = 0.0  # f = g + h
    
    # Metadatos
    is_decision_point: bool = False
    is_dead_end: bool = False
    
    def add_child(self, child: 'SearchNode') -> None:
        """
        Agrega un nodo hijo.
        
        Args:
            child: Nodo hijo a agregar
        """
        self.children.append(child)
        child.parent = self
        child.depth = self.depth + 1
    
    def is_leaf(self) -> bool:
        """
        Verifica si el nodo es una hoja (sin hijos).
        
        Returns:
            True si no tiene hijos
        """
        return len(self.children) == 0
    
    def get_path_to_root(self) -> List['SearchNode']:
        """
        Obtiene el camino desde este nodo hasta la raíz.
        
        Returns:
            Lista de nodos desde la raíz hasta este nodo
        """
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return list(reversed(path))
    
    def get_path_positions(self) -> List[Tuple[int, int]]:
        """
        Obtiene las posiciones del camino desde la raíz hasta este nodo.
        
        Returns:
            Lista de posiciones (row, col)
        """
        return [node.position for node in self.get_path_to_root()]
    
    def __lt__(self, other: 'SearchNode') -> bool:
        """
        Comparación para priority queue (menor f_cost tiene prioridad).
        
        Args:
            other: Otro nodo a comparar
            
        Returns:
            True si este nodo tiene menor f_cost
        """
        return self.f_cost < other.f_cost
    
    def __eq__(self, other) -> bool:
        """
        Comparación de igualdad basada en posición.
        
        Args:
            other: Otro objeto a comparar
            
        Returns:
            True si tienen la misma posición
        """
        if not isinstance(other, SearchNode):
            return False
        return self.position == other.position
    
    def __hash__(self) -> int:
        """
        Hash basado en posición para usar en sets/dicts.
        
        Returns:
            Hash de la posición
        """
        return hash(self.position)
    
    def __repr__(self) -> str:
        """Representación para debug."""
        return f"SearchNode(pos={self.position}, f={self.f_cost:.1f}, g={self.g_cost:.1f}, h={self.h_cost:.1f})"
