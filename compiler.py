from __future__ import annotations
from ball_game import BallGame
from game import Game
from random import random

must_break = "must break"
return_value = "return value"
block_not_executed = (..., ...)
DONE = (...,)


class Stack:
    def __init__(self) -> None:
        self.stack = []

    def add(self, block: Block) -> Stack:
        self.stack.append(block)
        return self

    def run(self) -> Stack:
        if not self.stack:
            return None
        block = self.stack.pop()
        return Executer.run(block)


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
    def add(block: Block, frame: int = 0) -> Block:
        for _ in range(frame + 1 - len(Executer.blocks)):
            Executer.blocks.append([])
        Executer.blocks[frame].append(block)
        return block

    @staticmethod
    def run(block: Block) -> Block | object:
        block.next = block.execute()
        if block.next == DONE:
            return block.stack.run()
        return block.next

    @staticmethod
    def execute() -> None:
        if not Executer.blocks:
            return
        while Executer.blocks[0]:
            block = Executer.blocks[0].pop(0)
            block.execute()
        Executer.blocks.pop(0)


class Block:
    def __init__(self, lines: list[str], scope: dict[str, object], stack: Stack) -> None:
        self.lines = lines
        self.scope = scope
        self.stack = stack
        self.next: Block | object = block_not_executed

    def value(self, words: list[str], as_type: type = ...) -> object:
        tmp = eval(" ".join(words), self.scope)
        if as_type != ...:
            tmp = as_type(tmp)
        return tmp

    def execute(self) -> Block | object:
        while self.lines and not self.scope[must_break]:
            line = self.lines.pop(0)
            words = line.split(" ")
            try:
                if words[0] == "wait" and words[-1] == "frames":
                    frames = self.value(words[1:-1], int)
                    return Executer.add(self, frames)

                elif words[0] == "return":
                    return self.value(words[1:])

                elif words[0] == 'break':
                    return None

                elif words[0] == "let" and words[2] == "be":
                    _, name, _, *values = words
                    value = eval(" ".join(values), self.scope)
                    self.scope[name] = value

                elif words[0] == "set" and words[2] == "to":
                    _, part, _, *values = words
                    value = eval(" ".join(values), self.scope)
                    parts = part.split(".")
                    obj = self.scope[parts[0]]
                    for attribute in parts[1:-1]:
                        obj = obj.__getattribute__(attribute)
                    setter = parts[-1]
                    obj.__setattr__(setter, value)

                elif words[0] == "after" and words[-2] == "frames" and words[-1] == "{":
                    n = int(eval(" ".join(words[1:-2]), self.scope))
                    lines, _ = findBloc(self.lines)
                    Executer.add(Block(lines, self.scope.copy(), Stack()), frame=n)

                elif words[0] == "every" and words[-2] == "frames" and words[-1] == "{":
                    n = self.value(words[1:-2], int)
                    lines, _ = findBloc(self.lines)
                    scope = self.scope.copy()
                    Executer.add(Block(lines, scope, Stack()), frame=n)  # frame=0, hvis man vil have den gør det første gang også
                    block = [f"every {n} frames "+"{", *(lines.copy()), "}"]
                    Executer.add(Block(block, scope, Stack()), frame=n)

                elif words[0] == "loop" and words[-2] == "times" and words[-1] == "{":
                    n = self.value(words[1:-2], int)
                    lines, _ = findBloc(self.lines)
                    if n > 0:
                        block = [*lines, f"loop {n-1} times "+"{", *lines, "}"]
                        return Executer.run(Block(lines, self.scope, self.stack.add(self)))

                elif words[0] == "loop" and words[1] == "{":
                    lines, _ = findBloc(self.lines)
                    block = [*lines, "loop {", *lines, "}"]
                    return Executer.run(Block(lines, self.scope, self.stack.add(self)))

                elif words[0] == "do":
                    self.value(words[1:])

                elif words[0] == "if" and words[-1] == "{":
                    condition = self.value(words[1:-1], bool)
                    true_lines, rest = findBloc(self.lines)
                    false_exists = rest.startswith("}") and "else" in rest and line.endswith("{")
                    if false_exists:
                        false_lines, _ = findBloc(self.lines)
                    if condition:
                        return Executer.run(Block(true_lines, self.scope, self.stack.add(self)))
                    elif false_exists:
                        return Executer.run(Block(false_lines, self.scope, self.stack.add(self)))

                else:
                    print(line)

            except Exception as e:
                raise Exception(f"{e}\nYou have an error in the line:\n{line}")
        return DONE


class Code:
    game: Game

    def __init__(self, type: str, lines: list[str]) -> None:
        if type == "BallGame":
            self.game = BallGame(640, 480)
        scope = self.game.objects
        scope[must_break] = False
        scope[return_value] = block_not_executed
        scope["random"] = random
        Executer.add(Block(lines, scope, Stack()))

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
