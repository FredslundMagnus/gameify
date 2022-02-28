from imports import *


class BallGame(Game):
    def draw(self, screen: Screen) -> None:
        screen.background(Colors.red)
        ball = Rect(0, 0, 100, 30)
        rect1 = Rect(0, 30, 100, 100)

        screen.draw_rect(Colors.blue, rect1, 1)
        screen.draw_circle(Colors.green, (40, 20), 20)
