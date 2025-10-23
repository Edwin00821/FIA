from typing import Optional, Set, List, Tuple
from dataclasses import dataclass, field

from src.core.search import SearchStep, SearchResult


@dataclass
class VisualizationState:
    """
    Estado de visualización para búsqueda y reproducción.
    
    Mantiene el estado actual de qué se debe mostrar en pantalla
    durante la búsqueda y reproducción.
    """
    # Estado de búsqueda
    current_step: Optional[SearchStep] = None
    search_result: Optional[SearchResult] = None
    
    # Conjuntos de posiciones para renderizado
    visited_positions: Set[Tuple[int, int]] = field(default_factory=set)
    frontier_positions: Set[Tuple[int, int]] = field(default_factory=set)
    current_path: List[Tuple[int, int]] = field(default_factory=list)
    solution_path: List[Tuple[int, int]] = field(default_factory=list)
    
    # Estado de reproducción
    is_playing: bool = False
    playback_mode: str = "step"  # "step" o "decision"
    
    # Flags de visualización
    show_tree: bool = False
    show_frontier: bool = True
    show_visited: bool = True
    show_path: bool = True
    
    def update_from_step(self, step: SearchStep) -> None:
        """
        Actualiza el estado desde un paso de búsqueda.
        
        Args:
            step: Paso de búsqueda
        """
        self.current_step = step
        self.visited_positions = set(step.visited)
        self.frontier_positions = set(step.frontier)
        self.current_path = step.current_path.copy()
    
    def update_from_result(self, result: SearchResult) -> None:
        """
        Actualiza el estado desde un resultado de búsqueda.
        
        Args:
            result: Resultado de búsqueda completo
        """
        self.search_result = result
        if result.success and result.solution_path:
            self.solution_path = result.solution_path.copy()
        
        # Actualizar con el último paso
        if result.steps:
            self.update_from_step(result.steps[-1])
    
    def clear(self) -> None:
        """Limpia todo el estado de visualización."""
        self.current_step = None
        self.search_result = None
        self.visited_positions.clear()
        self.frontier_positions.clear()
        self.current_path.clear()
        self.solution_path.clear()
        self.is_playing = False
    
    def toggle_tree_view(self) -> bool:
        """
        Alterna la visualización del árbol.
        
        Returns:
            Nuevo estado de show_tree
        """
        self.show_tree = not self.show_tree
        return self.show_tree
    
    def has_solution(self) -> bool:
        """
        Verifica si hay una solución disponible.
        
        Returns:
            True si hay solución
        """
        return bool(self.solution_path)
