from random import Random
from typing import Callable, Collection, Hashable, NewType
from arena.types import AgentID
from env import Environment

Card = NewType('Card', str)

RANKS_TO_SCORE = {Card(str(n)): n for n in range(2, 11)} | {Card('J'): 10, Card('Q'): 10, Card('K'): 10, Card('A'): 1}
RANKS = list(RANKS_TO_SCORE.keys())
DECK = 4 * RANKS


def score(hand: Collection[Card]) -> int:

    score = sum(RANKS_TO_SCORE[c] for c in hand)

    if 'A' in hand and score <= 11:
        score += 10

    return score


def score_excluding_ace(hand: Collection[Card]) -> int:

    return sum(RANKS_TO_SCORE[c] for c in hand) - int('A' in hand)


class Blackjack(Environment):

    _hands: dict[Hashable, list[Card]]
    draw_fn: Callable[[], Card]

    def __init__(self, draw_fn: Callable[[], Card]):

        self._hands = dict()
        self.draw_fn = draw_fn

        super().__init__()

    def reset(self):

        assert len(self._agents) > 0

        self._finished = False
        self._hands.clear()

        for id in self._agents:
            self._hands[id] = [self.draw_fn(), self.draw_fn()]

    def is_finished(self) -> bool:

        return self._finished

    def _get_obs(self, id: AgentID):

        return (
            score_excluding_ace(self._hands[id]),
            bool(Card('A') in self._hands[id]),
            tuple(self._hands[other_id][0]
                  for other_id in self._agents
                  if other_id != id),  # First card in each other player's hand
        )

    def step(self):

        for id in self._agents:
            self._agents[id].add_observation(self._get_obs(id))

            # TODO: Process agent actions.