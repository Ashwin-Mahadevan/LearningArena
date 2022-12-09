from collections import defaultdict
from random import Random
from typing import Hashable


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

        self._Q = defaultdict(lambda: 0)

    def select_action(self, state: Hashable, training: bool = False) -> Hashable:

        if training and self._RNG.random() < self.exploration_rate:
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


def sample_generator(
        agent: QAgent,
        env: object,  # TODO: Environment type.
):
    while True:

        env.reset()

        next_state = None
        next_action = None

        while not env.is_finished():

            prev_action = next_action
            next_action = agent.select_action(next_state, training=True)

            reward = env.step(next_action)

            prev_state = next_state
            next_state = env.observe()

            yield (prev_state, prev_action, reward, next_state, next_action)
