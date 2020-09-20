from treys import Card
from treys import Evaluator
from treys import Deck

""" takes first five cards 
@param deck (treys Deck): deck for drawing
@returns: playerCards, communityCards
"""
# def firstFive(deck):
#     return deck.draw(5), []

def getCardSuit(card):
    return Card.print_pretty_card(card)[2]


def getRank(card):
    return Card.print_pretty_card(card)[1]


def getRanks(cards):
    if cards == []:
        return ''
    elif type(cards) is int:
        return Card.print_pretty_card(cards)
    if type(cards) is list:
        return Card.print_pretty_cards(cards)


def drawAnyNumberOfCards(deck, numberOfCards):
    if numberOfCards == 0:
        return []
    elif numberOfCards == 1:
        return [deck.draw(numberOfCards)]
    else:
        return deck.draw(numberOfCards)


def getMostFrequentCard(cards):
    cardsAsString = Card.print_pretty_cards(cards)
    cardRanksAsList = [rank for rank in list(cardsAsString) if rank.isalnum()]
    return max(set(cardRanksAsList), key=cardRanksAsList.count)


def getLeastFrequentCard(cards):
    cardsAsString = Card.print_pretty_cards(cards)
    cardRanksAsList = [rank for rank in list(cardsAsString) if rank.isalnum()]
    return min(set(cardRanksAsList), key=cardRanksAsList.count)


def getNumberOfDistinctRanks(cards):
    cardsAsString = Card.print_pretty_cards(cards)
    cardRanksAsList = [rank for rank in list(cardsAsString) if rank.isalnum()]
    return len(set(cardRanksAsList))


# function draws until N of a kind (i.e. 1, 2, 3, 4 of a kind)
# @param additionalPair (bool): if True, adds another pair to requirement. N=2 -> two pair, N=3 -> full house
# note: if it by chance finds a better hand like trips instead of two pair, it keeps the better hand
def firstNOfAKind(deck, N, additionalPair = 1):
    playerCards, communityCards = [], []
    additionalPair = 1 if (additionalPair and N != 4) else 0

    while len(communityCards) < 5 or len(playerCards) < 5:
        card = deck.draw(1)

        if len(playerCards) == 5:
            communityCards.append(card)
        # add initial cards to deck
        elif (5 - getNumberOfDistinctRanks(playerCards)) >= (N + additionalPair):
            playerCards.append(card)
        # if card does not make at least a pair, append to community
        elif getRank(card) not in getRanks(playerCards):
            communityCards.append(card)
        # if there is no most frequent card, append
        elif getMostFrequentCard(playerCards) == getLeastFrequentCard(playerCards):
            playerCards.append(card)
        elif getRank(card) == getMostFrequentCard(playerCards):
            playerCards.append(card)
        elif additionalPair == 1:
            playerCards.append(card)
        else:
            communityCards.append(card)

    return playerCards, communityCards