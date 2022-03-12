import random

class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face
        if self.face in {'Jack', 'Queen', 'King', }:
            self.value = 10
        elif self.face == 'Ace':
            self.value = 11
        else:
            self.value = self.face

    def __str__(self):
        return f'{self.face} of {self.suit}'

    def __repr__(self):
        return f"<Card | {self.face} of {self.suit}"

class Deck:
    def __init__(self):
        self.decklist = []
    
    def generate_deck(self):
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        faces = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        self.decklist = [Card(suit, face) for suit in suits for face in faces]
        return self.decklist
        
    def print_deck(self):
        print(f"There are {len(self.decklist)} cards left in the decklist.")
        for card in self.decklist:
            print(f"{card.face} of {card.suit}")

    def randomize_deck(self):
        random.shuffle(self.decklist)

    def deal_single_card(self, dealerdeck):
        single_card = dealerdeck.decklist.pop(0)
        return single_card
        
class Person:
    def __init__(self, name):
        self.name = name.title()
        self.hand = []
        self.bust = False

    def add_to_hand(self, name, card):
        name.hand.append(card)
        print(self.hand)

    def show_hand(self):
        if self.hand:
            print("-----")
            for card in self.hand:
                print(card)
            print("-----")
        else:
            print("Your hand is empty.")
        

    def hand_total(self):
        ace = 0
        total = sum([card.value for card in self.hand if card.face != 'Ace'])
        ace   = sum([ace + 1 for card in self.hand if card.face == 'Ace' ])
        
        if ace > 0:
            for i in range(ace):
                if total + 11 > 21:
                    total += 1
                else:
                    total += 11

        return total
    
    def __str__(self):
        return self.name

    def __repr__(self):
        print(f"<Person | {self.name} {self.hand}")


class Player(Person):
    def __init__(self, name, cash):
        super().__init__(name)
        self.cash = cash
        self.bet = 0
        self.blackjack = False

    def bet_win(self):
        self.cash += 2 * self.bet
        self.bet = 0
    
    def bet_lose(self):
        self.bet = 0

class Dealer(Person):
    def __init__(self, name):
        super().__init__(name)
        self.dealerDeck = Deck()

    def gen_deck(self):
        self.dealerDeck.generate_deck()

    def shuffle(self):
        self.dealerDeck.randomize_deck()

    def deal_card(self, name, times):
        # print(self.deck.deck)
        # loop for each time card dealt
        for i in range(times):
            rand_card = self.dealerDeck.deal_single_card(self.dealerDeck)
            name.hand.append(rand_card)

    def reveal_first_card(self):
        print(f"The dealers face up card is {self.hand[0]}")

def create_dealer():
    # Generate Dealer, create / shuffle deck
    potentialdealers = ["Lilja", "Elviira", "Jakub", "Slagathor", "Saybil", "Holt"]
    dealer = potentialdealers[random.randint(0, len(potentialdealers)-1)]
    dealer = Dealer(dealer)
    dealer.gen_deck()
    dealer.shuffle()
    return dealer

def blackjack():
    players = []
    
    # Main Game Loop
    while True:
        dealer = create_dealer()
    
        print(f"Hello and welcome to Bobs Blackjack emporium! Your dealer today will be {dealer.name}, and they'll be taking care of you this evening. Let's get started!")
        # Add players
        while True:
            player_name  = input("What is your name: ")
            player_cash  = int(input("How much do you have to bet: "))
            new_player = Player(player_name, player_cash)
            players.append(new_player)

            # Add another player or continue with game.
            cont = input("Would you like to add a new player? (Y/N) ").lower()
            while cont not in {'y', 'n'}:
                cont = input("Please enter either 'Y' or 'N'").lower()
            
            if cont == 'n':
                break

        # Game starts here, restart skips creating players
        while True:
            # deal starter cards to players
            for player in players: 
                #Get bets
                while True:
                    playerbet = int(input(f"{player.name}, how much would you like to bet? "))
                    if playerbet <= player.cash:
                        player.bet = playerbet      # set the bet amount
                        player.cash -= player.bet   # remove the bet from cash pool
                        break
                    print(f"Sorry, you only have ${player.cash} left to spend. Please enter an amount lower than that.")

                print(player)
                dealer.deal_card(player, 2)
                player.show_hand()
                print(player.hand_total())
                print()
                
                # test for blackjack
                if player.hand_total() == 21:
                    print(f"Congratulations {player.name}! Starting hand of 21 is a Blackjack and you win.")
                    player.bet_win()
                    print(f"Your new total is {player.cash}")
                    print()
                    player.blackjack = True

            # deal dealer cards
            dealer.deal_card(dealer, 2)
            dealer.reveal_first_card()
            print()

            for player in players:
                if not player.blackjack:
                    print(f"Your turn {player.name}, your current hand is...")
                    player.show_hand()
                    print(f"For a total of {player.hand_total()}\n")

                    # loop until bust or stand
                    print(f"{player.name} is up.")
                    while True:
                        hit = input("What would you like to do? You can choose to 'hit' or 'stand' ")

                        # Test valid input
                        while hit not in {'hit', 'stand'}:
                            hit = input("Please enter 'hit' or 'stand'")
                        # If player stands, break
                        if hit == 'stand':
                            break
                        #else
                        dealer.deal_card(player, 1)
                        print("Your current hand is now: ")
                        player.show_hand()
                        print(f"Your new total is {player.hand_total()}")

                        # Test if hand is a bust, break current player loop
                        if player.hand_total() > 21:
                            print("Sorry, over 21 is a bust and you lose.")
                            player.bust = True
                            break

            # Dealer hits until 17 or higher
            dealer.show_hand()
            while dealer.hand_total() < 17:
                dealer.deal_card(dealer, 1)
                print(f"The dealers total is: {dealer.hand_total()}")
            dealer.show_hand()

            if dealer.hand_total() > 21:
                print("Dealer busts.")
                dealer.bust = True

            # Test if player wins
            for player in players:
                if (player.hand_total() > dealer.hand_total() or dealer.bust) and not player.bust:
                    print(f"Congratulations {player.name}, you win this round!")
                    player.bet_win()
                    print(f"You have ${player.cash} remaining.")
                else:
                    print(f"Sorry {player.name}, Dealer {dealer.name} wins.")
                    player.bet_lose()
                    print(f"You have ${player.cash} remaining.")

                # Reset player hand
                player.hand = []
                player.bust = False

                # Check player cash
                if player.cash == 0:
                    player_check = input(f"Sorry {player.name}, you're out of cash. Would you like to add more to continue? (y/n) ").lower()
                    while player_check not in {'y', 'n'}:
                        player_check = input(f"Sorry {player.name}, you're out of cash. Would you like to add more to continue? (y/n) ").lower()
                    if player_check == 'y':
                        player.cash += int(input("Please enter the amount of cash you want to add: "))
                    else:
                        players.remove(player)
                else:
                    # Check if player wants to continue
                    player_quit = input(f"{player.name}, would you like to play again? (y/n) ").lower()
                    while player_quit not in {'y', 'n'}:
                        player_quit = input("Would you like to play again? (y/n) ")
                    if player_quit == 'n':
                        players.remove(player)
            
            if len(players) > 0:
                # Reset dealer if game restarts
                dealer.hand = []
                dealer.bust = False
                dealer.gen_deck()
                dealer.shuffle()
                continue

            # Exit game loop if players quit
            break

        # Quit game
        break


blackjack()