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


class Poker:
    def __init__(self, strategy=None, desiredCards=None):
        self.strategy = strategy
        self.desiredCards = desiredCards
        self.POKER_HAND_EVALUATOR = Evaluator()

    def isTypeOfCard(self, card):
        for desiredCard in self.desiredCards:
            if desiredCard in card:
                self.desiredCards.remove(desiredCard)
                return True
        return False

    def simulatePokerStrategy(self):
        playerCards, communityCards, deck = set(), set(), Deck()
        while (desiredCombo := self.isDesiredHand(communityCards)) == None:
            card = deck.draw(1)
            communityCards.add(card)

        communityCards -= set(desiredCombo)
        communityCards |= set(deck.draw(5 - len(communityCards)))
        playerCards = desiredCombo

        return playerCards, communityCards

    def isDesiredHand(self, playerCards):
        return (
            self.isDesiredHandGeneral(playerCards)
            if self.desiredCards
            else self.isDesiredHandStrategy(playerCards)
        )

    def isDesiredHandGeneral(self, playerCards):
        playerDesiredCards = []

        if len(playerCards) < 5:
            return None

        for card in playerCards:
            stringCardDrawn = Card.print_pretty_card(card)
            if self.isTypeOfCard(stringCardDrawn, self.desiredCards):
                playerDesiredCards.append(card)

        if len(playerDesiredCards) >= 5:
            return playerCards

        return None

    # tech debt, should be done with polymorphism instead
    def isDesiredHandStrategy(self, playerCards):
        allSatisfiedHands, strongestComboIndex = [], 0

        handRankingsUpperBoundsForStrats = {
            "straight": (1609, 1600),
            "flush": (1599, 323),
            "pair": (6185, 3326),
            "two-pair": (3325, 2468),
            "trips": (2467, 1610),
            "boat": (322, 167),
            "quads": (166, 11),
            "royal": (1, 1),
            "straight-flush": (10, 1),
        }

        lowerBound, upperBound = handRankingsUpperBoundsForStrats[self.strategy]

        totalCombinations = list(itertools.combinations(playerCards, 5))
        for combination in totalCombinations:
            handStrength = self.POKER_HAND_EVALUATOR.evaluate(list(combination), [])
            if handStrength <= upperBound and handStrength >= lowerBound:
                allSatisfiedHands.append(combination)

        if allSatisfiedHands:
            (_, strongestComboIndex) = max(
                (self.POKER_HAND_EVALUATOR.evaluate(list(satisfiedHand), []), i)
                for i, satisfiedHand in enumerate(allSatisfiedHands)
            )

        return lget(allSatisfiedHands, strongestComboIndex)

    def isPlayerHandBetter(self, playerCards, communityCards):
        if not playerCards or not communityCards:
            print("ERROR: NO PLAYER CARDS OR NO COMMUNITY CARDS")

        playerHandStrength = self.POKER_HAND_EVALUATOR.evaluate(playerCards, [])
        totalCombinations = list(itertools.combinations(communityCards, 5))
        (communityHandStrength, communityHandComboIndex) = min(
            (self.POKER_HAND_EVALUATOR.evaluate(list(combination), []), index)
            for index, combination in enumerate(totalCombinations)
        )

        return (
            playerHandStrength <= communityHandStrength,
            totalCombinations[communityHandComboIndex],
        )
