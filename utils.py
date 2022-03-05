from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar


@dataclass
class XandY:
    x: float
    y: float


class name:
    pass


class value:
    pass


def _matcher(shape: list[str | type | list[type]], _matches_: list[object], words: list[str], valuefy) -> bool:
    temp = []
    for i in range(len(words)):
        if len(shape) <= i:
            return False
        _type = type(shape[i])
        if _type == str and shape[i] != words[i]:
            return False
        elif _type == list:
            break
        elif _type == type:
            if shape[i] == name:
                temp.append(words[i])
            else:
                temp.append(valuefy(words[i], shape[i]))
    else:  # no list
        if len(words) != len(shape):
            return False
        _matches_.extend(temp)
        return True

    # In case there was a list
    temp2 = []
    for j in range(1, len(words)+1):
        if len(shape) < j:
            return False
        _type = type(shape[-j])
        if _type == str and shape[-j] != words[-j]:
            return False
        elif _type == type:
            if shape[-j] == name:
                temp2.append(words[-j])
            else:
                temp2.append(valuefy(words[-j], shape[-j]))
        elif _type == list:
            element = shape[-j][0]
            string = " ".join(words[i:-j+1] if j > 1 else words[i:])
            if element == name:
                temp2.append(string)
            else:
                temp2.append(valuefy(string, element))

            _matches_.extend(temp + list(reversed(temp2)))
            return True


_matcher


def clean(li: list[object]) -> list[object] | object:
    if len(li) == 0:
        raise Exception("You have no values to get")
    return li[0] if len(li) == 1 else li


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


class BREAK:
    pass


class CONTINUE:
    pass


class DONE:
    pass


class Position:
    def __init__(self, position: tuple[int, int]) -> None:
        self.position = position

    def __hash__(self):
        return self.position.__hash__()

    def __eq__(self, __o: object) -> bool:
        return __o.__hash__() == self.__hash__()

    @property
    def left(self) -> Position:
        return Position((self.position[0]-1, self.position[1]))

    @property
    def right(self) -> Position:
        return Position((self.position[0]+1, self.position[1]))

    @property
    def up(self) -> Position:
        return Position((self.position[0], self.position[1]-1))

    @property
    def down(self) -> Position:
        return Position((self.position[0], self.position[1]+1))

    def __repr__(self) -> str:
        return str((self.position[0], 12-self.position[1]))


X = TypeVar('X')


class Observable(Generic[X]):
    def __init__(self, value: X, on_change: Callable[[X], None] | None = None) -> None:
        self._value: X = value
        if on_change != None:
            self.on_change = on_change

    @property
    def value(self) -> X:
        return self.value

    def on_change(self, new_value: X) -> None:
        pass

    @value.setter
    def value(self, new_value: X):
        self._value = new_value
        self.on_change(new_value)
