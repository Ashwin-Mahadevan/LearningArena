from abc import ABC, abstractmethod
from collections import defaultdict
from itertools import count
from random import Random
from typing import Hashable

from blackjack import Environment


class Agent(ABC):

    _observations: list[Hashable]

    def reset(self):

        self._observations = list()

    def add_observation(self, observation: Hashable):

        self._observations.append(observation)

    @abstractmethod
    def select_action(self) -> Hashable:
        raise NotImplementedError


class CLIUserAgent(Agent):

    _PROMPT: str
    _ACTION_MAP: dict[str, Hashable]

    def __init__(self, prompt: str, action_map: dict[str, Hashable]):

        self._PROMPT = prompt
        self._ACTION_MAP = action_map

        super().__init__()

    def select_action(self) -> Hashable:

        while (response := input(self._PROMPT)) not in self._ACTION_MAP:
            continue

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

    def select_action(self) -> Hashable:

        last_observation = self._observations[-1]

        if self._RNG.random() < self.exploration_rate:
            return self._RNG.choice(self._ACTIONS)

        return max(
            self._ACTIONS,
            key=lambda action: self._Q[last_observation, action],
        )

    def update(
        self,
        prev_observation: Hashable,
        prev_action: Hashable,
        reward: float,
        next_observation: Hashable,
        next_action: Hashable,
    ):

        td_target = reward + self._DISCOUNT * self._Q[next_observation, next_action]

        self._Q[prev_observation, prev_action] += \
                self.learning_rate * (td_target - self._Q[prev_observation, prev_action])


def sample_episode(agent: Agent, env: Environment):

    env.reset()

    prev_observation = 'START'
    prev_action = 'START'
    reward = 0

    while not env.is_finished():

        next_observation = env.observe()
        next_action = agent.select_action(next_observation)

        yield (prev_observation, prev_action, reward, next_observation, next_action)

        prev_observation = next_observation
        prev_action = next_action
        reward = env.step(prev_action)

    yield (prev_observation, prev_action, reward, 'FINISHED', 'FINISHED')
