import random

suits = ['♠', '♣', '♦', '♥']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []

        # Generate a deck of cards
        for suit in suits:
            for value in values:
                self.cards.append(Card(value, suit))

    def display_deck(self):
        for item in self.cards:
            print(item)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

deck = Deck()
deck.shuffle()
print(deck.deal())