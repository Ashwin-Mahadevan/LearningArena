from collections import defaultdict
from itertools import count
from random import Random
from typing import Hashable

from arena.blackjack import Environment


class QAgent:

    discount_factor: float
    exploration_rate: float
    learning_rate: float

    _ACTIONS: list[Hashable]
    _Q: dict[tuple[Hashable, Hashable], float]

    _RNG: Random

    def __init__(
        self,
        actions: list[Hashable],
        rng: Random,
        discount_factor: float = 1,
        exploration_rate: float = 0.1,
        learning_rate: float = 0.01,
    ):

        self._ACTIONS = actions
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.learning_rate = learning_rate

        self._RNG = rng

        self._Q = defaultdict(lambda: float('-inf'))

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

        td_target = reward + self.discount_factor * self._Q[next_state, next_action]
        self._Q[prev_state, prev_action] += self.learning_rate * (td_target - self._Q[prev_state, prev_action])


def sample_episode(agent: QAgent, env: Environment):

    env.reset()

    next_state = 'START'
    next_action = 'START'

    while not env.is_finished():

        prev_state = next_state
        prev_action = next_action

        reward = env.step(prev_action)

        next_state = env.observe()
        next_action = agent.select_action(next_state, training=True)

        yield (prev_state, prev_action, reward, next_state, next_action)

def sample_episodes(
    agent: QAgent,  # TODO: Generic agent type.
    env: Environment,  # TODO: Environment type.
    num_episodes: int,
):
    if num_episodes > 0:
        episode_iterator = range(num_episodes)
    else:
        episode_iterator = count()

    for episode_idx in episode_iterator:
        
        yield from sample_episode(agent, env)


