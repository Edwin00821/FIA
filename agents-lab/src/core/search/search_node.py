from typing import Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class SearchNode:
    """
    Nodo en el árbol de búsqueda.

    Representa un estado en la exploración del laberinto, incluyendo
    su posición, padre, hijos y metadatos para visualización.
    """
    position: Tuple[int, int]
    parent: Optional['SearchNode'] = None
    children: List['SearchNode'] = None
    depth: int = 0
    is_decision_point: bool = False
    is_dead_end: bool = False

    def __post_init__(self):
        """Inicializa la lista de hijos si es None."""
        if self.children is None:
            self.children = []

    def add_child(self, child: 'SearchNode') -> None:
        """
        Agrega un hijo a este nodo.

        Args:
            child: Nodo hijo a agregar
        """
        self.children.append(child)
        child.parent = self
        child.depth = self.depth + 1

    def get_path_to_root(self) -> List['SearchNode']:
        """
        Obtiene el camino desde este nodo hasta la raíz.

        Returns:
            Lista de nodos desde la raíz hasta este nodo
        """
        path = []
        current = self
        while current is not None:
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

    def is_leaf(self) -> bool:
        """
        Verifica si este nodo es una hoja (sin hijos).

        Returns:
            True si es hoja
        """
        return len(self.children) == 0

    def __eq__(self, other) -> bool:
        """Compara nodos por posición."""
        if not isinstance(other, SearchNode):
            return False
        return self.position == other.position

    def __hash__(self) -> int:
        """Hash basado en posición para uso en sets/dicts."""
        return hash(self.position)

    def __str__(self) -> str:
        """Representación string del nodo."""
        return f"SearchNode(pos={self.position}, depth={self.depth}, children={len(self.children)})"

    def __repr__(self) -> str:
        """Representación detallada para debug."""
        return self.__str__()
