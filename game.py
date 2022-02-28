from __future__ import annotations
from game_object import GameObject
from screen import Screen


class Game:
    elements: dict[str, GameObject]
    
    def __init__(self, width: int, height: int) -> None:
        self.screen: Screen = Screen(width, height)
        self.create()

    def create(self) -> None:
        pass

    def draw(self, screen: Screen) -> None:
        pass

    def update(self) -> None:
        pass
