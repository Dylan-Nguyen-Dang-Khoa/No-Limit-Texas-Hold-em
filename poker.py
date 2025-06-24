from random import shuffle, randint
import os

def clear_screen():
    if os.name == "nt":
        for i in range(2):
            os.system("cls")
    else:
        for i in range(2):
            os.system("clear")

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hole_cards = []
        self.fold_status = False 

    def __str__(self):
        return f"Name: {self.name}, Balance: {self.money}"
    
    def __repr__(self):
        return str(self)

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self):
        return str(self)

class Deck:
    def __init__(self):
        suits = ["diamonds", "hearts", "clubs", "spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        self.deck = [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        shuffle(self.deck)
    
    def deal_card(self):
        return self.deck.pop(0)
    
    def __str__(self):
        return str(self.deck)
    
    def __repr__(self):
        return str(self)

class PokerGame:
    def __init__(self):
        self.player_num_init()  
        self.blinds_init() 
        self.players_list = [Player(input(f"Player {i+1}, please input your name: ").strip(), 1500) for i in range(self.player_num)]
        self.button_player = randint(0, len(self.players_list)-1) 
        self.small_blind_player = (self.button_player + 1) % self.player_num
        self.big_blind_player = (self.button_player + 2) % self.player_num
        self.utg_player = (self.button_player + 3) % self.player_num
        self.quit = ""
        """
        self.deck is shuffled card deck
        self.player_num is number of players
        self.big_blind_amount is the big blind amount
        self.small_blind_amount is the small blind amount
        self.players_list is the list with all the player objects
        self.dealer is the dealer position in self.players_list
        self.small_blind_player is the small blind position in self.players_list
        self.big_blind_player is the big blind position in self.players_list
        self.utg_player is the position of the player after the big blind in self.players_list
        """ 
        
    def deal(self): # Deal cards to each player one at a time until everyone has 2
        for _ in range(2):
            for player in self.players_list:
                player.hole_cards.append(self.deck.deal_card())

    def movebutton(self): # Move the dealer, blinds and under the gun player
        self.button_player = (self.button_player+1) % self.player_num
        self.small_blind_player = (self.button_player + 1) % self.player_num
        self.big_blind_player = (self.button_player + 2) % self.player_num
        self.utg_player = (self.button_player + 3) % self.player_num

    def reset(self): # Reset after showdown for next set of rounds
        self.pot = 0
        self.community = []
        for player in self.players_list:
            player.hole_cards = []
            player.fold_status = False
        self.deck = Deck()
        self.deck.shuffle()

    def play(self): # This is the flow of the game
        while self.quit != "q":
            self.active_players = self.player_num
            self.movebutton()
            self.reset()
            self.deal()
            self.preflop()
            self.quit = input("Press q to quit, any other button to continue: ").lower().strip()


    def round_init(self): # Initialise the betting round
        contributions = {key:0 for key in range(self.player_num)}
        self.pot = self.big_blind_amount + self.small_blind_amount
        contributions[self.small_blind_player] += self.small_blind_amount
        contributions[self.big_blind_player] += self.big_blind_amount
        current_bet = last_raise_amount = self.big_blind_amount
        
        current_player_index = self.utg_player
        return contributions, current_bet, last_raise_amount, current_player_index
    
    def playerUI(self, player, player_contributions, current_bet, type): # This is all the code relating to what each player will see during their turn
        clear_screen()
        input(f"{player.name}, it is now your turn. Please step forward and press enter to continue: ")
        print(f"Hole cards: {player.hole_cards}", end="\n\n")
        if type == "preflop":
            print(f"Actions: Call({current_bet-player_contributions})  Raise  Fold")
            action = input("Please input your desired action (call, raise, fold). Keep in mind the spelling, but it is case-insensitive: ").lower().strip()
            valid_moves = ["call", "fold", "raise"]
            while action not in valid_moves:
                print("Please input a valid move")
                action = input("Please input your desired action (call, raise, fold). Keep in mind the spelling, but it is case-insensitive: ").lower().strip()
        else:
            ...
        return action

    def game_update(self, amount, contributions, current_player_index, player): # Updates the player and pot amount after bettng
        contributions[current_player_index] += amount
        self.pot += amount
        player.money -= amount
        return contributions

    def preflop(self): # This is the logic for the preflop rounds, which is used in self.game as one of the game rounds
        contributions, current_bet, last_raise_amount, current_player_index = self.round_init()
        while len(set(contributions.values())) > 1 and self.active_players > 1:
            player = self.players_list[current_player_index]
            player_contributions = contributions[current_player_index]
            if not player.fold_status and player_contributions < current_bet:
                action = self.playerUI(player, player_contributions, current_bet, "preflop")
                if action == "fold":
                    del contributions[current_player_index]
                    player.fold_status = True
                    self.active_players -= 1
                elif action == "call":
                    amount = current_bet-player_contributions
                    contributions = self.game_update(amount, contributions, current_player_index, player)
                elif action == "raise":
                    while True:
                        try:
                            raise_to = int(input(f"Please input the amount you want to raise to (Min: {current_bet + last_raise_amount}, Max: {player_contributions + player.money})"))
                            if current_bet + last_raise_amount <= raise_to <= player_contributions + player.money:
                                break
                            else:
                                print("Please input a valid amount within the allowed range.")
                        except ValueError:
                            print("Please input a number")
                    last_raise_amount = raise_to - current_bet
                    current_bet = raise_to
                    amount = current_bet-player_contributions
                    contributions = self.game_update(amount, contributions, current_player_index, player)
            current_player_index = (current_player_index + 1) % self.player_num

    def postflop(self):
        ...

    def player_num_init(self): # Check if the number of players is valid and initialises it at the beginning of everything
        self.player_num = None
        while self.player_num is None or not 3 <= self.player_num <= 10:
            try:
                self.player_num = int(input("Please input the number of players you want (2-10): "))
            except ValueError:
                print("Please input a number")
    
    def blinds_init(self): # Check if the blind amount is valid and intialises it as the beginning of everything
        self.big_blind_amount = None
        while self.big_blind_amount is None or not self.big_blind_amount >= 2:
            try:
                self.big_blind_amount = int(input("Please input your big blind (Must be bigger than or equal to 2): "))
            except ValueError:
                print("Please input a number")
        self.small_blind_amount = self.big_blind_amount//2
    
    def __str__(self):
        return "Hi! This is the poker game object."
    
    def __repr__(self):
        return str(self)

class HandEvaluator:
    ...

def main():
    game = PokerGame()
    game.play()
    
main()
