from screen import Screen


class Game:
    def __init__(self, width: int, height: int) -> None:
        self.screen: Screen = Screen(width, height)

    def draw(self, screen: Screen) -> None:
        pass
