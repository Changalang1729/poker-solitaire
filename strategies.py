from treys import Card
from treys import Evaluator
from treys import Deck

def FirstFive(deck):
    """ takes first five cards 
    @param deck (treys Deck): deck for drawing
    @returns: playerCards, communityCards
    """
    return deck.draw(5), []

def FirstFlush(deck):
    """ looks for cards with suit of first card
    @param deck (treys Deck): deck for drawing
    @returns: playerCards, communityCards
    """
    first_card = deck.draw(1)
    first_suit = Card.print_pretty_card(first_card)[2]
    playerCards = [first_card]
    communityCards = []
    while len(playerCards) < 5:
        card = deck.draw(1)
        if Card.print_pretty_card(card)[2] == first_suit:
            playerCards.append(card)
        else:
            communityCards.append(card)
    return playerCards, communityCards

def FirstPair(deck):
    """" takes first four cards and draws until it pairs one
    @param deck (treys Deck):
    @param returns: playerCards, communityCards
    """
    first_cards = deck.draw(4)
    playerCards = first_cards
    communityCards = []
    first_cards_pretty = Card.print_pretty_cards(first_cards)
    while len(playerCards) < 5:
        card = deck.draw(1)
        # check if drawn card rank in first four
        if Card.print_pretty_card(card)[1] in first_cards_pretty:
            playerCards.append(card)
        else:
            communityCards.append(card)
    return playerCards, communityCards