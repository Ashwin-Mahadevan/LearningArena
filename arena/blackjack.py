from random import Random

RANKS_TO_SCORE = {str(n): n for n in range(2, 11)} | {'J': 10, 'Q': 10, 'K': 10, 'A': 1}
RANKS = list(RANKS_TO_SCORE.keys())
DECK = 4 * RANKS

def _score(hand):
    
    score = sum(RANKS_TO_SCORE[card] for card in hand)

    if 'A' in hand and score <= 11:
        score += 10
    
    return score


class Shoe:

    num_drawn: int
    _cards: list

    _RNG: Random
    _NAIVE: bool

    def __init__(self, rng: Random, num_decks: int = 0):

        self._RNG = rng

        if num_decks == 0:

            self._NAIVE = True
            self._cards = list()

        else:

            self._NAIVE = False
            self._cards = DECK * num_decks

    def draw(self):

        if self._NAIVE:

            self._cards.append(self._RNG.choice(RANKS))

        card = self._cards[self.num_drawn]
        self.num_drawn += 1
        return card

    def reset(self):

        self.num_drawn = 0

        if self._NAIVE:

            self._cards.clear()

        else:

            self._RNG.shuffle(self._cards)

    @property
    def history(self):
        return self._cards[:self.num_drawn]


class Blackjack:

    _player_hand: list
    _dealer_hand: list

    _SHOE: Shoe

    def __init__(self, shoe: Shoe):

        self._SHOE = shoe
    
    def reset(self):

        self._player_hand = [self._SHOE.draw(), self._SHOE.draw()]
        self._dealer_hand = [self._SHOE.draw()]
    
    def step(self, action):

        if action == 'H':

            self._player_hand.append(self._SHOE.draw())

            if _score(self._player_hand) > 21:

                # TODO: Player busts.
                ...
            
            # TODO: Game continues, zero reward.
            ...
            
        
        if action == 'S':

            while _score(self._dealer_hand) < 17:  # TODO: Option for dealer hitting on soft 17.

                self._dealer_hand.append(self._SHOE.draw())
            
            if _score(self._dealer_hand) > 21:

                # TODO: Dealer busts.
                ...
            
            if _score(self._player_hand) > _score(self._dealer_hand):

                # TODO: Player wins.
                ...

            elif _score(self._dealer_hand) > _score(self._player_hand):

                # TODO: Dealer wins.
                ...
            
            else:

                # TODO: Tie.
                ...

            


