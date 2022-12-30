from abc import ABC, abstractmethod
from random import Random

from arena.agents import Agent
from arena.types import AgentID


class Environment(ABC):
    """ Represents a multi-agent partially-observable Markov decision process. """

    _agents: dict[AgentID, Agent]

    def __init__(self):
        self._agents = dict()

    def add_agent(self, id: AgentID, agent: Agent):

        if id in self._agents:
            raise ValueError  # TODO: Add details to exception.

        self._agents[id] = agent

    @abstractmethod
    def reset(self):
        raise NotImplementedError

    @abstractmethod
    def step(self):
        raise NotImplementedError

    @abstractmethod
    def is_finished(self) -> bool:
        raise NotImplementedError
