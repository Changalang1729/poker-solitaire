import sys
import itertools
import argparse

from treys import Card
from treys import Evaluator
from treys import Deck

from rules import *
from utils import lget

def typeOfCard(card, cardsDesired):
    if not cardsDesired:
        return True
    
    return card in cardsDesired


def simulatePokerSolitaire(cardsDesired, keyWord):
    playerCards, communityCards, deck = [], [], Deck()
    
    if keyWord == "FirstFive":
        cardsDesired = []
        cards = deck.draw(5)
        for card in cards:
            playerCards.append(card)
    count = 0

    while len(playerCards) != 5:
        card = deck.draw(1)
        count += 1
        if typeOfCard(Card.print_pretty_card(card), Card.print_pretty_cards(cardsDesired)):
            playerCards.append(card)
        else:
            communityCards.append(card)
    
    if len(communityCards) < 5:
        numOfCardsNeeded = 5 - len(communityCards)
        cards = deck.draw(numOfCardsNeeded)
        for card in cards:
            communityCards.append(card)
            
    return playerCards, communityCards


def findBestCombination(totalCombinations, highestScore, evaluator):
    for combination in totalCombinations:
        if evaluator.evaluate(list(combination), []) == highestScore:
            return list(combination)
    
    return None


def evaluateBetterHand(playerCards, communityCards):
    evaluator = Evaluator()
    playerScore = evaluator.evaluate(playerCards, [])
    totalCombinations = [combinationCommunityCards for combinationCommunityCards in itertools.combinations(communityCards, 5)]
    highestScore = min(evaluator.evaluate(list(combination), []) for combination in totalCombinations)
    bestCommunityCombination = findBestCombination(totalCombinations, highestScore, evaluator)
    
    return highestScore >= playerScore, bestCommunityCombination


def playPoker(enterHand, keyWord):
    numericCardHand = [((CHAR_RANK_TO_INT_RANK[lget(card, 0)] << 8) + 
                        (CHAR_SUIT_TO_INT_SUIT[lget(card, 1)] << 12)) for card in enterHand]
    playerCards, communityCards = simulatePokerSolitaire(numericCardHand, keyWord)
    playerWin, bestCommunityCombination = evaluateBetterHand(playerCards, communityCards)
    
    return playerWin, Card.print_pretty_cards(playerCards), Card.print_pretty_cards(communityCards), Card.print_pretty_cards(bestCommunityCombination)


if __name__ == "__main__":
    CLI = argparse.ArgumentParser()
    CLI.add_argument(
        "--cards", 
        nargs = 5, 
        type = str,
       	default = ['2c', '3s', '4d', '5s', '7s'],
    )
    CLI.add_argument(
    	"--key",
    	nargs=1,
    	type = str, 
    	default = None,
    )

    args = CLI.parse_args()
    playerCards = args.cards
    keyWord = args.key

    print(playPoker(playerCards, keyWord))
