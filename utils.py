from __future__ import annotations
from dataclasses import dataclass


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


class DONE:
    pass
