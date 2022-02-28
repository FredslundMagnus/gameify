from __future__ import annotations
from imports import *


class Ball(GameObject):
    def __init__(self, center: tuple[float, float], radius: float, speed: tuple[float, float] = (0, 0), color: Color = Colors.red) -> None:
        self.center = center
        self.radius = radius
        self.color = color
        self.speed = speed

    def draw(self, screen: Screen):
        screen.draw_circle(Colors.white, self.center, self.radius)
        screen.draw_circle(self.color, self.center, self.radius-5)

    @property
    def rect(self) -> Rect:
        return Rect(self.center[0] - self.radius, self.center[1] - self.radius, self.radius*2, self.radius*2)

    def update(self, platforms: list[Platform]):
        self.speed = (self.speed[0], self.speed[1] + self.gravity)
        self.center = (self.center[0], self.center[1] + self.speed[1])
        for platform in platforms:
            if not platform.rect.colliderect(self.rect):
                continue

            if platform.rect.top <= self.rect.bottom:
                self.speed = (self.speed[0], -abs(self.speed[1]))
            if platform.rect.top >= self.rect.bottom:
                self.speed = (self.speed[0], abs(self.speed[1]))

            if platform.rect.left <= self.rect.right:
                self.speed = (-abs(self.speed[0]), self.speed[1])
            if platform.rect.left >= self.rect.right:
                self.speed = (abs(self.speed[0]), self.speed[1])


class Platform(GameObject):
    def __init__(self, left: float, top: float, width: float, height: float, color: Color = Colors.gray.c900) -> None:
        self.rect = Rect(left, top, width, height)
        self.color = color

    def draw(self, screen: Screen):
        screen.draw_rect(self.color, self.rect, border_radius=4)


class BallGame(Game):
    def create(self) -> None:
        self.balls = [Ball((140, 120), 30), Ball((240, 120), 30)]
        self.platforms = [Platform(0, 300, 400, 20)]

    def draw(self, screen: Screen) -> None:
        screen.background(Colors.blue)

        for platform in self.platforms:
            platform.draw(screen)

        for ball in self.balls:
            ball.draw(screen)

    def update(self) -> None:
        for ball in self.balls:
            ball.update(self.platforms)
