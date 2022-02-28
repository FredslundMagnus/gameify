from pygame import init, QUIT, quit as close_game
from pygame.time import Clock
from pygame.display import flip
from ball_game import BallGame
from pygame.event import get as events

size = init()
clock = Clock()
game = BallGame(640, 480)

while True:
    clock.tick(60)
    for e in events():
        if e.type == QUIT:
            close_game()
            quit()
    game.draw(game.screen)
    flip()
