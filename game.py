import sys
import itertools
import argparse

from treys import Card
from treys import Evaluator
from treys import Deck

from rules import *
from utils import lget

POKER_HAND_EVALUATOR = Evaluator()


def isTypeOfCard(card, desiredCards):
    for desiredCard in desiredCards:
        if desiredCard in card:
            desiredCards.remove(desiredCard)
            return True
    return False


def simulatePokerSolitaire(desiredCards):
    """Simulates the game of playPoker.
    Args:
        cardsDesired: the cards that the
        player specified to want to draw
    Returns:
        playerCards: the cards drawn by
        the player
        communityCards: the cards drawn by
        the community
    """
    playerCards, communityCards, deck = [], [], Deck()
    while len(playerCards) != 5 or len(communityCards) < 5:
        card = deck.draw(1)

        if len(playerCards) != 5:
            stringCardDrawn = Card.print_pretty_card(card)
            if isTypeOfCard(stringCardDrawn, desiredCards):
                playerCards.append(card)

        communityCards.append(card)

    return playerCards, communityCards


def findStrongestCombinationAndItsStrength(totalCombinations):
    combination = totalCombinations[0]
    handStrength = POKER_HAND_EVALUATOR.evaluate(list(combination), [])
    for index in range(0, len(totalCombinations)):
        tempHandStrength = POKER_HAND_EVALUATOR.evaluate(
            list(totalCombinations[index]), []
        )
        if tempHandStrength <= handStrength:
            handStrength = tempHandStrength
            combination = totalCombinations[index]

    return combination, handStrength


def evaluateBetterHand(playerCards, communityCards):
    """Evaluates the stronger hand between the player's hand
    and the community's strongest 5 card combination
    Args:
        playerCards --> player's 5 cards
        communityCards --> community's collected cards
    Returns:
        boolean --> if playerHand is lower (stronger)
        bestCommunityCombination --> strongest possible hand that
        the community has
    """
    playerHandStrength = POKER_HAND_EVALUATOR.evaluate(playerCards, [])
    totalCombinations = [
        combinationCommunityCards
        for combinationCommunityCards in itertools.combinations(communityCards, 5)
    ]

    (
        communityStrongestCombo,
        communityHandStrength,
    ) = findStrongestCombinationAndItsStrength(totalCombinations)

    return (
        communityHandStrength >= playerHandStrength,
        communityStrongestCombo,
    )


def playPoker(enterHand):
    enterHandInSymbols = [
        Card.print_pretty_card(Card.new(card)) if len(card) > 1 else card
        for card in enterHand
    ]
    playerCards, communityCards = simulatePokerSolitaire(enterHandInSymbols)
    playerWin, bestCommunityCombination = evaluateBetterHand(
        playerCards, communityCards
    )

    return (
        playerWin,
        Card.print_pretty_cards(playerCards),
        Card.print_pretty_cards(communityCards),
        Card.print_pretty_cards(bestCommunityCombination),
    )