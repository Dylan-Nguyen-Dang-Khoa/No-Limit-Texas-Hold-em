from random import shuffle, randint

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
        self.players_list = [Player(input(f"Player {i+1}, please input your name: "), 1500) for i in range(self.player_num)]
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
        

    def play(self):
        while self.quit != "q":
            self.pot = 0
            self.community = []
            for player in self.players_list:
                player.hole_cards = []
                player.fold_status = False
            self.deck = Deck() 
            self.deck.shuffle() 
            self.deal()
            self.preflop()
            self.quit = input("Press q to quit, any other button to continue: ").lower()
            self.movebutton()

    def movebutton(self):
        self.button_player = (self.button_player+1) % self.player_num
        self.small_blind_player = (self.button_player + 1) % self.player_num
        self.big_blind_player = (self.button_player + 2) % self.player_num
        self.utg_player = (self.button_player + 3) % self.player_num

    def preflop(self):
        contributions = {key:0 for key in range(self.player_num)}
        self.pot = self.big_blind_amount + self.small_blind_amount
        contributions[self.small_blind_player] += self.small_blind_amount
        contributions[self.big_blind_player] += self.big_blind_amount
        current_bet = self.big_blind_amount
        last_raise_amount = 0
        current_player_index = self.utg_player
        while len(set(contributions.values())) != 1:
            for player in self.players_list[self.utg_player:]+self.players_list[:self.utg_player]:
                if contributions[current_player_index] != current_bet and not player.fold_status:
                    _ =  input(f"{player.name}, it is now your turn. Please step forward and press enter to continue: ")
                    print(f"Here are your cards: {player.hole_cards}")
                    print("Here are you possible actions")
                    print(f"Call(${current_bet-contributions[current_player_index]})   Raise    Fold")
                    valid_actions = ["call", "raise", "fold"]
                    action = input("Please input your desired action. (Spelling is important, but case-insensitive): ").lower().strip()
                    while action not in valid_actions:
                        print("Please input a valid action")
                        action = input("Please input your desired action (Call, Raise or Fold). (Spelling is important, but case-insensitive): ").lower().strip()
                    if action == "fold":
                        del contributions[current_player_index]
                        player.fold_status == True
                    elif action == "call":
                        amount = current_bet-contributions[current_player_index]
                        player.money -= amount
                        self.pot += amount
                        contributions[current_player_index] += amount
                    else:
                        raise_to = int(input(f"Please input the amount you want to raise to (Min: {max(self.big_blind_amount * 2, last_raise_amount + current_bet)}, Max:{player.money-contributions[index]}):"))
                        while raise_to > player.money-contributions[current_player_index] or raise_to < max(self.big_blind_amount * 2, last_raise_amount + current_bet):
                            print("Your raise amount is invalid. Please input a valid raise amount")
                            raise_to = int(input(f"Please input the amount you want to raise to (Min: {max(self.big_blind_amount * 2, last_raise_amount + current_bet)}, Max:{player.money-contributions[index]}):"))
                        last_raise_amount, current_bet = raise_to - current_bet, raise_to
                        amount = current_bet - contributions[current_player_index]
                        player.money -= amount
                        self.pot += amount
                        contributions[current_player_index] += amount
                else:
                    continue
                current_player_index = (current_player_index + 1) % self.player_num

    

    def postflop(self):
        ...
        
    def deal(self):
        for _ in range(2):
            for player in self.players_list:
                player.hole_cards.append(self.deck.deal_card())

    def player_num_init(self):
        self.player_num = None
        while self.player_num is None or not 3 <= self.player_num <= 10:
            try:
                self.player_num = int(input("Please input the number of players you want (2-10): "))
            except ValueError:
                print("Please input a number")
    
    def blinds_init(self):
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
