import random

suits = ['♠', '♣', '♦', '♥']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10,
          'Q': 10, 'K': 10, 'A': 11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.suit} of {self.rank}"

class Deck:
    def __init__(self):
        self.cards = []

        # Generate a deck of cards
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    # For the curious :)
    def display_deck(self):
        for item in self.cards:
            print(item)

    def cards_in_deck(self):
        return len(self.cards)

    # Sometimes casinos play with 3-8 decks.
    def multiply_decks(self, number):
        self.cards = self.cards * number

    # Necessary eh?
    def shuffle(self):
        random.shuffle(self.cards)

    # Deal the last card from the list
    def deal(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.rank = 0
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    # Calculating the correct value of the cards according to standard BJ rules.
    def get_value(self):
        self.value = 0
        # Ace counter for adjusting value over 21.
        ace_count = 0
        for card in self.cards:
            if card.rank == 'A':
                ace_count += 1
            self.value += values[card.rank]
        # Need to adjust the value for aces. Also, 2 aces on start should give a 12, not 2 or 22
        # Example Ace Ace Ace hand should be 13.
        if ace_count == 1 and self.value > 21:
            self.value -= 10
        elif ace_count > 1 and self.value > 21:
            self.value = self.value - 10*(ace_count-1)

    # Use the get_value and return a number for us to show.
    def display_value(self):
        self.get_value()
        return self.value

    # Display the full hand and the value.
    def display_full_hand(self):
        for item in self.cards:
            print(item)
        print("Value:", self.display_value())

    def display_part_hand(self):
        print(self.cards[0])
        print("---HIDDEN---")
        print("Value:", values[self.cards[0].rank])


def game_on():
    # Start with a standard deck, shuffle it. TO-DO: implement the amount of decks.
    play_deck = Deck()
    play_deck.shuffle()

    # Player hand and dealer hand
    player_hand = Hand()
    dealer_hand = Hand()

    # Let's add cards to those hands.
    for _ in range(2):
        player_hand.add_card(play_deck.deal())
        dealer_hand.add_card(play_deck.deal())

    print("Player hand:")
    player_hand.display_full_hand()
    print("\nDealer hand:")
    dealer_hand.display_part_hand()

if __name__ == '__main__':
    game_on()
