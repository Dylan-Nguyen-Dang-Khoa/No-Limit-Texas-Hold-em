from random import shuffle, randint
from itertools import combinations
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
        suits = ["Diamonds", "Hearts", "Clubs", "Spades"]
        ranks = [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "Jack",
            "Queen",
            "King",
            "Ace",
        ]
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
        self.players_list = [
            Player(input(f"Player {i+1}, please input your name: ").strip(), 1500)
            for i in range(self.player_num)
        ]
        self.button_player = randint(0, len(self.players_list) - 1)
        self.small_blind_player = (self.button_player + 1) % self.player_num
        self.big_blind_player = (self.button_player + 2) % self.player_num
        self.utg_player = (self.button_player + 3) % self.player_num
        self.quit = ""
        """
        self.deck is shuffled card deck
        self.player_num is number of players
        self.big_blind_amount is the big blind amount
        self.small_blind_amount is the small blind amount
        self.players_list is the list with all the player objects, even those who have folded
        self.dealer is the dealer position in self.players_list
        self.small_blind_player is the small blind position in self.players_list
        self.big_blind_player is the big blind position in self.players_list
        self.utg_player is the position of the player after the big blind in self.players_list
        """

    def deal(self):  # Deal cards to each player one at a time until everyone has 2
        for _ in range(2):
            for player in self.players_list:
                player.hole_cards.append(self.deck.deal_card())

    def movebutton(
        self,
    ):  # Move the dealer, blinds and under the gun player for next hand
        self.button_player = (self.button_player + 1) % self.player_num
        self.small_blind_player = (self.button_player + 1) % self.player_num
        self.big_blind_player = (self.button_player + 2) % self.player_num
        self.utg_player = (self.button_player + 3) % self.player_num

    def reset(self):  # Reset after showdown for next hand
        self.active_players = self.player_num
        self.pot = 0
        self.community_cards = []
        for player in self.players_list:
            player.hole_cards = []
            player.fold_status = False
        self.deck = Deck()
        self.deck.shuffle()

    def play(self):  # This is the flow of the game
        while self.quit != "q":
            print(f"The dealer is {self.players_list[self.button_player].name}")
            input("Press enter to continue: ")
            self.reset()
            self.deal()
            self.preflop()
            if self.active_players > 1:
                for i in range(3):
                    self.community_cards.append(self.deck.deal_card())
                clear_screen()
                print(f"Community Cards: {self.community_cards}")
                input("Press enter to continue: ")
                self.postflop()
            for i in range(2):
                if self.active_players > 1:
                    self.community_cards.append(self.deck.deal_card())
                    clear_screen()
                    print(f"Community Cards: {self.community_cards}")
                    input("Press enter to continue: ")
                    self.postflop()
                else:
                    break
            self.active_players_list = [
                player_index
                for player_index in range(self.player_num)
                if not self.players_list[player_index].fold_status
            ]
            if len(self.active_players_list) == 1:
                self.players_list[self.active_players_list[0]].money += self.pot
            else:
                self.active_players_cards = {
                    player_index: self.players_list[player_index].hole_cards
                    for player_index in self.active_players_list
                }
                hand_evaluation = HandEvaluator(
                    self.active_players_cards,
                    self.community_cards,
                )
                winner = hand_evaluation.evaluate()
                self.players_list[winner].money += winner
            self.quit = (
                input("Press q to quit, any other button to continue: ").lower().strip()
            )
            self.movebutton()

    def playerUI(
        self, player, player_contributions, current_bet, type
    ):  # This is all the code relating to what each player will see during their turn
        clear_screen()
        input(
            f"{player.name}, it is now your turn. Please step forward and press enter to continue: "
        )
        print(f"Balance: ${player.money}")
        print(f"Hole cards: {player.hole_cards}")
        print(f"Community Cards: {self.community_cards}")
        print(f"Pot: ${self.pot}", end="\n\n")
        if type == "preflop no check":
            print(f"Actions: Call(${current_bet-player_contributions})  Raise  Fold")
            action = (
                input(
                    "Please input your desired action (call, raise, fold). Keep in mind the spelling, but it is case-insensitive: "
                )
                .lower()
                .strip()
            )
            valid_actions = ["call", "fold", "raise"]
            while action not in valid_actions:
                print("Please input a valid move")
                action = (
                    input(
                        "Please input your desired action (call, raise, fold). Keep in mind the spelling, but it is case-insensitive: "
                    )
                    .lower()
                    .strip()
                )
        elif type == "preflop check":
            print(f"Actions: Check  Raise  Fold")
            action = (
                input(
                    "Please input your desired action (check, raise, fold). Keep in mind the spelling, but it is case-insensitive: "
                )
                .lower()
                .strip()
            )
            valid_actions = ["check", "fold", "raise"]
            while action not in valid_actions:
                print("Please input a valid move")
                action = (
                    input(
                        "Please input your desired action (call, raise, fold). Keep in mind the spelling, but it is case-insensitive: "
                    )
                    .lower()
                    .strip()
                )
        else:
            if current_bet == 0:
                print(
                    f"Actions: Check  Bet(Min: ${self.big_blind_amount}, Max: ${player.money})  Fold"
                )
                action = (
                    input(
                        "Please input your desired action (check, bet, fold). Keep in mind the spelling, but it is case-insensitive: "
                    )
                    .lower()
                    .strip()
                )
                valid_actions = ["check", "bet", "fold"]
                while action not in valid_actions:
                    print("Please input a valid move")
                    action = (
                        input(
                            "Please input your desired action (check, bet, fold). Keep in mind the spelling, but it is case-insensitive: "
                        )
                        .lower()
                        .strip()
                    )
            else:
                print(
                    f"Actions: Call(${current_bet-player_contributions})  Raise  Fold"
                )
                action = (
                    input(
                        "Please input your desired action (call, raise, fold). Keep in mind the spelling, but it is case-insensitive: "
                    )
                    .lower()
                    .strip()
                )
                valid_actions = ["call", "raise", "fold"]
                while action not in valid_actions:
                    print("Please input a valid move")
                    action = (
                        input(
                            "Please input your desired action (call, raise, fold). Keep in mind the spelling, but it is case-insensitive: "
                        )
                        .lower()
                        .strip()
                    )

        return action

    def game_update(
        self, amount, contributions, current_player_index, player
    ):  # Updates the player and pot amount after bettng
        contributions[current_player_index] += amount
        self.pot += amount
        player.money -= amount
        return contributions

    def hand_init(self, preflop):  # Initialise the betting round
        contributions = {
            key: 0
            for key in range(self.player_num)
            if not self.players_list[key].fold_status
        }
        if preflop:
            self.game_update(
                self.small_blind_amount,
                contributions,
                self.small_blind_player,
                self.players_list[self.small_blind_player],
            )
            self.game_update(
                self.big_blind_amount,
                contributions,
                self.big_blind_player,
                self.players_list[self.big_blind_player],
            )
        last_raise_amount = self.big_blind_amount
        return contributions, last_raise_amount, self.utg_player

    def preflop(
        self,
    ):  # This is the logic for the preflop rounds, which is used in self.game as one of the game rounds
        """ "
        Possible Scenarios:
        1. Everyone contributes the same amount
        2. Everyone except one folds
        """
        contributions, last_raise_amount, current_player_index = self.hand_init(
            preflop=True
        )
        current_bet = self.big_blind_amount
        players_played = 0
        while self.active_players > 1 and (
            len(set(contributions.values())) > 1 or players_played < self.active_players
        ):
            player = self.players_list[current_player_index]
            if not player.fold_status:
                player_contributions = contributions[current_player_index]
                if player_contributions < current_bet:
                    action = self.playerUI(
                        player, player_contributions, current_bet, "preflop no check"
                    )
                else:
                    action = self.playerUI(
                        player, player_contributions, current_bet, "preflop check"
                    )
                if action == "fold":
                    del contributions[current_player_index]
                    player.fold_status = True
                    self.active_players -= 1
                elif action == "call":
                    amount = current_bet - player_contributions
                    contributions = self.game_update(
                        amount, contributions, current_player_index, player
                    )
                elif action == "raise":
                    while True:
                        try:
                            raise_to = int(
                                input(
                                    f"Please input the amount you want to raise to (Min: {current_bet + last_raise_amount}, Max: {player_contributions + player.money}): "
                                )
                            )
                            if (
                                current_bet + last_raise_amount
                                <= raise_to
                                <= player_contributions + player.money
                            ):
                                break
                            else:
                                print(
                                    "Please input a valid amount within the allowed range."
                                )
                        except ValueError:
                            print("Please input a number")
                    last_raise_amount = raise_to - current_bet
                    current_bet = raise_to
                    amount = current_bet - player_contributions
                    contributions = self.game_update(
                        amount, contributions, current_player_index, player
                    )
                players_played += 1
            current_player_index = (current_player_index + 1) % self.player_num

    def postflop(self):
        """
        Possible Scenarios:
        1. Everyone checks
        2. Everyone contributes the same amount
        3. Everyone except one folds
        """
        contributions, last_raise_amount, current_player_index = self.hand_init(
            preflop=False
        )
        current_bet = 0
        players_played = 0
        while self.active_players > 1 and (
            len(set(contributions.values())) > 1 or players_played < self.active_players
        ):
            player = self.players_list[current_player_index]
            if not player.fold_status:
                player_contributions = contributions[current_player_index]
                if player_contributions < current_bet or current_bet == 0:
                    action = self.playerUI(
                        player, player_contributions, current_bet, "postflop"
                    )
                else:
                    action = ""
                if action == "bet":
                    while True:
                        try:
                            current_bet = int(
                                input(
                                    f"Please input the amount you want to bet (Min: {last_raise_amount}, Max: {player.money})"
                                )
                            )
                            if last_raise_amount <= current_bet <= player.money:
                                break
                            else:
                                print("Please input a valid bet amount")
                        except ValueError:
                            print("Please input a number")
                    last_raise_amount = current_bet
                    contributions = self.game_update(
                        current_bet, contributions, current_player_index, player
                    )
                elif action == "fold":
                    del contributions[current_player_index]
                    player.fold_status = True
                    self.active_players -= 1
                elif action == "call":
                    amount = current_bet - player_contributions
                    contributions = self.game_update(
                        amount, contributions, current_player_index, player
                    )
                elif action == "raise":
                    while True:
                        try:
                            raise_to = int(
                                input(
                                    f"Please input the amount you want to raise to (Min: {current_bet + last_raise_amount}, Max: {player_contributions + player.money}): "
                                )
                            )
                            if (
                                current_bet + last_raise_amount
                                <= raise_to
                                <= player_contributions + player.money
                            ):
                                break
                            else:
                                print(
                                    "Please input a valid amount within the allowed range."
                                )
                        except ValueError:
                            print("Please input a number")
                    last_raise_amount = raise_to - current_bet
                    current_bet = raise_to
                    amount = current_bet - player_contributions
                    contributions = self.game_update(
                        amount, contributions, current_player_index, player
                    )
                players_played += 1
            current_player_index = (current_player_index + 1) % self.player_num

    def player_num_init(
        self,
    ):  # Check if the number of players is valid and initialises it at the beginning of everything
        while True:
            try:
                self.player_num = int(
                    input("Please input the number of players you want (3-10): ")
                )
                if 3 <= self.player_num <= 10:
                    break
                else:
                    print("Please input a valid number of players")
            except ValueError:
                print("Please input a number")

    def blinds_init(
        self,
    ):  # Check if the blind amount is valid and intialises it as the beginning of everything
        while True:
            try:
                self.big_blind_amount = int(
                    input(
                        "Please input your big blind (Must be bigger than or equal to 2): "
                    )
                )
                if self.big_blind_amount >= 2:
                    break
                else:
                    print("Your big blind is too small")
            except ValueError:
                print("Please input a number")
        self.small_blind_amount = self.big_blind_amount // 2

    def __str__(self):
        return "Hi! This is the poker game object."

    def __repr__(self):
        return str(self)


