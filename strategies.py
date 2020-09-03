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

def FirstTwoPair(deck):
    """ takes first three cards and draws until two pair
        note: if pair in first three cards, it draws a fourth
    @param deck (treys Deck):
    @returns: playerCards, communityCards
    """
    first_cards = deck.draw(3)
    playerCards = first_cards
    communityCards = []
    pretty_cards = Card.print_pretty_cards(first_cards)
    distinct_ranks = list(set([rank for rank in list(pretty_cards) if rank.isalnum()]))
    # if you draw trips, it doesn't break
    if len(distinct_ranks) == 1:
        playerCards += deck.draw(2)
    # draw a pair
    elif len(distinct_ranks) == 2:
        playerCards += [deck.draw(1)]

    pretty_cards = Card.print_pretty_cards(playerCards)

    while len(playerCards) < 5:
        card = deck.draw(1)
        # check if pair
        if Card.print_pretty_card(card)[1] in pretty_cards:
            playerCards.append(card)
            pretty_cards = Card.print_pretty_cards(playerCards)
        else:
            communityCards.append(card)

    return playerCards, communityCards

def FirstTrips(deck):
    """ takes first three cards and draws till trips
        note: if pair in first three cards, it draws a fourth
    @param deck (treys Deck):
    @returns: playerCards, communityCards
    """
    first_cards = deck.draw(3)
    playerCards = first_cards
    communityCards = []
    pretty_cards = Card.print_pretty_cards(first_cards)
    pretty_ranks = [rank for rank in list(pretty_cards) if rank.isalnum()]
    num_distinct_ranks = len(list(set(pretty_ranks)))
    paired_cards = []
    # if you draw trips, it doesn't break
    if num_distinct_ranks == 1:
        playerCards += deck.draw(2)
    # draw a pair
    elif num_distinct_ranks == 2:
        # get most frequent element
        paired_cards.append(max(set(pretty_ranks), key=pretty_ranks.count))

    # look for pair or trips
    while len(playerCards) < 4:
        card = deck.draw(1)
        if Card.print_pretty_card(card)[1] in pretty_cards:
            playerCards.append(card)
            # check if trips
            if Card.print_pretty_card(card)[1] in paired_cards:
                # makes trips so return
                card = deck.draw(1)
                playerCards.append(card)
            else:
                # add to paired cards list
                paired_cards.append(Card.print_pretty_card(card)[1])
        else:
            communityCards.append(card)

    # look for trips
    while len(playerCards) < 5:
        card = deck.draw(1)
        if Card.print_pretty_card(card)[1] in paired_cards:
            playerCards.append(card)
        else:
            communityCards.append(card)

    return playerCards, communityCards