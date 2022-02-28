from __future__ import annotations
from imports import *





class Ball(GameObject):
    def __init__(self, center: tuple[float, float], radius: float, speed: tuple[float, float] = (0, 0), color: Color = Colors.red) -> None:
        self.center = XandY(*center)
        self.radius = radius
        self.color = color
        self.speed = XandY(*speed)

    def draw(self, screen: Screen):
        screen.draw_circle(Colors.white, self.center, self.radius)
        screen.draw_circle(self.color, self.center, self.radius-5)

    @property
    def rect(self) -> Rect:
        return Rect(self.center.x - self.radius, self.center.y - self.radius, self.radius*2, self.radius*2)

    def update(self, platforms: list[Platform]):
        self.speed.y += self.gravity
        self.center = XandY(self.center.x + self.speed.x, self.center.y + self.speed.y)
        for platform in platforms:
            if not platform.rect.colliderect(self.rect):
                continue

            if platform.rect.top <= self.rect.bottom:
                self.speed = XandY(self.speed.x, -abs(self.speed.y))
            # if platform.rect.top >= self.rect.bottom:
            #     self.speed = XandY(self.speed.x, abs(self.speed.y))

            # if platform.rect.left <= self.rect.right:
            #     self.speed = XandY(-abs(self.speed.x), self.speed.y)
            # if platform.rect.left >= self.rect.right:
            #     self.speed = XandY(abs(self.speed.x), self.speed.y)


class Platform(GameObject):
    def __init__(self, left: float, top: float, width: float, height: float, color: Color = Colors.gray.c900) -> None:
        self.rect = Rect(left, top, width, height)
        self.color = color

    def draw(self, screen: Screen):
        screen.draw_rect(self.color, self.rect, border_radius=4)


class BallGame(Game):
    elements = {"Ball": Ball, "Platform": Platform}

    def create(self) -> None:
        self.balls = [Ball((140, 120), 30, (1, 0)), Ball((240, 120), 30, (-1, 0))]
        self.platforms = [Platform(0, 300, 400, 20), Platform(40, 50, 20, 400), Platform(340, 50, 20, 400)]

    def draw(self, screen: Screen) -> None:
        screen.background(Colors.blue)

        for platform in self.platforms:
            platform.draw(screen)

        for ball in self.balls:
            ball.draw(screen)

    def update(self) -> None:
        for ball in self.balls:
            ball.update(self.platforms)
