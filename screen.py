from __future__ import annotations
from pygame.draw import rect as draw_rect, circle as draw_circle
from pygame.surface import Surface
from pygame.display import set_mode as create_window
from colors import Color, Colors
from pygame import Rect


class Screen:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.window: Surface = create_window((width, height))

    def background(self, color: Color) -> None:
        self.window.fill(color.color)

    def draw_rect(self, color: Color, rect: Rect, width: int | None = None, border_radius: int | None = None) -> None:
        draw_rect(self.window, color.color, rect, width if width is not None else 0, border_radius if border_radius is not None else -1)

    def draw_circle(self, color: Color, center: tuple[float, float], radius: float) -> None:
        draw_circle(self.window, color.color, center, radius)
