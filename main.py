from pygame import init, QUIT, quit as close_game
from pygame.time import Clock
from pygame.display import flip
from ball_game import BallGame
from pygame.event import get as events
from compiler import compile, Code
from sys import argv

level = 1
if len(argv) == 2:
    level = int(argv[1])

size = init()
clock = Clock()
code: Code = compile(f"levels/level{level}.fun")
game = code.game
frame = 0
while True:
    clock.tick(60)
    for e in events():
        if e.type == QUIT:
            close_game()
            quit()
        if e.type == 768 and e.key == 114:
            code = compile(f"levels/level{level}.fun")
            game = code.game
        if e.type == 768 and e.key in {49, 50, 51, 52, 53, 54, 55, 56, 57}:
            level = e.key - 48
            code = compile(f"levels/level{level}.fun")
            game = code.game
    code.execute()
    game.update(frame)
    game.draw(game.screen)
    flip()
    frame += 1
