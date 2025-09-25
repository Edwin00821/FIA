from abc import ABC, abstractmethod
from typing import Tuple


class IGraphicsEngine(ABC):
    """Interfaz para motores gráficos."""

    @abstractmethod
    def initialize(self, width: int, height: int, title: str) -> None:
        """Inicializa el motor gráfico y crea la ventana."""
        pass

    @abstractmethod
    def clear_screen(self, color: Tuple[int, int, int]) -> None:
        """Limpia la pantalla con el color especificado."""
        pass

    @abstractmethod
    def draw_rectangle(self, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]) -> None:
        """Dibuja un rectángulo sólido."""
        pass

    @abstractmethod
    def draw_line(self, start: Tuple[int, int], end: Tuple[int, int], color: Tuple[int, int, int], width: int) -> None:
        """Dibuja una línea."""
        pass

    @abstractmethod
    def draw_text(self, text: str, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """Dibuja texto centrado en las coordenadas dadas."""
        pass

    @abstractmethod
    def present(self) -> None:
        """Presenta el frame en pantalla."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Limpia recursos del motor gráfico."""
        pass
