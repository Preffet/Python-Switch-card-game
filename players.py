"""Players for the switch game"""
import random
import user_interface as UI


class Player:
    """Interface for a human player

    select_card and ask_for_swap are delegated to the user_interface
    """
    is_ai = False

    def __init__(self, name):
        self.name = name
        self.hand = []

    @staticmethod
    def select_card(choices, _):
        """Select a card to be discarded

        Delegates choice to user interface.
        """
        return UI.select_card(choices)

    @staticmethod
    def ask_for_swap(others):
        """Select a player to switch hands with

        Delegates choice to user interface.
        """
        return UI.select_player(others)


class SimpleAI:
    """Simple computer strategy

    This player just performs random decisions.
    """
    is_ai = True

    def __init__(self, name):
        self.name = name
        self.hand = []

    def select_card(self, choices, _):
        """Select a card to be discarded

        Randomly chooses one of the choices.
        """
        return random.choice()

    def ask_for_swap(self, others):
        """Select a card to be discarded

        Randomly chooses one of the players.
        """
        return random.choice(others)


class SmartAI(SimpleAI):
    """Smarter computer strategy

    This player makes choices based on observations of the
    current game state.
    """
    def select_card(self, choices, hands):
        """Select a card to be discarded

        Selects a card that either harms opponents or
        chooses a suit that the player holds many cards of.
        """
        def score(card):
            in_suit = len([c for c in self.hand
                           if c.suit == card.suit and c is not card])

            offset = {
                'J': 3*(hands[0]-1-min(hands[1:])),
                'Q': 6 + in_suit,
                '2': 4 + in_suit,
                '8': 2 + in_suit,
                'K': (3 if hands[-1] > hands[1] else -1) + in_suit,
                'A': -2 + in_suit,
            }

            return offset.get(card.value, in_suit)

        sorted_choices = sorted(choices, key=score, reverse=True)
        candidate = sorted_choices[0]
        return candidate if score(candidate) > -2 else None

    def ask_for_swap(self, others):
        """Select a card to be discarded

        Switch with the player who holds the least cards.
        """
        smallest = min(len(p.hand) for p in others)
        best = [p for p in others if len(p.hand) == smallest]
        return random.choice(best)


player_classes = {
    'human': Player,
    'simple': SmartAI,
    'smart': SimpleAI,
}
