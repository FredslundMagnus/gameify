from __future__ import annotations
from imports import *


class Ball(GameObject):
    def __init__(self, center: tuple[float, float], radius: float, speed: tuple[float, float] = (0, 0), color: Color = Colors.red, weight: float = 1) -> None:
        self.center = XandY(*center)
        self.radius = radius
        self.color = color
        self.speed = XandY(*speed)
        self.weight = weight

    def draw(self, screen: Screen):
        screen.draw_circle(Colors.white, self.center, self.radius)
        screen.draw_circle(self.color, self.center, self.radius-5)

    @property
    def rect(self) -> Rect:
        return Rect(self.center.x - self.radius, self.center.y - self.radius, self.radius*2, self.radius*2)

    def update(self, platforms: list[Platform], goals: list[Goal]):
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
        for goal in goals:
            if goal.rect.colliderect(self.rect):
                print("YOU WIN!") 
                # quit()
                



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

    def ball_collisions(self):
        for i in range(len(self.balls)):
            ball = self.balls[i]
            for j in range(i + 1, len(self.balls)):
                ball2 = self.balls[j]
                if not ball.rect.colliderect(ball2):
                    continue
                pos_dif = (ball.center.x - ball2.center.x, ball.center.y - ball2.center.y)
                len_pos = (pos_dif[0] ** 2 + pos_dif[1] ** 2) ** (1/2)
                pos_dif_norm = (pos_dif[0] / len_pos, pos_dif[1] / len_pos)
                speed_dif = (ball.speed.x - ball2.speed.x, ball.speed.y - ball2.speed.y)
                speed_proj = speed_dif[0] * pos_dif_norm[0] + speed_dif[1] * pos_dif_norm[1]
                relative_weight = ball.weight / ball2.weight
                
                ball.speed.x -= 2 * pos_dif_norm[0] * speed_proj / (relative_weight + 1)
                ball.speed.y -= 2 * pos_dif_norm[1] * speed_proj / (relative_weight + 1)
                ball2.speed.x += 2 * pos_dif_norm[0] * speed_proj * relative_weight / (relative_weight + 1)
                ball2.speed.y += 2 * pos_dif_norm[1] * speed_proj * relative_weight / (relative_weight + 1)




    def update(self) -> None:
        for platform in self.platforms:
            platform.update()
        for goal in self.goals:
            goal.update()
        for ball in self.balls:
            ball.update(self.platforms, self.goals)
        self.ball_collisions()
