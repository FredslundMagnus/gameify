from __future__ import annotations
from imports import *


class Ball(GameObject):
    def __init__(self, center: tuple[float, float], radius: float, color: Color = Colors.red) -> None:
        self.center = center
        self.radius = radius
        self.color = color

    def draw(self, screen: Screen):
        screen.draw_circle(Colors.white, self.center, self.radius)
        screen.draw_circle(self.color, self.center, self.radius-5)


class BallGame(Game):
    def draw(self, screen: Screen) -> None:
        screen.background(Colors.blue)
        ball = Ball((140, 120), 30)
        rect1 = Rect(0, 30, 100, 100)

        screen.draw_rect(Colors.gray, rect1, border_radius=4)
        ball.draw(screen)
