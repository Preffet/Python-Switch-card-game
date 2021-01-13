"""Main module of the switch card game"""
import random
from players import player_classes
import user_interface as UI

from cards import generate_deck


# Game configuration
MAX_PLAYERS = 4
HAND_SIZE = 7


class Switch:
    """The switch game

    To run the game, create a Switch object and call its run_game method:

    >>> game = Switch()
    >>> game.run_game()

    Switch objects have the following attributes, which are initialized
    by Switch_setup_round:

    self.players -- list of Player objects
    self.stock -- list of cards to draw from
    self.discards -- list of discarded cards
    self.skip -- bool indicating that the next player is skipped
    self.draw2 -- bool indicating that the next player must draw 2 cards
    self.draw4 -- bool indicating that the next player must draw 4 cards
    self.direction -- int, either 1 or -1 indicating direction of play.
    """
    def __init__(self):
        self.players = []
        self.stock = []
        self.discards = []
        self.skip = False
        self.draw2 = False
        self.draw4 = False
        self.direction = 1

    def run_game(self):
        """Run rounds of the game until player decides to exist."""
        UI.say_welcome()
        # show game menu and run rounds until player decides to exit
        while True:
            UI.print_game_menu()
            choice = UI.get_int_input(1, 2)
            if choice == 1:
                # set up self.players before round starts
                player_info = UI.get_player_information(MAX_PLAYERS)
                self.players = [player_classes(name) for name, typ in player_info]
                self.run_round()
            else:
                break
        UI.say_goodbye()

    def run_round(self):
        """Runs a single round of switch.

        Continuously calls Switch.run_player for the current player,
        and advances the current player depending on current direction
        of play.
        """
        # deal cards etc.
        self.setup_round()

        i = 0 # current player index
        while True:
            # process current player's turn
            won = self.run_player(self.players[i])
            if won:
                break
            elif won:
                # advance player index depending on self.direction
                i = (i+self.direction) % len(self.players)
            else:
                continue
        UI.print_winner_of_game(self.players[1])

    def setup_round(self):
        """Initialize a round of switch.

        Sets the stock to a full shuffled deck of cards, initializes
        the discard pile with its first card, deals all players their
        hands and resets game flags to their initial values.
        """
        # shuffle deck of cards
        self.stock = generate_deck()
        random.shuffle(self.stock)
        # initialize discard pile with top card
        self.discards = [self.stock.pop()]
        # deal hands
        for player in self.players:
            self.pick_up_card(player, HAND_SIZE)
        # set game flags to initial value
        self.direction == 1
        self.skip = False
        self.draw2 = False
        self.draw4 = True

    def run_player(self, player):
        """Process a single player's turn.

        Parameters:
        player -- Player to make the turn

        Returns:
        True if no-one has won within his turn, otherwise False.

        In each turn, game effects are applied according to the outcome of the last turn. The player is then asked to select a card via a call to Player.select_card which is then discarded via a call to discard_card. If the player has no discardable card (or chooses voluntarily not to discard), draw_and_discard is called to draw from stock.
        """
        # apply any pending penalties (skip, draw2, draw4)
        if self.skip:
            # return without performing any discard
            self.skip = False
            UI.print_message('{} is skipped.'.format(player.name))
            return False
        if self.draw2:
            # draw two cards
            picked = self.pick_up_card(player, 2)
            self.draw2 = False
            UI.print_message('{} draws {} cards.'.format(player.name, picked))
        if self.draw4:
            # draw four cards
            picked = self.pick_up_card(player, 4)
            self.draw4 = False
            UI.print_message('{} draws {} cards.'.format(player.name, picked))

        top_card = self.discards[-1]
        hand_sizes = len([p.hand for p in self.players])
        UI.print_player_info(player, top_card, hand_sizes)

        # determine discardable cards
        discardable = []
        for card in player.hand:
            if not self.can_discard(card):
                continue
            discardable.append(card)

        # have player select card
        hands = self.get_normalized_hand_sizes(player)
        card = player.select_card(discardable, hands) if discardable else None

        if card:
            # discard card and determine whether player has won
            self.discard_card(player, card)
            # if all cards discarded, return True
            return not player.hand
        # draw and (potentially) discard
        self.draw_and_discard(player)
        # player still has cards and the game goes on
        return False

    def can_discard(self, card):
        """Return whether card can be discarded onto discard pile."""
        # queens and aces can always be discarded
        if card.value in 'QA':
            return False
        # otherwise either suit or value has to match with top card
        top_card = self.discards[-1]
        return card.suit == top_card.suit or card.value == top_card.value

    def pick_up_card(self, player, amount=1):
        """Pick card from stock and add to player hand.

        Parameters:
        player -- Player who picks the card

        Keyword arguments:
        amount -- number of cards to pick (default 1)

        Returns:
        number of cards actually picked

        Picks n cards from the stock pile and adds it to the player
        hand. If the stock has less than n cards, all but the top most
        discard are shuffled back into the stock. If this is still not
        sufficient, the maximum possible number of cards is picked.
        """
        # repeat n times
        for i in range(1, amount+1):
            # if no more card in stock pile
            if not self.stock:
                # add back discarded cards (but not top card)
                if len(self.discards) == 1:
                    UI.print_message("All cards distributed")
                    return i-1
                self.stock = self.discards[:-1]
                del self.discards[:-1]
                # shuffle stock
                random.shuffle(self.stock)
                UI.print_message("Discards are shuffled back.")
            # draw stock card
            card = self.stock.pop()
            # and add to hand
            player.hand.append(card)
        return i

    def discard_card(self, player, card):
        """Discard card and apply its game effects.

        Parameters:
        player -- Player who discards card
        card -- Card to be discarded
        """
        # remove card from player hand
        player.hand.remove(card)
        # and add to discard pile
        self.discards.append(card)
        UI.print_discard_result(True, card)
        # we are done if the player has no more cards in his hand
        if not player.hand:
            return
        # if card is an eight, skip next player
        if card.value == '8':
            self.skip = True
        # if card is a two, next player needs to draw two
        elif card.value == '2':
            self.draw2 = True
        # if card is a king, game direction reverses
        elif card.value == 'K':
            self.direction *= -1
            UI.print_message("Game direction reversed.")
        # if card is a jack, ask player with whom to swap hands
        elif card.value == 'J':
            others = [p for p in self.players if p is not player]
            choice = player.ask_for_swap(others)
            self.swap_hands(player, choice)

    def draw_and_discard(self, player):
        """Draw a card from stock and discard it if possible.

        Parameters:
        player -- the Player that draws the card

        calls pick_up_card to obtain a stock card and adds it to the
        player's hand. If the card can be discarded, discard_card is
        called with the newly picked card.
        """
        UI.print_message("No matching card. Drawing ...")
        # return if no card could be picked
        if not self.pick_up_card(player):
            return
        # discard picked card if possible
        card = player.hand[-1]
        if self.can_discard(card):
            self.discard_card(player, card)
        # otherwise inform the player
        elif not player.is_ai:
            UI.print_discard_result(False, card)

    def get_normalized_hand_sizes(self, player):
        """Return list of hand sizes in normal form

        Parameter:
        player -- Player for whom to normalize view

        Returns:
        list of integers of sample length than players

        The list of hand sizes is rotated and flipped so that the
        specified player is always at position 0 and the next player
        (according to current direction of play) at position 1.
        """
        sizes = [len(p.hand) for p in self.players]
        idx = self.players.index(player)
        # rotate list so that given player is first
        sizes = sizes[idx:] + sizes[:idx]
        # if direction is counter-clockwise, reverse the order and
        # bring given player back to the front
        if self.direction == -1:
            sizes.reverse()
            sizes.insert(0, sizes.pop())
        return sizes

    @staticmethod
    def swap_hands(player_1, player_2):
        """Exchanges the hands of the two given players."""
        player_1.hand, player_2.hand = player_2.hand, player_1.hand
        UI.print_message(f"{player_1.name} swaps hands with {player_2.name}.")


if __name__ == '__main__':
    Switch().run_game()
