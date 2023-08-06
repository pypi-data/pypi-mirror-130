#import scratch
from functools import partial
from typing import Optional

def add_ints(a: int = None, b: int = None) -> Optional[int]:
    if a is not None and b is not None:
        return a + b
    return None

add_5 = partial(add_ints, 5)

print(add_5(10))


class Adder:
    def __init__(self, a:int = None, b:int = None) -> None:
        self.a = a
        self.b = b
        passed_args = {k: v for k, v in self.__dict__.items() if v is not None}
        self.add_ints = partial(add_ints, **passed_args)

print(add_ints(b=5, a=12))

