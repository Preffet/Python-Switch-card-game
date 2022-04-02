![Badge tracking project size](https://img.shields.io/github/repo-size/Preffet/Python-switch-card-game?color=%2380006d)![Badge tracking code size](https://img.shields.io/github/languages/code-size/Preffet/Python-Switch-card-game?color=%235a0080)![Badge tracking last commit](https://img.shields.io/github/last-commit/Preffet/Python-switch-card-game?color=%23260080)

-----------------------------------------------------------------------------

![banner2](https://user-images.githubusercontent.com/84241003/161401729-d59858d4-167a-4a79-bdcd-9e50c6c5f49b.png)

-----------------------------------------------------------------------------
### Description

This is a text-based clone of the Switch card game.
Switch is a card game similar to the popular UNO game. The objective
of the game is to be the first player who managed to discard all his
or her cards. Some discards have consequences on the subsequent player
or mode of play.

-----------------------------------------------------------------------------
## Rules

Switch is played by 2-4 players. Each player is initially dealt a hand
of seven cards. The stock of remaining cards is put on the table face
down. One card is taken from the stock and placed face up to form the
discard pile.

Players take turns in discarding cards from their hand. In general,
a card can be discarded if it matches the top-most card of the discard
pile ("top card") in either suit (diamond, hearts, clubs, or spade) or
value. In addition, aces and queens can always be discarded, no matter
the current top card.

Some discards have special effects on the game flow:

| Card  | Discard Rule       | Effect                                                                  |
| :---: | ------------------ | ----------------------------------------------------------------------- |
| 2     | Same suit or value | Next player must draw two stock cards at the beginning of his turn      |
| 8     | Same suit or value | Next player is skipped and the turn proceeds with the subsequent player |
| J     | Same suit or value | The player must swap his hand with the hand of some other player        |
| Q     | Anytime            | Next player must draw four stock cards at the beginning of his turn     |
| K     | Same suit or value | The direction of game changes before the start of the next players turn |
| A     | Anytime            | None                                                                    |

If a player is not able to discard any card, he must draw a card from
the stock pile. If that card can be discarded, the player must do so
immediately, otherwise the card goes into the players hand and play
proceeds with the next player.

If there is no more card in the stock pile, all discards but the top
card are shuffled and placed face down to form a new stock pile.


-----------------------------------------------------------------------------
## Running the game

Start switch on the command line with

	$ python3 switch.py

Or press `Run` in your IDE.

Run the test suite with

	$ python3 -m pytest

The latter assumes that you have installed pytest using

    $ pip3 install pytest
    
-----------------------------------------------------------------------------

<h2 align="center"> Game preview </h2>

<p align="center">
  <img width="545" alt="Screenshot 1" src="https://user-images.githubusercontent.com/84241003/161402921-cb1e5e18-98c7-4368-87a4-7b0d25055b06.png">
</p>

<p align="center">
<img width="545" alt="Screenshot 2" src="https://user-images.githubusercontent.com/84241003/161402955-0ec35ee7-f439-405d-bf1e-3d892e154835.png">
</p>

-----------------------------------------------------------------------------
