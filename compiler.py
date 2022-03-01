from __future__ import annotations
from ball_game import BallGame
from game import Game


class Executer:
    blocks: list[list[Block]] = [[]]

    @staticmethod
    def add(block: Block, frame: int = 0) -> None | Block:
        for _ in range(frame + 1 - len(Executer.blocks)):
            Executer.blocks.append([])
        Executer.blocks[frame].append(block)
        return block

    def execute() -> None:
        if not Executer.blocks:
            return
        while Executer.blocks[0]:
            block = Executer.blocks[0].pop(0)
            block.execute()
        Executer.blocks.pop(0)


class Block:
    def __init__(self, lines: list[str], scope: dict[str, object]) -> None:
        self.lines = lines
        self.scope = scope

    def execute(self) -> None:
        while self.lines:
            line = self.lines.pop(0)
            try:
                if line.startswith("wait") and line.endswith("frames"):
                    frames = int(line.split(' ')[1])
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
                    n = int(eval(line.split(" ")[1], self.scope))
                    lines = []
                    while True:
                        temp = self.lines.pop(0)
                        if temp == "}":
                            break
                        lines.append(temp)
                    Executer.add(Block(lines, self.scope.copy()), frame=n)
                elif "every" in line and "frames" in line and line.endswith("{"):
                    n = int(eval(line.split(" ")[1], self.scope))
                    lines = []
                    while True:
                        temp = self.lines.pop(0)
                        if temp == "}":
                            break
                        lines.append(temp)
                    temp = [l for l in lines]
                    lines.append(f"every {n} frames "+"{")
                    lines.extend(temp)
                    lines.append("}")
                    Executer.add(Block(lines, self.scope.copy()), frame=n)
                elif "loop" in line and "times" in line and line.endswith("{"):
                    n = int(eval(line.split(" ")[1], self.scope))
                    lines = []
                    while True:
                        temp = self.lines.pop(0)
                        if temp == "}":
                            break
                        lines.append(temp)
                    for _ in range(n):
                        Executer.add(Block(lines.copy(), self.scope))
                elif line.startswith("do"):
                    eval(line[3:], self.scope)
                else:
                    print(line, self.scope)
            except Exception as e:
                raise Exception(f"{e}\nYou have an error in the line:\n{line}")


class Code:
    game: Game

    def __init__(self, type: str, lines: list[str]) -> None:
        if type == "BallGame":
            self.game = BallGame(640, 480)
        Executer.add(Block(lines, self.game.objects))

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
