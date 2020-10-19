STR_RANKS = "23456789TJQKA"
INT_RANKS = range(13)

CHAR_RANK_TO_INT_RANK = dict(zip(list(STR_RANKS), INT_RANKS))
CHAR_SUIT_TO_INT_SUIT = {
    "s": 1,  # spades
    "h": 2,  # hearts
    "d": 4,  # diamonds
    "c": 8,  # clubs
}
