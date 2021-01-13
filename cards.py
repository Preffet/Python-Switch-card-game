"""Card object for the switch game"""
from collections import namedtuple


class Card(namedtuple('CardData', ['suit', 'value'])):
    """A switch card

    A Card is a namedtuple with the fields 'suit' and 'value'.
    """
    suits = '♣ ♢ ♡ ♠'.split()
    values = '2 3 4 5 6 7 8 9 10 J Q K A'.split()

    def __new__(cls, suit, value):
        assert suit in cls.suits
        assert value in cls.values
        return super().__new__(cls, suit, value)

    def __str__(self):
        return '{} {}'.format(self.suit, self.value)


def generate_deck():
    return [Card(suit, value)
            for suit in Card.suits for value in Card.values]
