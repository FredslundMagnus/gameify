from screen import Screen


class Game:
    def __init__(self, width: int, height: int) -> None:
        self.screen: Screen = Screen(width, height)
        self.create()

    def create(self) -> None:
        pass

    def draw(self, screen: Screen) -> None:
        pass

    def update(self) -> None:
        pass
