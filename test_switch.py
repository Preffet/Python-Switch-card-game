"""Test suit for the switch game"""
from copy import deepcopy
import switch

from cards import Card


class MockPlayer:
    """Mock player which deterministic behaviour"""
    is_ai = True

    def __init__(self, hand):
        self.name = "Mock player"
        self.hand = hand

    @staticmethod
    def select_card(choices, _):
        """Select a card to be discarded

        Returns cards in hand one after the other
        """
        return choices[0]

    @staticmethod
    def ask_for_swap(others):
        """Select a player to switch hands with

        Selects first player
        """
        return others[0]


def mock_setup_round(hands, stock, discards, **flags):
    """Set up a specific game state"""
    def str_to_cards(spec):
        return [Card(sv[:1], sv[1:]) for sv in spec.split()]

    game = switch.Switch()
    game.players = [MockPlayer(str_to_cards(hand)) for hand in hands]
    game.discards = str_to_cards(discards)
    game.stock = str_to_cards(stock)
    for flag, value in flags.items():
        setattr(game, flag, value)
    return game


def test_setup_round__resets_flags():
    """setup_round sets all flags to initial value"""
    game = switch.Switch()
    game.players = [MockPlayer([]), MockPlayer([])]
    game.setup_round()
    assert game.skip is False
    assert game.draw2 is False
    assert game.draw4 is False
    assert game.direction == 1


def test_setup_round__deals_cards():
    """setup_round deals correct number of cards"""
    game = switch.Switch()
    game.players = [MockPlayer([]), MockPlayer([])]
    game.setup_round()
    assert all(len(p.hand) == 7 for p in game.players)
    assert len(game.discards) == 1
    assert len(game.stock) == 52-len(game.players)*7-1


def test_pick_up_card__pick_correct_number():
    """pick_up_card picks up correct number of cards"""
    game = mock_setup_round(['♣4', '♣9'], '♠7 ♢8 ♠5 ♢6 ♢7', '♠5 ♢6 ♡3')
    player = game.players[0]
    picked = game.pick_up_card(player, 4)
    assert picked == 4
    assert len(player.hand) == 5
    assert len(game.stock) == 1

    picked = game.pick_up_card(player, 4)
    assert picked == 3
    assert len(player.hand) == 8
    assert len(game.stock) == 0


def test_can_discard__follows_suit():
    """all cards of the same suit can be discarded"""
    game = mock_setup_round([], '', '♣5')
    assert game.can_discard(Card('♣', '2'))
    assert game.can_discard(Card('♣', '3'))
    assert game.can_discard(Card('♣', '4'))
    assert game.can_discard(Card('♣', '6'))
    assert game.can_discard(Card('♣', '7'))
    assert game.can_discard(Card('♣', '8'))
    assert game.can_discard(Card('♣', '9'))
    assert game.can_discard(Card('♣', '10'))
    assert game.can_discard(Card('♣', 'J'))
    assert game.can_discard(Card('♣', 'K'))


def test_can_discard__follows_value():
    """all cards of the same value can be discarded"""
    game = mock_setup_round([], '', '♣5')
    assert game.can_discard(Card('♢', '5'))
    assert game.can_discard(Card('♡', '5'))
    assert game.can_discard(Card('♠', '5'))


