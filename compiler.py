from __future__ import annotations
from ball_game import BallGame
from game import Game
from random import random
from utils import name, value, _matcher, clean, findBloc, BREAK, DONE


class Function:
    def __init__(self, name: str, parameters: list[str], lines: list[str], scope: dict[str, object]) -> None:
        self.name = name
        self.parameters = parameters
        self.lines = lines
        self.scope = scope
        self.scope[self.name] = self

    def __call__(self, *args: object) -> object:
        if len(args) != len(self.parameters):
            raise Exception("You used a wrong number of arguments!")
        for _name, _value in zip(self.parameters, args):
            self.scope[_name] = _value
        return Executer.run(Block(self.lines.copy(), self.scope.copy(), Stack()))


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


class Future:
    def __init__(self) -> None:
        self._value = ...

    def __repr__(self) -> str:
        return f"Future(done={self.isDone}{', value='+str(self.value) if self.value != ... else ''})"

    @property
    def value(self) -> object:
        if self._value is ...:
            return ...
        if type(self._value) is Future:
            return self._value._value
        return self._value

    @property
    def done(self) -> bool:
        return self.isDone

    @property
    def isDone(self) -> bool:
        if self._value is ...:
            return False
        if type(self._value) is Future:
            return self._value.isDone
        return True


class Executer:
    blocks: list[list[Block]] = [[]]
    temp: list[tuple[Block, int]] = []

    @staticmethod
    def add(block: Block, frame: int = 0) -> Block:
        for _ in range(frame + 1 - len(Executer.blocks)):
            Executer.blocks.append([])
        Executer.blocks[frame].append(block)
        if block.future is None:
            block.future = Future()
        # print(Executer.blocks)
        return block.future

    @staticmethod
    def run(block: Block) -> Block | object:
        _future = block.future
        result = block.execute()
        if result == DONE:
            _value = block.stack.run()
        elif result == BREAK:
            _value = block.stack.catch_break()
        else:
            _value = result
        if _future is not None:
            _future._value = _value
        return _value

    @staticmethod
    def execute() -> None:
        if not Executer.blocks:
            return
        while Executer.blocks[0]:
            block = Executer.blocks[0].pop(0)
            _future = block.future
            result = block.execute()

            if _future is not None:
                if _future is not result:
                    _future._value = result

            # return result
        Executer.blocks.pop(0)


class Block:
    def __init__(self, lines: list[str], scope: dict[str, object], stack: Stack) -> None:
        self.lines = lines
        self.scope = scope
        self.stack = stack
        self.future: None | Future = None

    def __repr__(self) -> str:
        return f"Block(future={self.future}, lines={self.lines})"
        # return f"Block(lines={self.lines}, stack={self.stack})"

    def value(self, text: str, as_type: type = value) -> object:
        tmp = eval(text, self.scope)
        if as_type != value:
            tmp = as_type(tmp)
        return tmp

    def execute(self) -> Block | object:
        while self.lines:
            line = self.lines.pop(0)
            words = line.split(" ")
            _matches_ = []
            def match(*shape: str | type | list[type]): return _matcher(shape, _matches_, words, self.value)
            def matches() -> object | list[object]: return clean(_matches_)

            try:
                if match("wait", [int], "frames"):
                    return Executer.add(self, matches())

                elif match("return", [value]):
                    return matches()

                elif match("return"):
                    return None

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

                elif match("make", [name], "{"):
                    temp: tuple[str, str] = matches()[:-1].split("(")
                    _name, _parameters = temp
                    parameters = _parameters.replace(" ", "").split(",")
                    if parameters == [""]:
                        parameters = []
                    lines, _ = findBloc(self.lines)
                    self.scope[_name] = Function(_name, parameters, lines, self.scope.copy())

                elif match("await", [name], "as", name):
                    _code, _name = matches()
                    self.lines.insert(0, f"await {_name}")
                    self.lines.insert(0, f"let {_name} be {_code}")

                elif match("await", [name]):
                    _name = matches()
                    _future = self.value(_name)
                    if _future.isDone:
                        self.scope[_name] = _future.value
                    else:
                        self.lines.insert(0, f"await {_name}")
                        self.lines.insert(0, f"wait 1 frames")

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
        Executer.run(Block(lines, scope, Stack()))

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