class HandEvaluator:
    rank_to_value = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "Jack": 11,
        "Queen": 12,
        "King": 13,
        "Ace": 14,
    }

    def __init__(self, player_cards_dict, community_cards):
        self.player_cards_dict = player_cards_dict
        self.community_cards = community_cards

    def add_winner(
        self,
        winners_list,
        winners_hand_score,
        hand_score,
        player_index,
        card_ranks,
    ):
        if hand_score > winners_hand_score:
            winners_list = [{player_index: card_ranks}]
            winners_hand_score = hand_score
        elif hand_score == winners_hand_score:
            winners_list.append({player_index: card_ranks})
        return winners_hand_score, winners_list

    def evaluate(self):
        winners_hand_score = -1
        winners_list = []
        for player_index, player_cards in self.player_cards_dict.items():
            cards = self.community_cards + player_cards
            card_combinations = combinations(cards, 5)
            for card_combination in card_combinations:
                card_ranks = [
                    self.rank_to_value[card.rank] for card in card_combination
                ]
                card_suits = [card.suit for card in card_combination]
                if self.is_straight(card_ranks) and self.is_flush(
                    card_suits
                ):  # Check for straight flush
                    winners_hand_score, winners_list = self.add_winner(
                        winners_list,
                        winners_hand_score,
                        8,
                        player_index,
                        card_ranks,
                    )
                elif self.card_frequency_check(
                    card_ranks, 4
                ):  # Check for four of a kind
                    winners_hand_score, winners_list = self.add_winner(
                        winners_list,
                        winners_hand_score,
                        7,
                        player_index,
                        card_ranks,
                    )
                elif self.card_frequency_check(
                    card_ranks, 3
                ) and self.card_frequency_check(
                    card_ranks, 2
                ):  # Check for full house
                    winners_hand_score, winners_list = self.add_winner(
                        winners_list,
                        winners_hand_score,
                        6,
                        player_index,
                        card_ranks,
                    )
                elif self.is_flush(card_suits):  # Check for flush
                    winners_hand_score, winners_list = self.add_winner(
                        winners_list,
                        winners_hand_score,
                        5,
                        player_index,
                        card_ranks,
                    )
                elif self.is_straight(card_ranks):  # Check for straight
                    winners_hand_score, winners_list = self.add_winner(
                        winners_list,
                        winners_hand_score,
                        4,
                        player_index,
                        card_ranks,
                    )
                elif self.card_frequency_check(
                    card_ranks, 3
                ):  # Check for three of a kind
                    winners_hand_score, winners_list = self.add_winner(
                        winners_list,
                        winners_hand_score,
                        3,
                        player_index,
                        card_ranks,
                    )
                elif self.two_pair_check(card_ranks):  # Check for two pair
                    winners_hand_score, winners_list = self.add_winner(
                        winners_list,
                        winners_hand_score,
                        2,
                        player_index,
                        card_ranks,
                    )
                elif self.card_frequency_check(card_ranks, 2):  # Check for one pair
                    winners_hand_score, winners_list = self.add_winner(
                        winners_list,
                        winners_hand_score,
                        1,
                        player_index,
                        card_ranks,
                    )
                else:  # You got high card
                    winners_hand_score, winners_list = self.add_winner(
                        winners_list,
                        winners_hand_score,
                        0,
                        player_index,
                        card_ranks,
                    )

        if len(winners_list) == 1:
            return next(iter(winners_list[0]))
        else:
            return self.winner_tiebreaker(self, winners_list)

    def is_straight(self, card_ranks):
        card_ranks = sorted(card_ranks)
        return all(
            card_ranks[card + 1] == card_ranks[card] + 1
            for card in range(len(card_ranks) - 1)
        )

    def is_flush(self, card_suits):
        return len(set(card_suits)) == 1

    def card_frequency_check(self, card_ranks, frequency_wanted):
        frequencies = {}
        for card_rank in card_ranks:
            frequencies[card_rank] = frequencies.get(card_rank, 0) + 1
        else:
            if frequency_wanted in frequencies.values():
                return True
            else:
                return False

    def two_pair_check(self, card_ranks):
        frequencies = {}
        for card_rank in card_ranks:
            frequencies[card_rank] = frequencies.get(card_rank, 0) + 1
        two_count = 0
        for frequency in frequencies.values():
            if frequency == 2:
                two_count += 1
        return two_count == 2

    def highest_card_tiebreaker(self, card_ranks, player_index):
        sorted_ranks = [player_index]
        sorted_ranks += sorted(set(card_ranks), reverse=True)
        return sorted_ranks

    def n_of_a_kind_tiebreaker(self, card_ranks, player_index, frequency):
        sorted_ranks = [player_index]
        frequencies = {}
        for card_rank in card_ranks:
            frequencies[card_rank] = frequencies.get(card_rank, 0) + 1 # {3: 1, 13: 2, 4: 1, 5: 1}
        for rank in frequencies:
            if frequencies[rank] == frequency:
                sorted_ranks.append(rank)
                card_ranks = list(card_ranks.keys()).remove(rank)
                break
        sorted_ranks += sorted(set(card_ranks, reverse=True))
        return sorted_ranks

    def two_pair_tiebreaker(self, card_ranks, player_index):
        sorted_ranks = [player_index]
        two_pairs = []
        kicker = []
        frequencies = {}
        for card_rank in card_ranks:
            frequencies[card_rank] = frequencies.get(card_rank, 0) + 1
        for card in frequencies:
            if frequencies[card] == 2:
                two_pairs.append(card)
            else:
                kicker.append(card)
        sorted_ranks += sorted(two_pairs, reverse=True) + kicker
        return sorted_ranks

    def winner_tiebreaker(self, winners_list, winners_hand_score):
        winner = -1
        tie_breaker_comparisons = []
        highest_card_tiebreaker = [8, 5, 4, 0]
        if winners_hand_score in highest_card_tiebreaker:
            for player_dict in winners_list:
                player_index, card_ranks = next(iter(player_dict.items()))
                tie_breaker_comparisons.append(
                    self.highest_card_tiebreaker(card_ranks, player_index)
                )
        elif winners_hand_score == 2:
            for player_dict in winners_list:
                player_index, card_ranks = next(iter(player_dict.items()))
                tie_breaker_comparisons.append(self.two_pair_tiebreaker(card_ranks, player_index))
        else:
            for player_dict in winners_list:
                player_index, card_ranks = next(iter(player_dict.items()))
                if winners_hand_score == 7:
                    frequency = 4
                elif winners_hand_score in [6, 3]:
                    frequency = 3
                else:
                    frequency = 2
                tie_breaker_comparisons.append(self.n_of_a_kind_tiebreaker(card_ranks, player_index, frequency))


def main():
    game = PokerGame()
    game.play()

if __name__ == "__main__":  
    main()
