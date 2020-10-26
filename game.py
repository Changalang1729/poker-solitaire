from treys import Evaluator
from treys import Card
from treys import Deck
from utils import lget

import itertools


class Poker:
    def __init__(self, strategy=None, desiredCards=None):
        self.strategy = strategy
        self.desiredCards = (
            [
                Card.print_pretty_card(Card.new(card)) if len(card) > 1 else card
                for card in desiredCards
            ]
            if desiredCards
            else None
        )
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

        return list(playerCards), list(communityCards)

    def simulatePokerGeneral(self):
        playerCards, communityCards, deck = [], [], Deck()
        while len(playerCards) != 5 or len(communityCards) < 5:
            card = deck.draw(1)
            if len(playerCards) != 5:
                stringCardDrawn = Card.print_pretty_card(card)
                if self.isTypeOfCard(stringCardDrawn):
                    playerCards.append(card)
                else:
                    communityCards.append(card)

        return playerCards, communityCards

    # tech debt, should be done with polymorphism instead
    def isDesiredHand(self, playerCards):
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
            if handStrength >= upperBound and handStrength <= lowerBound:
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

    def playPoker(self):
        if self.desiredCards and self.strategy:
            print("ERROR: WE CANNOT HAVE BOTH A STRATEGY AND DESIRED CARDS")
        playerCards, communityCards = (
            self.simulatePokerGeneral()
            if self.desiredCards
            else self.simulatePokerStrategy()
        )
        playerWin, bestCommunityCombination = self.isPlayerHandBetter(
            playerCards, communityCards
        )
        return (
            playerWin,
            Card.print_pretty_cards(playerCards),
            Card.print_pretty_cards(communityCards),
            Card.print_pretty_cards(bestCommunityCombination),
        )


"""
poker = Poker(strategy= 'royal')
poker.desiredCards
poker.strategy --> 'royal'
poker.playPoker() -->
(True,
 ' [T♠],[J♠],[Q♠],[K♠],[A♠] ',
 ' [2♥],[3♦],[2♦],[4♠],[3♣],[5♠],[5♦],[4♦],[5♥],[5♣],[6♠],[7♥],[4♣],[2♣],[6♦],[8♣],[8♥],[9♠],[8♠],[8♦],[9♦],[T♣],[T♥],[9♣],[9♥],[J♦],[Q♣],[Q♥],[Q♦],[K♣],[K♥],[A♦],[A♣],[A♥],[4♥],[6♥],[6♣],[7♦],[2♠] ',
 ' [7♥],[8♥],[T♥],[9♥],[6♥] ')
"""

"""
poker = Poker(desiredCards=['Th', 'A', 'K', 'Q', 'J'])
poker.desiredCards -->
['[T♥]', 'A', 'K', 'Q', 'J']
poker.strategy
poker.playPoker() --> 
(False,
 ' [Q♦],[A♦],[J♠],[K♦],[T♥] ',
 ' [5♦],[7♥],[9♣],[4♠],[6♣],[T♠],[2♦],[8♦],[Q♠],[6♦],[4♥],[3♦],[6♠],[3♠],[9♦],[J♥],[7♠],[9♠],[5♠],[T♣],[K♠],[Q♣],[5♣],[8♠] ',
 ' [T♠],[6♠],[7♠],[9♠],[8♠] ')
 """
