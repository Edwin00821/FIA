from typing import List, Set, Optional, Tuple
from dataclasses import dataclass

from src.core.search import SearchNode, SearchResult


@dataclass
class TreeConsoleConfig:
    """Configuración para el renderizado del árbol por consola."""
    show_position: bool = True
    # Formato de coordenadas humanas (A1, B2, etc.)
    human_readable: bool = True

    # Caracteres para el árbol
    branch_char: str = "├──"
    last_branch_char: str = "└──"
    vertical_char: str = "│  "
    space_char: str = "   "


class TreeConsoleRenderer:
    """
    Renderizador de árbol de búsqueda para consola.

    Genera una representación tipo 'tree' del árbol de búsqueda,
    mostrando la estructura jerárquica de exploración.
    """

    def __init__(self, config: Optional[TreeConsoleConfig] = None):
        """
        Inicializa el renderizador de consola.

        Args:
            config: Configuración de renderizado (usa defaults si es None)
        """
        self.config = config or TreeConsoleConfig()

    def _position_to_human(self, position: Tuple[int, int]) -> str:
        """
        Convierte una posición (row, col) a formato humano (A1, B2, etc.).

        Args:
            position: Tupla (row, col) en formato 0-indexado

        Returns:
            String con formato humano (e.g., "A1", "B10")
        """
        row, col = position
        human_row = row + 1  # Convertir a 1-indexado
        human_col = chr(ord('A') + col)  # Convertir a letra
        return f"({human_row},{human_col})"

    def render_all_trees(self, result: SearchResult) -> str:
        """
        Renderiza los tres tipos de árboles: completo, decisiones y camino óptimo.

        Args:
            result: Resultado de búsqueda con el árbol

        Returns:
            String con los tres árboles formateados
        """
        if not result or not result.root_node:
            return "No hay árbol de búsqueda disponible"

        lines = []

        lines.append("\n" + "="*60)
        lines.append("CAMINO ÓPTIMO")
        lines.append("="*60)

        if result.success and result.solution_path:
            lines.append(self.render_solution_path(
                result.root_node, result.solution_path))
        else:
            lines.append("No se encontró solución")

        lines.append("\n" + "="*60)
        lines.append("ÁRBOL DE DECISIONES")
        lines.append("="*60)
        lines.append(self.render_decisions(result.root_node))

        lines.append("\n" + "="*60)
        lines.append("ÁRBOL COMPLETO - PASO A PASO")
        lines.append("="*60)
        lines.append(self.render(result.root_node))

        lines.append("\n" + "="*60)

        return "\n".join(lines)

    def render(self, root_node: SearchNode | None) -> str:
        """
        Renderiza el árbol completo como texto.

        Args:
            root_node: Nodo raíz del árbol

        Returns:
            String con el árbol formateado
        """
        if not root_node:
            return "No hay árbol de búsqueda disponible"

        lines = []
        lines.append("")
        self._render_node(root_node, "", True, lines, None)
        return "\n".join(lines)

    def render_decisions(self, root_node: SearchNode | None) -> str:
        """
        Renderiza solo los nodos de decisión del árbol.

        Args:
            root_node: Nodo raíz del árbol

        Returns:
            String con el árbol de decisiones formateado
        """
        if not root_node:
            return "No hay árbol de búsqueda disponible"

        lines = []
        lines.append("")
        self._render_node_decisions(root_node, "", True, lines)
        return "\n".join(lines)

    def render_solution_path(self, root_node: SearchNode | None, solution_path: List[Tuple[int, int]]) -> str:
        """
        Renderiza solo el camino de la solución.

        Args:
            root_node: Nodo raíz del árbol
            solution_path: Lista de posiciones del camino solución

        Returns:
            String con el camino solución formateado
        """
        if not root_node or not solution_path:
            return "No hay camino de solución disponible"

        solution_set = set(solution_path)
        lines = []
        lines.append("")
        self._render_node(root_node, "", True, lines, solution_set)
        return "\n".join(lines)

    def _render_node(
        self,
        node: SearchNode,
        prefix: str,
        is_last: bool,
        lines: List[str],
        solution_filter: Optional[Set[Tuple[int, int]]] = None
    ) -> None:
        """
        Renderiza un nodo y sus hijos recursivamente.

        Args:
            node: Nodo actual a renderizar
            prefix: Prefijo de indentación acumulado
            is_last: Si este nodo es el último hijo de su padre
            lines: Lista acumuladora de líneas de texto
            solution_filter: Si se proporciona, solo renderiza nodos en este set
        """
        # Si hay filtro de solución, solo procesar nodos en el camino
        if solution_filter is not None and node.position not in solution_filter:
            return

        # Formatear el nodo actual
        line = self._format_node(node, prefix, is_last)
        lines.append(line)

        # Preparar prefijo para hijos
        if node.children:
            # Filtrar hijos si es necesario
            children_to_render = node.children
            if solution_filter is not None:
                children_to_render = [
                    c for c in node.children if c.position in solution_filter]

            if children_to_render:
                child_prefix = prefix
                if is_last:
                    child_prefix += self.config.space_char
                else:
                    child_prefix += self.config.vertical_char

                for i, child in enumerate(children_to_render):
                    is_last_child = (i == len(children_to_render) - 1)
                    self._render_node(
                        child,
                        child_prefix,
                        is_last_child,
                        lines,
                        solution_filter
                    )

    def _render_node_decisions(
        self,
        node: SearchNode,
        prefix: str,
        is_last: bool,
        lines: List[str]
    ) -> None:
        """
        Renderiza solo los nodos que son puntos de decisión o hojas.

        Args:
            node: Nodo actual a renderizar
            prefix: Prefijo de indentación acumulado
            is_last: Si este nodo es el último hijo de su padre
            lines: Lista acumuladora de líneas de texto
        """
        # Solo renderizar si es punto de decisión, es hoja (sin hijos), o es la raíz
        if node.is_decision_point or node.is_leaf() or node.depth == 0:
            line = self._format_node_decision(node, prefix, is_last)
            lines.append(line)

            # Buscar descendientes que sean puntos de decisión o hojas
            decision_descendants = self._get_decision_descendants(node)

            if decision_descendants:
                child_prefix = prefix
                if is_last:
                    child_prefix += self.config.space_char
                else:
                    child_prefix += self.config.vertical_char

                for i, descendant in enumerate(decision_descendants):
                    is_last_child = (i == len(decision_descendants) - 1)
                    self._render_node_decisions(
                        descendant,
                        child_prefix,
                        is_last_child,
                        lines
                    )
        else:
            # Si no es decisión ni hoja, buscar en sus hijos
            for child in node.children:
                self._render_node_decisions(child, prefix, is_last, lines)

    def _get_decision_descendants(self, node: SearchNode) -> List[SearchNode]:
        """
        Obtiene los descendientes directos que son puntos de decisión o hojas.

        Args:
            node: Nodo desde donde buscar

        Returns:
            Lista de nodos descendientes que son puntos de decisión o hojas
        """
        decision_nodes = []
        queue = list(node.children)

        while queue:
            current = queue.pop(0)
            if current.is_decision_point or current.is_leaf():
                decision_nodes.append(current)
            else:
                # Si no es decisión ni hoja, seguir buscando en sus hijos
                queue.extend(current.children)

        return decision_nodes

    def _format_node_decision(
        self,
        node: SearchNode,
        prefix: str,
        is_last: bool
    ) -> str:
        """
        Formatea un nodo individual para el árbol de decisiones.

        Args:
            node: Nodo a formatear
            prefix: Prefijo de indentación
            is_last: Si es el último hijo

        Returns:
            String formateado del nodo
        """
        # Elegir el símbolo de rama
        if node.depth == 0:
            branch = ""
        else:
            branch = self.config.last_branch_char if is_last else self.config.branch_char

        # Información básica del nodo
        parts = []

        # Posición
        if self.config.show_position:
            if self.config.human_readable:
                parts.append(self._position_to_human(node.position))
            else:
                parts.append(f"({node.position[0]},{node.position[1]})")

        # Contar descendientes que son decisiones o hojas
        decision_count = len(self._get_decision_descendants(node))
        parts.append(f"({decision_count} hijos)")

        # Marcadores especiales
        if node.is_decision_point:
            parts.append("[DECISIÓN]")
        if node.is_dead_end:
            parts.append("[DEAD END]")

        return f"{prefix}{branch} {' '.join(parts)}"

    def _get_decision_descendants(self, node: SearchNode) -> List[SearchNode]:
        """
        Obtiene los descendientes directos que son puntos de decisión.

        Args:
            node: Nodo desde donde buscar

        Returns:
            Lista de nodos descendientes que son puntos de decisión
        """
        decision_nodes = []
        queue = list(node.children)

        while queue:
            current = queue.pop(0)
            if current.is_decision_point:
                decision_nodes.append(current)
            else:
                # Si no es decisión, seguir buscando en sus hijos
                queue.extend(current.children)

        return decision_nodes

    def _format_node(
        self,
        node: SearchNode,
        prefix: str,
        is_last: bool
    ) -> str:
        """
        Formatea un nodo individual.

        Args:
            node: Nodo a formatear
            prefix: Prefijo de indentación
            is_last: Si es el último hijo

        Returns:
            String formateado del nodo
        """
        # Elegir el símbolo de rama
        if node.depth == 0:
            branch = ""
        else:
            branch = self.config.last_branch_char if is_last else self.config.branch_char

        # Información básica del nodo
        parts = []

        # Posición
        if self.config.show_position:
            if self.config.human_readable:
                parts.append(self._position_to_human(node.position))
            else:
                parts.append(f"({node.position[0]},{node.position[1]})")

        # Número de hijos
        parts.append(f"({len(node.children)} hijos)")

        # Marcadores especiales
        if node.is_decision_point:
            parts.append("[DECISIÓN]")
        if node.is_dead_end:
            parts.append("[DEAD END]")

        return f"{prefix}{branch} {' '.join(parts)}"