def test_discard_card__sets_draw2():
    """discarding a two sets the draw2 flag"""
    game = mock_setup_round(['♣4 ♡2', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    game.discard_card(game.players[0], Card('♡', '2'))
    assert game.draw2


def test_discard_card__sets_draw4():
    """discarding a queen sets the draw4 flag"""
    game = mock_setup_round(['♣4 ♡Q', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    game.discard_card(game.players[0], Card('♡', 'Q'))
    assert game.draw4


def test_discard_card__sets_skip():
    """discarding an eight sets the skip flag"""
    game = mock_setup_round(['♣4 ♡8', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    game.discard_card(game.players[0], Card('♡', '8'))
    assert game.skip


def test_discard_card__reverses():
    """discarding a king reverses direction"""
    game = mock_setup_round(['♣4 ♡K', '♣K ♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    game.discard_card(game.players[0], Card('♡', 'K'))
    assert game.direction == -1
    game.discard_card(game.players[1], Card('♣', 'K'))
    assert game.direction == 1


def test_discard_card__swaps():
    """discarding a jack swaps hands"""
    game = mock_setup_round(['♣4 ♡J', '♣K ♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    game.discard_card(game.players[0], Card('♡', 'J'))
    assert game.players[0].hand == [Card('♣', 'K'), Card('♣', '9')]
    assert game.players[1].hand == [Card('♣', '4')]


def test_can_discard__allows_ace():
    """aces can always be discarded"""
    game = mock_setup_round([], '', '♣5')
    assert game.can_discard(Card('♢', 'A'))
    assert game.can_discard(Card('♡', 'A'))
    assert game.can_discard(Card('♠', 'A'))


def test_can_discard__allows_queen():
    """queens can always be discarded"""
    game = mock_setup_round([], '', '♣5')
    assert game.can_discard(Card('♢', 'Q'))
    assert game.can_discard(Card('♡', 'Q'))
    assert game.can_discard(Card('♠', 'Q'))


def test_get_normalized_hand_sizes():
    """test hand size normalization"""
    game = mock_setup_round(['♣4', '♣K ♣9', '♡J ♢5 ♢6'], '♢7 ♢8', '♡3')
    assert game.get_normalized_hand_sizes(game.players[0]) == [1, 2, 3]
    assert game.get_normalized_hand_sizes(game.players[1]) == [2, 3, 1]
    assert game.get_normalized_hand_sizes(game.players[2]) == [3, 1, 2]

    game = mock_setup_round(['♣4', '♣K ♣9', '♡J ♢5 ♢6'], '♢7 ♢8', '♡3', direction=-1)
    assert game.get_normalized_hand_sizes(game.players[0]) == [1, 3, 2]
    assert game.get_normalized_hand_sizes(game.players[1]) == [2, 1, 3]
    assert game.get_normalized_hand_sizes(game.players[2]) == [3, 2, 1]


def test_swap_hands():
    """Test swapping of hands"""
    game = mock_setup_round(['♣4', '♣K ♣9', '♡J ♢5 ♢6'], '♢7 ♢8', '♡3')
    game.swap_hands(game.players[1], game.players[2])
    assert len(game.players[1].hand) == 3
    assert len(game.players[2].hand) == 2


def test_run_player__returns_true_upon_win():
    """run_player returns True if player wins"""
    game = mock_setup_round(['♣4 ♣5', '♣9', '♣10'], '♣6 ♣7 ♣8', '♣3')
    player = game.players[0]
    assert not game.run_player(player)
    assert game.run_player(player)


def test_run_player__draws_card():
    """run_player forces pick up if no discard possible"""
    game = mock_setup_round(['♣4', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    player = game.players[0]
    game.run_player(player)
    assert len(player.hand) == 2
    assert len(game.stock) == 3
    assert len(game.discards) == 1


def test_run_player__draws_card_and_discards():
    """run_player discards drawn card if possible"""
    game = mock_setup_round(['♣4', '♣9'], '♢5 ♢6 ♢7 ♡8', '♡3')
    player = game.players[0]
    game.run_player(player)
    assert len(player.hand) == 1
    assert len(game.stock) == 3
    assert len(game.discards) == 2


def test_run_player__adheres_to_draw2_flag():
    """run_player adheres to switch.draw2"""
    game = mock_setup_round(['', ''], '♢5 ♣6 ♣7', '♢3', draw2=True)
    player = game.players[1]
    game.run_player(player)
    assert len(player.hand) == 2
    assert not game.draw2


def test_run_player__adheres_to_draw4_flag():
    """run_player adheres to switch.draw4"""
    game = mock_setup_round(['', ''], '♢5 ♣5 ♣6 ♣7 ♣8', '♢3', draw4=True)
    player = game.players[1]
    game.run_player(player)
    assert len(player.hand) == 4
    assert not game.draw4


def test_run_player__adheres_to_skip_flag():
    """run_player adheres to switch.skip"""
    game = mock_setup_round(['', '', ''], '', '♣3', skip=True)
    player = game.players[1]
    hand_before = deepcopy(player.hand)
    game.run_player(player)
    assert player.hand == hand_before
    assert not game.skip
