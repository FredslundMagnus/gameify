import pygame as pg
import pygame.draw
pg.init()
clock = pg.time.Clock()
running = True
window = pg.display.set_mode((640, 480))
window.fill((255, 255, 255))
ball = pg.Rect(0, 0, 100, 30)
rect1 = pg.Rect(0, 30, 100, 100)

while running:
    clock.tick(60)
    window.fill((255, 255, 255))
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    pg.draw.rect(window, (255, 0, 255), rect1, 1)
    pg.draw.circle(window, "red", (40, 20), 20)

    pg.display.flip()

# end main loop
pg.quit()
