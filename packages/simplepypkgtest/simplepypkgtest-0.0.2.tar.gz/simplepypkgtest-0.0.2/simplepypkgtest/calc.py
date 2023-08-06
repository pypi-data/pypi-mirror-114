from typing import TypeVar

addible = TypeVar("T", str, int, float)

def add(a: addible, b: addible) -> addible:
    return a + b

