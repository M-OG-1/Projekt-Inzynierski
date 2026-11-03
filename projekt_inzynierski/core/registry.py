from types import NoneType
from typing import TypeVar, Generic

T = TypeVar('T')

class Registry(Generic[T]):
    def __init__(self):
        self.values = {}
        self.values_inv = {}

    def register(self, name: str, value: T):
        self.values[name] = value
        self.values_inv[value] = name

    def get(self, name: str) -> T | NoneType:
        if name in self.values.keys():
            return self.values[name]
        return None

    def get_id(self, value: T) -> str | NoneType:
        if value in self.values_inv:
            return self.values_inv[value]
        return None

    def get_values(self) -> list[T]:
        return [v for v in self.values.values()]

    def get_keys(self) -> list[str]:
        return [k for k in self.values.keys()]


