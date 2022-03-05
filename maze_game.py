from __future__ import annotations
from math import ceil
import random
import compiler
from imports import *
from utils import Position


class Player(GameObject):
    def __init__(self, center: tuple[float, float], maze: Maze) -> None:
        self.center = XandY(*center)
        self.color = Colors.red
        self.maze = maze
        self.speed = 5
        self.hasWon = False

    @property
    def position(self) -> Position:
        return Position(((self.center.x-20)//40, (self.center.y-20)//40))

    def draw(self, screen: Screen):
        screen.draw_rect(Colors.white, self.rect(20))
        screen.draw_rect(self.color, self.rect(17))

    def rect(self, radius) -> Rect:
        return Rect(self.center.x - radius, self.center.y - radius, radius*2, radius*2)

    def left(self) -> compiler.Future:
        return self.move("left", "x", "-")

    def right(self) -> compiler.Future:
        return self.move("right", "x", "+")

    def up(self) -> compiler.Future:
        return self.move("up", "y", "-")

    def down(self) -> compiler.Future:
        return self.move("down", "y", "+")

    def move(self, name: str, xORy: str, plusORminus: str) -> compiler.Future:
        if self.hasWon:
            return compiler.Future()
        if not self.maze.canMove(name):
            print(f"You cannot go {name}")
            return compiler.Function(name, [], [f"wait {max(ceil(40/self.speed), 1)} frames"], {"self": self})()
        return compiler.Function(name, [], [
            f"let start be self.center.{xORy}",
            "wait 1 frames",
            *("|".join([f"set self.center.{xORy} to self.center.{xORy} {plusORminus} {40/max(ceil(40/self.speed), 1)}|wait 1 frames" for _ in range(max(ceil(40/self.speed), 1) - 1)]).split("|")),
            f"set self.center.{xORy} to start{plusORminus}40"
        ], {"self": self})()

    def update(self, goal: Goal) -> None:
        if goal.rect.colliderect(self.rect(20)):
            self.color = Colors.green
            self.hasWon = True
            print("YOU WIN!")


class Block(GameObject):
    def __init__(self, point: tuple[int, int], size: float, color: Color = Colors.gray.c900) -> None:
        self.rect = Rect(point[0]*size, point[1]*size, size, size)
        self.color = color

    def draw(self, screen: Screen):
        screen.draw_rect(self.color, self.rect)


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


class Maze(GameObject):
    width: int
    height: int

    def __init__(self, level: int | None = None) -> None:
        self.size = 40
        self.level = level
        if level is not None:
            random.seed(level)
        self.player = Player(((3 * self.size)//2, self.height - (3 * self.size)//2), self)
        self.goal = Goal(self.width - 2 * self.size, self.size, self.size, self.size)
        self.create()

    def canMove(self, direction: str) -> bool:
        pos = self.player.position.position
        if direction == "up":
            return not self.have_block[(pos[0], pos[1]-1)]
        if direction == "down":
            return not self.have_block[(pos[0], pos[1]+1)]
        if direction == "left":
            return not self.have_block[(pos[0]-1, pos[1])]
        if direction == "right":
            return not self.have_block[(pos[0]+1, pos[1])]

    def is_free(self, position: Position):
        return not self.have_block[position.position]

    def create(self):
        points: dict[tuple[int, int], bool] = {}
        height = self.height//40
        width = self.width//40

        for x in range(width):
            for y in range(height):
                points[(x, y)] = not (x % 2 and y % 2)  # x in (0, width-1) or y in (0, height-1)

        splitters = [point for point in points if point[0] % 2 and point[1] % 2]
        start = random.choice(splitters)
        splitters.remove(start)
        opened = [start]

        def neighbors(element: tuple[int, int]) -> list[tuple[int, int]]:
            return [p for p in [(element[0] - 2, element[1]), (element[0] + 2, element[1]), (element[0], element[1] - 2), (element[0], element[1] + 2)] if p in splitters]

        while splitters:
            c = random.choice(opened)
            if not neighbors(c):
                opened.remove(c)
                continue
            n = random.choice(neighbors(c))
            mid = (n[0]+(c[0]-n[0])//2, n[1]+(c[1]-n[1])//2)
            points[mid] = False
            splitters.remove(n)
            opened.append(n)

        self.have_block = points
        self.blocks: list[Block] = [Block(point, self.size) for point, have_block in points.items() if have_block]


class MazeGame(Game):
    types = [Maze, Player, Block, Goal, Colors]

    def create(self, screen: Screen) -> None:
        Maze.height = screen.height
        Maze.width = screen.width

    @ property
    def blocks(self) -> list[Block]:
        return self.maze.blocks

    @ property
    def maze(self) -> Maze:
        return [o for o in self.objects.values() if o.__class__ == Maze][0]

    @ property
    def goal(self) -> Goal:
        return self.maze.goal

    @ property
    def player(self) -> Player:
        return self.maze.player

    def draw(self, screen: Screen) -> None:
        screen.background(Colors.gray)

        self.goal.draw(screen)
        for block in self.blocks:
            block.draw(screen)
        self.player.draw(screen)

    def update(self, frame: int) -> None:
        self.player.update(self.goal)
