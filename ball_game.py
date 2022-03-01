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
            if platform.rect.top >= self.center.y:
                self.speed = XandY(self.speed.x, -abs(self.speed.y))
            if platform.rect.left >= self.center.x:
                self.speed = XandY(-abs(self.speed.x), self.speed.y)
            if platform.rect.right <= self.center.x:
                self.speed = XandY(abs(self.speed.x), self.speed.y)
            if platform.rect.bottom <= self.center.y:
                self.speed = XandY(self.speed.x, abs(self.speed.y))


class Platform(GameObject):
    def __init__(self, left: float, top: float, width: float, height: float, speed: tuple[float, float] = (0, 0), color: Color = Colors.gray.c900) -> None:
        self.rect = Rect(left, top, width, height)
        self.color = color
        self.speed = XandY(*speed)

    def draw(self, screen: Screen):
        screen.draw_rect(self.color, self.rect, border_radius=4)

    def update(self):
        self.rect = self.rect.move(self.speed.x, self.speed.y)


class Goal(GameObject):
    def __init__(self, left: float, top: float, width: float, height: float, speed: tuple[float, float] = (0, 0)) -> None:
        self.rect = Rect(left, top, width, height)
        self.speed = XandY(*speed)

    def draw(self, screen: Screen):
        n = 5
        top, left = self.rect.top, self.rect.left
        width, height = self.rect.width/n, self.rect.height/n
        for x in range(n):
            for y in range(n):
                color = Colors.gray.c800 if (x+y) % 2 else Colors.white
                screen.draw_rect(color, Rect(left+x*width, top+y*height, width, height))

    def update(self):
        self.rect = self.rect.move(self.speed.x, self.speed.y)


class BallGame(Game):
    types = [Ball, Platform, Goal, Colors]

    @property
    def balls(self) -> list[Ball]:
        return [o for o in self.objects.values() if o.__class__ == Ball]

    @property
    def goals(self) -> list[Goal]:
        return [o for o in self.objects.values() if o.__class__ == Goal]

    @property
    def platforms(self) -> list[Platform]:
        return [o for o in self.objects.values() if o.__class__ == Platform]

    def draw(self, screen: Screen) -> None:
        screen.background(Colors.blue)

        for platform in self.platforms:
            platform.draw(screen)

        for goal in self.goals:
            goal.draw(screen)

        for ball in self.balls:
            ball.draw(screen)

    def update(self) -> None:
        for platform in self.platforms:
            platform.update()
        for goal in self.goals:
            goal.update()
        for ball in self.balls:
            ball.update(self.platforms)
