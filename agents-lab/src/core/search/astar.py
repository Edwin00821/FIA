from typing import Tuple, List, Set, Optional, Callable, TYPE_CHECKING
import heapq

from .search_algorithm import SearchAlgorithm
from .search_node import SearchNode
from .search_result import SearchResult

from ..map import Map
from ..cost_strategy import CostStrategy

if TYPE_CHECKING:
    from ..being import Being


class AStarSearch(SearchAlgorithm):
    """
    Implementación del algoritmo A*.
    
    A* es un algoritmo de búsqueda informada que utiliza una función
    heurística para guiar la búsqueda hacia el objetivo de manera eficiente.
    
    Soporta fog of war: solo expande nodos en celdas descubiertas.
    """
    
    def __init__(
        self,
        heuristic_func: Callable[[Tuple[int, int], Tuple[int, int]], float],
        cost_strategy: Optional[CostStrategy] = None,
        being: Optional['Being'] = None,
        use_fog_of_war: bool = False
    ):
        """
        Inicializa el algoritmo A*.
        
        Args:
            heuristic_func: Función heurística h(n)
            cost_strategy: Estrategia de costos por terreno (opcional)
            being: Ser que realiza la búsqueda (para descubrir celdas)
            use_fog_of_war: Si True, solo expande nodos en celdas descubiertas
        """
        self.heuristic_func = heuristic_func
        self.cost_strategy = cost_strategy
        self.being = being
        self.use_fog_of_war = use_fog_of_war
    
    def search(
        self,
        map_obj: Map,
        start: Tuple[int, int],
        goal: Tuple[int, int]
    ) -> SearchResult:
        """
        Ejecuta la búsqueda A* desde start hasta goal.
        
        Con fog of war, descubre el mapa dinámicamente durante la búsqueda.
        
        Args:
            map_obj: Mapa donde buscar
            start: Posición inicial (row, col)
            goal: Posición objetivo (row, col)
            
        Returns:
            SearchResult con el resultado de la búsqueda
        """
        # Descubrir celda inicial y sus adyacentes
        if self.use_fog_of_war and self.being:
            map_obj.discover_cell(start[0], start[1])
            self.being.discover_adjacent_cells(map_obj, start)
        
        # Inicializar nodo raíz
        root = SearchNode(
            position=start,
            g_cost=0.0,
            h_cost=self.heuristic_func(start, goal),
        )
        root.f_cost = root.g_cost + root.h_cost
        
        # Open set (priority queue) y closed set
        open_set: List[SearchNode] = [root]
        closed_set: Set[Tuple[int, int]] = set()
        
        # Diccionario para tracking de nodos por posición
        nodes_by_position = {start: root}
        
        nodes_expanded = 0
        
        while open_set:
            # Obtener nodo con menor f_cost
            current = heapq.heappop(open_set)
            
            # Si ya fue visitado, skip
            if current.position in closed_set:
                continue
            
            # Descubrir celdas adyacentes al nodo actual
            if self.use_fog_of_war and self.being:
                self.being.discover_adjacent_cells(map_obj, current.position)
            
            # Marcar como visitado
            closed_set.add(current.position)
            nodes_expanded += 1
            
            # ¿Llegamos al objetivo?
            if current.position == goal:
                return SearchResult(
                    success=True,
                    root_node=root,
                    goal_node=current,
                    solution_path=current.get_path_positions(),
                    nodes_expanded=nodes_expanded,
                    path_cost=current.g_cost
                )
            
            # Expandir vecinos (solo los descubiertos si hay fog of war)
            neighbors = self._get_neighbors(map_obj, current.position)
            
            for neighbor_pos in neighbors:
                # Si ya fue visitado, skip
                if neighbor_pos in closed_set:
                    continue
                
                # Con fog of war, solo expandir celdas descubiertas
                if self.use_fog_of_war:
                    neighbor_cell = map_obj.grid[neighbor_pos[0]][neighbor_pos[1]]
                    if not neighbor_cell.is_visible():
                        continue
                
                # Calcular costo del movimiento
                move_cost = self._get_movement_cost(map_obj, neighbor_pos)
                tentative_g = current.g_cost + move_cost
                
                # Verificar si ya existe el nodo
                if neighbor_pos in nodes_by_position:
                    neighbor_node = nodes_by_position[neighbor_pos]
                    
                    # Si encontramos un camino mejor, actualizar
                    if tentative_g < neighbor_node.g_cost:
                        neighbor_node.g_cost = tentative_g
                        neighbor_node.f_cost = neighbor_node.g_cost + neighbor_node.h_cost
                        neighbor_node.parent = current
                        
                        # Re-agregar a open_set con nuevo costo
                        heapq.heappush(open_set, neighbor_node)
                else:
                    # Crear nuevo nodo
                    neighbor_node = SearchNode(
                        position=neighbor_pos,
                        g_cost=tentative_g,
                        h_cost=self.heuristic_func(neighbor_pos, goal),
                    )
                    neighbor_node.f_cost = neighbor_node.g_cost + neighbor_node.h_cost
                    neighbor_node.parent = current
                    
                    nodes_by_position[neighbor_pos] = neighbor_node
                    heapq.heappush(open_set, neighbor_node)
                    
                    # Agregar como hijo para construir árbol
                    current.add_child(neighbor_node)
        
        # No se encontró camino
        return SearchResult(
            success=False,
            root_node=root,
            goal_node=None,
            solution_path=[],
            nodes_expanded=nodes_expanded,
            path_cost=float('inf')
        )
    
    def _get_neighbors(self, map_obj: Map, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Obtiene las posiciones vecinas válidas (4-conectividad).
        
        Args:
            map_obj: Mapa
            position: Posición actual
            
        Returns:
            Lista de posiciones vecinas válidas
        """
        row, col = position
        neighbors = []
        
        # 4 direcciones: arriba, derecha, abajo, izquierda
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Verificar límites
            if not (0 <= new_row < map_obj.rows and 0 <= new_col < map_obj.cols):
                continue
            
            cell = map_obj.grid[new_row][new_col]
            
            # Verificar si es transitable según estrategia de costos
            if self.cost_strategy:
                if not self.cost_strategy.can_traverse(cell.terrain):
                    continue
            else:
                if not cell.is_passable():
                    continue
            
            neighbors.append((new_row, new_col))
        
        return neighbors
    
    def _get_movement_cost(self, map_obj: Map, position: Tuple[int, int]) -> float:
        """
        Obtiene el costo de moverse a una posición.
        
        Args:
            map_obj: Mapa
            position: Posición destino
            
        Returns:
            Costo de movimiento
        """
        row, col = position
        cell = map_obj.grid[row][col]
        
        if self.cost_strategy:
            return self.cost_strategy.get_cost(cell.terrain)
        
        # Costo por defecto
        return 1.0
