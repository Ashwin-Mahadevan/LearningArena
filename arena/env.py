


from abc import ABC, abstractmethod


class Environment(ABC):

    @abstractmethod
    def reset(self):
        ...

    @abstractmethod
    def is_finished(self) -> bool:
        ...

    @abstractmethod
    def observe(self):
        ...

    @abstractmethod
    def step(self, action: Hashable) -> float:
        ...
