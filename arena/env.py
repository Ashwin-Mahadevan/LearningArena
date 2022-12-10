


from abc import ABC, abstractmethod
from typing import Hashable


class Environment(ABC):

    @abstractmethod
    def reset(self):
        ...

    @abstractmethod
    def is_finished(self) -> bool:
        ...

    @abstractmethod
    def observe(self) -> Hashable:
        ...

    @abstractmethod
    def step(self, action: Hashable) -> float:
        ...
