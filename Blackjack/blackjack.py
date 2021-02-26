import random
import time

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True
pot = 0

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.all_cards = []
    
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)


    def shuffle(self):
        random.shuffle(self.all_cards)


    def deal_one(self):
        return self.all_cards.pop()

    
class Hand:
    
    def __init__(self, name):
        self.name = name
        self.all_cards = []
        self.bet = 0
        self.aces = 0 
        self.value = 0
        self.chips = 100


    def __str__(self):
        return f"Player {self.name}"

    def add_cards(self, new_card):
        self.all_cards.append(new_card) 
        if new_card.rank == 'Ace':
            self.aces += 1   
    
    def show_hand(self):
        print(f"\n{self.name} cards: ")
        for i in range (len(self.all_cards)):
            print(f"\t{self.all_cards[i]}")

    def sum_value(self):
        for i in range(len(self.all_cards)):
            self.value += self.all_cards[i].value
            
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


def hit(deck, player):
    player.add_cards(deck.deal_one())
    player.sum_value()
    player.adjust_for_ace()


def hit_stand(deck, player):
    global playing
    while True:
        x = input("Hit or Stand? Enter 'h' or 's' ")
        
        if x[0].lower() == 'h':
            hit(deck,player)
            player_one.show_hand()
              
        elif x[0].lower() == 's':
            print("Player Stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break

def win(player):
    global pot
    pot += player.bet

def take_bet(player):
    global pot
    while True:
        try:
            ask = int(input("What's your bet? "))
            player_one.bet += ask
            pot += ask
            print(f"\nYou have {player_one.chips} Chips left")
            print("Overall Pot is: ", pot)

        except ValueError:
            print("ERROR! Please enter a VALID Integer value!")
        
        else:
            if ask > player_one.chips:
                print("Your don't have enough Chips for this ammount!")
            else:
                break

while True:
        new_deck = Deck()
        new_deck.shuffle()

        player_one = Hand("Player")
        player_dealer = Hand("Dealer")

        take_bet(player_one)
        # Dealing cards to Player and Dealer
        for x in range(2):
            player_one.add_cards(new_deck.deal_one())
            player_dealer.add_cards(new_deck.deal_one())
        
        player_one.show_hand()
        player_dealer.show_hand()

        while True:
            if player_one.value == 21:
                player_one.chips += player_one.bet
                print(f"You win {player_one.bet} chips!")
                print(player_one.chips)
            elif player_dealer.value == 21:
                player_one.chips -= player_one.bet
                print(f"Dealer wins!, You lost {player_one.bet} chips!")
            else:
                break

        hit_stand(new_deck, player_one)

        if player_one.value > 21:
            time.sleep(3)
            print(f"{player_one} Busts!")
            print(f"You lost {player_one.bet} chips!")
            player_one.chips -= player_one.bet
            break

        if player_one.value <= 21:
            
            print("== Dealer plays ==")
            time.sleep(3)

            while player_dealer.value < 17:
                hit(new_deck, player_dealer)

                player_one.show_hand()
                player_dealer.show_hand()

                if player_dealer.value > 21:
                    print("Dealer Busts!")
                    player_one.chips += player_one.bet
                    print(f"You win {player_one.bet} chips!")
                    print(player_one.chips)

                elif player_dealer.value > player_one.value:
                    print("Dealer Wins!")
                    player_one.chips -= player_one.bet
                    print(f"You lost {player_one.bet} chips!")
                    print(player_one.chips)

                elif player_dealer.value < player_one.value:
                    print("Player Wins!")
                    player_one.chips += player_one.bet
                    print(f"You win {player_one.bet} chips!")
                
                else:
                    print("Tie!")

            print(f"You got overall {player_one.chips} chips.")
            new_game = input("New Game? Enter 'y' or 'n' ")
    
            if new_game[0].lower()=='y':
                playing=True
                continue
            else:
                print("Thanks for playing!")
                break