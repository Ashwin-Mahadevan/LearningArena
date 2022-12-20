from abc import ABC, abstractmethod
from collections import defaultdict
from itertools import count
from random import Random
from typing import Hashable

from blackjack import Blackjack, Environment, Shoe


class Agent(ABC):

    _ACTIONS: list[Hashable]
    _RNG: Random

    def __init__(self, actions: list[Hashable], rng: Random):
        """
        Note: Subclasses that override this method should begin by calling super().__init__
        """

        self._ACTIONS = actions
        self._RNG = rng

    @abstractmethod
    def select_action(self, state: Hashable) -> Hashable:
        ...


class CLIUserAgent(Agent):

    _PROMPT: str
    _ACTION_MAP: dict[str, Hashable]

    def __init__(self, rng: Random, prompt: str, action_map: dict[str, Hashable]):

        super().__init__(action_map.keys(), rng)

        self._PROMPT = prompt
        self._ACTION_MAP = action_map

    def select_action(self, state: Hashable) -> Hashable:

        while True:
            response = input(self._PROMPT)
            if response in self._ACTION_MAP:
                return self._ACTION_MAP[response]


class QAgent(Agent):

    _DISCOUNT: float
    exploration_rate: float
    learning_rate: float

    _Q: dict[tuple[Hashable, Hashable], float]

    def __init__(
        self,
        actions: list[Hashable],
        rng: Random,
        discount_factor: float = 1.0,
        exploration_rate: float = 0.1,
        learning_rate: float = 0.01,
    ):

        self._ACTIONS = actions
        self._RNG = rng

        self._DISCOUNT = discount_factor
        self.exploration_rate = exploration_rate
        self.learning_rate = learning_rate

        self._Q = defaultdict(lambda: 0)

    def select_action(self, state: Hashable) -> Hashable:

        if self._RNG.random() < self.exploration_rate:
            return self._RNG.choice(self._ACTIONS)

        return max(
            self._ACTIONS,
            key=lambda action: self._Q[state, action],
        )

    def update(
        self,
        prev_state: Hashable,
        prev_action: Hashable,
        reward: float,
        next_state: Hashable,
        next_action: Hashable,
    ):

        td_target = reward + self._DISCOUNT * self._Q[next_state, next_action]
        self._Q[prev_state, prev_action] += self.learning_rate * (td_target - self._Q[prev_state, prev_action])


def sample_episode(agent: Agent, env: Environment):

    env.reset()

    prev_state = 'START'
    prev_action = 'START'
    reward = 0

    while not env.is_finished():

        next_state = env.observe()
        next_action = agent.select_action(next_state)

        yield (prev_state, prev_action, reward, next_state, next_action)

        prev_state = next_state
        prev_action = next_action
        reward = env.step(prev_action)

    yield (prev_state, prev_action, reward, 'FINISHED', 'FINISHED')
