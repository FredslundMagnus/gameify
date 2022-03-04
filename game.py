from __future__ import annotations
from game_object import GameObject
from screen import Screen


class Game:
    types: list[type]
    objects: dict[str, object]

    def __init__(self, width: int, height: int) -> None:
        self.objects = {_type.__name__: _type for _type in self.types}
        self.screen: Screen = Screen(width, height)
        self.create(self.screen)

    def create(self, screen: Screen) -> None:
        pass

    def draw(self, screen: Screen) -> None:
        pass

    def update(self) -> None:
        pass
