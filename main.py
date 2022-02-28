from pygame import init, QUIT, quit as close_game
from pygame.time import Clock
from pygame.display import flip
from ball_game import BallGame
from pygame.event import get as events
from compiler import compile, Code

size = init()
clock = Clock()
code: Code = compile("levels/level1.fun")
game = code.game

while True:
    clock.tick(60)
    for e in events():
        if e.type == QUIT:
            close_game()
            quit()
    code.execute()
    game.update()
    game.draw(game.screen)
    flip()
