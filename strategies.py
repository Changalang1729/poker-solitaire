from treys import Card
from treys import Evaluator
from treys import Deck

""" takes first five cards 
@param deck (treys Deck): deck for drawing
@returns: playerCards, communityCards
"""
def FirstFive(deck):
    return deck.draw(5), []

""" looks for cards with suit of first card
@param deck (treys Deck): deck for drawing
@returns: playerCards, communityCards
"""
def FirstFlush(deck):
    firstCard = deck.draw(1)
    firstSuit = Card.print_pretty_card(firstCard)[2]
    playerCards = [firstCard]
    communityCards = []
    while len(playerCards) < 5:
        card = deck.draw(1)
        if Card.print_pretty_card(card)[2] == firstSuit:
            playerCards.append(card)
        else:
            communityCards.append(card)
    return playerCards, communityCards

"""" takes first four cards and draws until it pairs one
@param deck (treys Deck):
@param returns: playerCards, communityCards
"""
def FirstPair(deck):
    firstCards = deck.draw(4)
    playerCards = firstCards
    communityCards = []
    firstCardsAsString = Card.print_pretty_cards(firstCards)
    while len(playerCards) < 5:
        card = deck.draw(1)
        # check if drawn card rank in first four
        if Card.print_pretty_card(card)[1] in firstCardsAsString:
            playerCards.append(card)
        else:
            communityCards.append(card)
    return playerCards, communityCards

""" takes first three cards and draws until two pair
    note: if pair in first three cards, it draws a fourth
@param deck (treys Deck):
@returns: playerCards, communityCards
"""
def FirstTwoPair(deck):
    firstCards = deck.draw(3)
    playerCards = firstCards
    communityCards = []
    cardsAsString = Card.print_pretty_cards(firstCards)
    distinctRanks = list(set([rank for rank in list(cardsAsString) if rank.isalnum()]))
    # if you draw trips, it doesn't break
    if len(distinctRanks) == 1:
        playerCards += deck.draw(2)
    # draw a pair
    elif len(distinctRanks) == 2:
        playerCards += [deck.draw(1)]

    cardsAsString = Card.print_pretty_cards(playerCards)

    while len(playerCards) < 5:
        card = deck.draw(1)
        # check if pair
        if Card.print_pretty_card(card)[1] in cardsAsString:
            playerCards.append(card)
            cardsAsString = Card.print_pretty_cards(playerCards)
        else:
            communityCards.append(card)

    return playerCards, communityCards

""" takes first three cards and draws till trips
    note: if pair in first three cards, it draws a fourth
@param deck (treys Deck):
@returns: playerCards, communityCards
"""
def FirstTrips(deck):
    firstCards = deck.draw(3)
    playerCards = firstCards
    communityCards = []
    cardsAsString = Card.print_pretty_cards(firstCards)
    cardRanksAsList = [rank for rank in list(cardsAsString) if rank.isalnum()]
    numDistinctRanks = len(set(cardRanksAsList))
    pairedCards = []
    # if you draw trips, it doesn't break
    if numDistinctRanks == 1:
        playerCards += deck.draw(2)
    # draw a pair
    elif numDistinctRanks == 2:
        # get most frequent element
        pairedCards.append(max(set(cardRanksAsList), key=cardRanksAsList.count))

    # look for pair or trips
    while len(playerCards) < 4:
        card = deck.draw(1)
        if Card.print_pretty_card(card)[1] in cardsAsString:
            playerCards.append(card)
            # check if trips
            if Card.print_pretty_card(card)[1] in pairedCards:
                # makes trips so return
                card = deck.draw(1)
                playerCards.append(card)
            else:
                # add to paired cards list
                pairedCards.append(Card.print_pretty_card(card)[1])
        else:
            communityCards.append(card)

    # look for trips
    while len(playerCards) < 5:
        card = deck.draw(1)
        if Card.print_pretty_card(card)[1] in pairedCards:
            playerCards.append(card)
        else:
            communityCards.append(card)

    return playerCards, communityCards