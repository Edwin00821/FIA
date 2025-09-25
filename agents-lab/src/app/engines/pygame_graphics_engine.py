import pygame
from typing import Tuple, Optional

from .graphics_engine import IGraphicsEngine


class PygameGraphicsEngine(IGraphicsEngine):
    """Motor gráfico usando pygame."""

    def __init__(self):
        self._screen: Optional[pygame.Surface] = None
        self._font: Optional[pygame.font.Font] = None

    def initialize(self, width: int, height: int, title: str) -> None:
        """Inicializa pygame y crea la ventana."""
        pygame.init()
        pygame.font.init()

        self._screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self._font = pygame.font.SysFont("monospace", 16)

    def clear_screen(self, color: Tuple[int, int, int]) -> None:
        """Limpia la pantalla."""
        self._ensure_initialized()
        self._screen.fill(color)

    def draw_rectangle(self, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]) -> None:
        """Dibuja un rectángulo."""
        self._ensure_initialized()
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self._screen, color, rect)

    def draw_line(self, start: Tuple[int, int], end: Tuple[int, int], color: Tuple[int, int, int], width: int) -> None:
        """Dibuja una línea."""
        self._ensure_initialized()
        pygame.draw.line(self._screen, color, start, end, width)

    def draw_text(self, text: str, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """Dibuja texto centrado en las coordenadas dadas."""
        self._ensure_initialized()
        text_surface = self._font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self._screen.blit(text_surface, text_rect)

    def present(self) -> None:
        """Presenta el frame."""
        self._ensure_initialized()
        pygame.display.flip()

    def cleanup(self) -> None:
        """Limpia recursos de pygame."""
        pygame.quit()

    def _ensure_initialized(self) -> None:
        """Verifica que el motor esté inicializado."""
        if self._screen is None:
            raise RuntimeError(
                "Graphics engine not initialized. Call initialize() first.")
