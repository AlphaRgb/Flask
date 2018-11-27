# -*- coding: utf-8 -*-
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamods clubs hearts'.split()

    def __init__(self):
        self._cards = [
            Card(rank, suit) for suit in self.suits for rank in self.ranks
        ]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __repr__(self):
        return 'this is a FrenchDeck...'


if __name__ == '__main__':
    deck = FrenchDeck()
    beer_card = Card('7', 'diamonds')
    print(beer_card)
    d = FrenchDeck()
    print(len(d))
    for _ in iter(d):
        print(_)
