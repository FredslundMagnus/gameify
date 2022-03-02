from __future__ import annotations
from ball_game import BallGame
from game import Game
from random import random


def findBloc(theLines: list[str]) -> tuple[list[str], str]:
    block = []
    state = 1
    while True:
        temp = theLines.pop(0)
        if temp.startswith("}"):
            state -= 1
        if state == 0:
            return block, temp
        if temp.endswith("{"):
            state += 1
        block.append(temp)


class Executer:
    blocks: list[list[Block]] = [[]]
    temp: list[tuple[Block, int]] = []

    @staticmethod
    def real_add(block: Block, frame: int) -> None:
        for _ in range(frame + 1 - len(Executer.blocks)):
            Executer.blocks.append([])
        Executer.blocks[frame].insert(0, block)

    @staticmethod
    def add(block: Block, frame: int = 0) -> None:
        # Executer.temp.append((block, frame))
        for _ in range(frame + 1 - len(Executer.blocks)):
            Executer.blocks.append([])
        Executer.blocks[frame].append(block)

    @staticmethod
    def run(block: Block) -> None:
        block.execute()

    @staticmethod
    def finalise() -> None:
        pass
        # for block, frame in reversed(Executer.temp):
        #     Executer.real_add(block, frame)
        # Executer.temp = []

    @staticmethod
    def execute() -> None:
        if not Executer.blocks:
            return
        while Executer.blocks[0]:
            block = Executer.blocks[0].pop(0)
            block.execute()
            Executer.finalise()
        Executer.blocks.pop(0)


class Block:
    def __init__(self, lines: list[str], scope: dict[str, object]) -> None:
        self.lines = lines
        self.scope = scope

    def execute(self) -> None:
        while self.lines and not self.scope["must_break"]:
            line = self.lines.pop(0)
            try:
                if line.startswith("wait") and line.endswith("frames"):
                    frames = int(eval(" ".join(line.split(" ")[1:-1]), self.scope))
                    return Executer.add(self, frames)
                elif "let" in line and "be" in line:
                    _, name, _, *values = line.split(" ")
                    value = eval(" ".join(values), self.scope)
                    self.scope[name] = value
                elif "set" in line and "to" in line:
                    _, part, _, *values = line.split(" ")
                    value = eval(" ".join(values), self.scope)
                    parts = part.split(".")
                    obj = self.scope[parts[0]]
                    for attribute in parts[1:-1]:
                        obj = obj.__getattribute__(attribute)
                    setter = parts[-1]
                    obj.__setattr__(setter, value)
                elif "after" in line and "frames" in line and line.endswith("{"):
                    n = int(eval(" ".join(line.split(" ")[1:-2]), self.scope))
                    lines, _ = findBloc(self.lines)
                    Executer.add(Block(lines, self.scope.copy()), frame=n)
                elif "every" in line and "frames" in line and line.endswith("{"):
                    n = int(eval(" ".join(line.split(" ")[1:-2]), self.scope))
                    lines, _ = findBloc(self.lines)
                    scope = self.scope.copy()
                    Executer.add(Block(lines, scope), frame=n)  # frame=0, hvis man vil have den gør det første gang også
                    block = [f"every {n} frames "+"{", *(lines.copy()), "}"]
                    Executer.add(Block(block, scope), frame=n)
                elif "loop" in line and "times" in line and line.endswith("{"):
                    n = int(eval(" ".join(line.split(" ")[1:-2]), self.scope))
                    lines, _ = findBloc(self.lines)
                    for _ in range(n):
                        Executer.run(Block(lines.copy(), self.scope))
                        if self.scope["must_break"] == True:
                            self.scope["must_break"] = False
                            break
                elif "loop" in line and line.endswith("{"):
                    lines, _ = findBloc(self.lines)
                    while True:
                        Executer.run(Block(lines.copy(), self.scope))
                        if self.scope["must_break"] == True:
                            self.scope["must_break"] = False
                            break
                elif line.startswith("do"):
                    eval(line[3:], self.scope)
                elif line.startswith("if") and line.endswith("{"):
                    condition = bool(eval(" ".join(line.split(" ")[1:-1]), self.scope))
                    true_lines, rest = findBloc(self.lines)
                    false_exists = rest.startswith("}") and "else" in rest and line.endswith("{")
                    if false_exists:
                        false_lines, _ = findBloc(self.lines)

                    if condition:
                        Executer.run(Block(true_lines, self.scope))
                    elif false_exists:
                        Executer.run(Block(false_lines, self.scope))
                elif line == 'break':
                    self.scope["must_break"] = True
                else:
                    print(line)
            except Exception as e:
                raise Exception(f"{e}\nYou have an error in the line:\n{line}")


class Code:
    game: Game

    def __init__(self, type: str, lines: list[str]) -> None:
        if type == "BallGame":
            self.game = BallGame(640, 480)
        scope = self.game.objects
        scope["must_break"] = False
        scope["random"] = random
        Executer.add(Block(lines, scope))
        Executer.finalise()

    def execute(self) -> None:
        Executer.execute()


def compile(file_name: str) -> Code:
    with open(file_name, 'r') as f:
        file = f.read()
    _types = [line.split("type")[-1].strip() for line in file.splitlines() if line.startswith("type")]
    if len(_types) != 1:
        raise Exception("You have not defined the type corectly!")
    lines = [line.strip() for line in file.splitlines() if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("type")]
    code = Code(_types[0], lines)

    return code
