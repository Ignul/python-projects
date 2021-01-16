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
        print("---HIDDEN---")
        print(self.cards[1])
        print("Value:", values[self.cards[1].rank])


class Game:

    # Need to know when the player goes over. Returns a simple T/F.
    def player_over_21(self):
        return self.player_hand.display_value() > 21

    # Need to know when the dealer goes over. Returns a simple T/F.
    def dealer_over_21(self):
        return self.dealer_hand.display_value() > 21

    # The checks for instant blackjack win!
    def check_blackjack(self):
        player = False
        dealer = False
        if self.player_hand.display_value() == 21:
            player = True
        if self.dealer_hand.display_value() == 21:
            dealer = True

        return player, dealer

    # Shows the results of instant blackjack win!
    def show_bj_result(self, player_bj, dealer_bj):
        if player_bj and dealer_bj:
            print("Both have BLACKJACK! Draw.")
        elif player_bj:
            print("Player WINS with a BLACKJACK!")
        elif dealer_bj:
            print("Dealer WINS with a BLACKJACK!")

    # Start the game!
    def play_bj(self):
        # Set the loop game state. Playing/Not Playing
        game_state = True
        # Set the other loop state. Is this game over?
        game_over = False

        while game_state:
            # Start with a standard deck, shuffle it. TO-DO: implement the amount of decks.
            self.play_deck = Deck()
            self.play_deck.shuffle()

            # Player hand and dealer hand
            self.player_hand = Hand()
            self.dealer_hand = Hand()
            # Let's add cards to those hands.
            for _ in range(2):
                self.player_hand.add_card(self.play_deck.deal())
                self.dealer_hand.add_card(self.play_deck.deal())

            # Display the hands.
            print("Player hand:")
            self.player_hand.display_full_hand()
            print("\nDealer hand:")
            self.dealer_hand.display_part_hand()

            while not game_over:
                # A quick check for a potential instant blackjack win. If so - do not continue.
                player_bj, dealer_bj = self.check_blackjack()
                if player_bj or dealer_bj:
                    # BLACKJACK can only happen at the beginning of the game, meaning both have only 2 cards.
                    if len(self.player_hand.cards) == 2 and len(self.dealer_hand.cards) == 2:
                        game_over = True
                        self.dealer_hand.display_full_hand()
                        self.show_bj_result(player_bj, dealer_bj)
                        continue

                # Let's ask the user, what does he want to do. + invalid input check.
                while True:
                    try:
                        user_input = input('Your decision: [(H)it, (S)tand]').lower()
                        if user_input not in ['h', 'hit', 's', 'stand']:
                            raise ValueError
                        break
                    except ValueError:
                        print("Invalid input, try again!")

                # If the user hits.
                if user_input in ['h', 'hit']:
                    self.player_hand.add_card(self.play_deck.deal())
                    self.player_hand.display_full_hand()

                    # Need to make sure the player doesn't go overboard.
                    if self.player_over_21():
                        print("The player goes over 21 and loses.")
                        game_over = True

                # The player stands, let's finish rolling out the game. ADD: dealer drawing cards until 17.
                else:
                    # Show both hands fully.
                    self.player_hand.display_full_hand()
                    self.dealer_hand.display_full_hand()

                    # Show both values fully.
                    print("Final Result:")
                    print("Player Hand Value:", self.player_hand.display_value())
                    print("Dealer Hand Value:", self.dealer_hand.display_value())

                    # Announce the winner!
                    if self.player_hand.display_value() > self.dealer_hand.display_value():
                        print("Player WINS!")
                    elif self.player_hand.display_value() < self.dealer_hand.display_value():
                        print("Dealer WINS!")
                    elif self.player_hand.display_value() == self.dealer_hand.display_value():
                        print("It's a tie!")

                    game_over = True

            while True:
                try:
                    play_again_input = input("Play again? [Yes/No]").lower()
                    if play_again_input not in ['yes', 'no', 'y', 'n']:
                        raise ValueError
                    break

                except ValueError:
                    print("Invalid input, try again.")

            if play_again_input in ['no', 'n']:
                print("Thank you for playing!")
                break
            else:
                game_over = False
                continue


if __name__ == '__main__':
    # Create an instance of the game.
    blackjack = Game()
    # Launch the game.
    blackjack.play_bj()
