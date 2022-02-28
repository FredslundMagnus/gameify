from __future__ import annotations
from ball_game import BallGame, Ball, Platform
from game import Game


class Code:
    game: Game

    def __init__(self, type: str, lines: list[str]) -> None:
        if type == "BallGame":
            self.game = BallGame(640, 480)
        self.lines = lines
        self.frame = 0
        self.next = 0
        self.elements = {}
        self.game.objects = self.elements

    def execute(self) -> None:
        if self.frame == self.next:
            while self.lines:
                line, self.lines = self.lines[0], self.lines[1:]
                try:
                    if line.startswith("wait") and line.endswith("frames"):
                        frames = int(line.split(' ')[1])
                        self.next += frames
                        break
                    elif "let" in line and "be" in line:
                        _, name, _, *values = line.split(" ")
                        value = eval(" ".join(values), self.game.elements)
                        self.elements[name] = value
                    elif "set" in line and "to" in line:
                        _, part, _, _value = line.split(" ")
                        value = float(_value)
                        parts = part.split(".")
                        obj = self.elements[parts[0]]
                        for attribute in parts[1:-1]:
                            obj = obj.__getattribute__(attribute)
                        setter = parts[-1]
                        obj.__setattr__(setter, value)
                    else:
                        print(self.frame, line)
                except Exception as e:
                    raise Exception(f"{e}\nYou have an error in the line:\n{line}")
        self.frame += 1
        if self.frame > self.next:
            self.next = self.frame


def compile(file_name: str) -> Code:
    with open(file_name, 'r') as f:
        file = f.read()
    _types = [line.split("type")[-1].strip() for line in file.splitlines() if line.startswith("type")]
    if len(_types) != 1:
        raise Exception("You have not defined the type corectly!")
    lines = [line.strip() for line in file.splitlines() if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("type")]
    code = Code(_types[0], lines)

    return code
