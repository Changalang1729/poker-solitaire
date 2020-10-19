import sys
import itertools

from treys import Card
from treys import Evaluator
from treys import Deck

from rules import *
from utils import lget

"""
HandRankings:
1. Royal Flush
2. Straight Flush
3. Four of a Kind
4. Full House
5. Flush
6. Straight
7. Three of a Kind
8. Two Pair
9. Pair
"""

POKER_HAND_EVALUATOR = Evaluator()


def isCorrectFlush(playerCards, upperBound):
    totalCombinations = list(itertools.combinations(playerCards, 5))
    for combination in totalCombinations:
        handStrength = POKER_HAND_EVALUATOR.evaluate(list(combination), [])
        if upperBound == 1609 and handStrength <= 815 and handStrength >= 323:
            return combination
        elif upperBound == handStrength and handStrength <= 10 and handStrength >= 1:
            return combination

    return None


def findFlushCombo(isStraight, isRoyal):
    playerCards, communityCards, deck = set(), set(), Deck()
    upperBound = 10 if isStraight else 1 if isRoyal else 815
    while (flushCombo := isCorrectFlush(playerCards, upperBound)) == None:
        card = deck.draw(1)
        playerCards.add(card)

    communityCards = playerCards - set(flushCombo)
    playerCards = set(flushCombo)

    return communityCards, playerCards


def isStraight(playerCards):
    totalCombinations = list(itertools.combinations(playerCards, 5))
    for combination in totalCombinations:
        handStrength = POKER_HAND_EVALUATOR.evaluate(list(combination), [])
        if handStrength >= 1 and handStrength <= 10:
            return combination
        elif handStrength >= 1600 and handStrength <= 1609:
            return combination

    return None


def findStraight():
    playerCards, communityCards, deck = set(), set(), Deck()
    while (straightCombo := isStraight(playerCards)) == None:
        card = deck.draw(1)
        playerCards.add(card)

    communityCards = playerCards - set(straightCombo)
    playerCards = set(straightCombo)

    return communityCards, playerCards