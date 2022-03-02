from __future__ import annotations
from ball_game import BallGame
from game import Game
from random import random
from utils import name, value, _matcher, clean, findBloc, BREAK, DONE


class Stack:
    def __init__(self) -> None:
        self.stack = []

    def add(self, block: Block, catch_break: bool = False) -> Stack:
        self.stack.append((block, catch_break))
        return self

    def run(self) -> Stack:
        if not self.stack:
            return None
        block, _ = self.stack.pop()
        return Executer.run(block)

    def catch_break(self) -> Stack:
        if not self.stack:
            return None
        block, catch_break = self.stack.pop()
        while not catch_break:
            if not self.stack:
                return None
            block, catch_break = self.stack.pop()
        return Executer.run(block)


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
        result = block.execute()
        if result == DONE:
            return block.stack.run()
        if result == BREAK:
            return block.stack.catch_break()
        return result

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

    def value(self, words: list[str], as_type: type = value) -> object:
        tmp = eval(" ".join(words), self.scope)
        if as_type != value:
            tmp = as_type(tmp)
        return tmp

    def value2(self, text: str, as_type: type = value) -> object:
        tmp = eval(text, self.scope)
        if as_type != value:
            tmp = as_type(tmp)
        return tmp

    def execute(self) -> Block | object:
        while self.lines:
            line = self.lines.pop(0)
            words = line.split(" ")
            _matches_ = []
            def match(*shape: str | type | list[type]): return _matcher(shape, _matches_, words, self.value2)
            def matches() -> object | list[object]: return clean(_matches_)

            try:
                if match("wait", [int], "frames"):
                    return Executer.add(self, matches())

                elif match("return", [value]):
                    return matches()

                elif match("break"):
                    return BREAK

                elif match("let", name, "be", [value]):
                    _name, _value = matches()
                    self.scope[_name] = _value

                elif match("set", name, "to", [value]):
                    part, _value = matches()
                    parts = part.split(".")
                    obj = self.scope[parts[0]]
                    for attribute in parts[1:-1]:
                        obj = obj.__getattribute__(attribute)
                    setter = parts[-1]
                    obj.__setattr__(setter, _value)

                elif match("after", [int], "frames", "{"):
                    n = matches()
                    lines, _ = findBloc(self.lines)
                    Executer.add(Block(lines, self.scope.copy(), Stack()), frame=n)

                elif match("every", [int], "frames", "{"):
                    n = matches()
                    lines, _ = findBloc(self.lines)
                    scope = self.scope.copy()
                    Executer.add(Block(lines, scope, Stack()), frame=n)  # frame=0, hvis man vil have den gør det første gang også
                    block = [f"every {n} frames "+"{", *(lines.copy()), "}"]
                    Executer.add(Block(block, scope, Stack()), frame=n)

                elif match("loop", [int], "times", "{"):
                    n = matches()
                    lines, _ = findBloc(self.lines)
                    if n > 0:
                        block = [*lines, f"loop {n-1} times "+"{", *lines, "}"]
                        return Executer.run(Block(block, self.scope, self.stack.add(self, catch_break=True)))

                elif match("loop", "{"):
                    lines, _ = findBloc(self.lines)
                    block = [*lines, "loop {", *lines, "}"]
                    return Executer.run(Block(block, self.scope, self.stack.add(self, catch_break=True)))

                elif match("do", [value]):
                    pass

                elif match("if", [bool], "{"):
                    condition = matches()
                    true_lines, rest = findBloc(self.lines)
                    false_exists = rest == "} else {"
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
