from poker import HandEvaluator, Card
import pytest



community_cards = [Card("10", "Diamonds"), Card("Queen", "Spades"), Card("8", "Clubs"), Card("9", "Spades"), Card("King", "Clubs")]
active_players_list = {0: [Card("Queen", "Diamonds"), Card("3", "Clubs")], 2: [Card("Jack", "Hearts"), Card("2", "Spades")]}
hand_evaluation = HandEvaluator(active_players_list, community_cards)

def test_is_straight():
    assert hand_evaluation.is_straight([3, 5, 2, 6, 13]) == False
    assert hand_evaluation.is_straight([3, 5, 4, 7, 6]) == True
    assert hand_evaluation.is_straight([10, 13, 14, 12, 11]) == True
    assert hand_evaluation.is_straight([10, 10, 12, 13, 14]) == False

def test_is_flush():
    assert hand_evaluation.is_flush(["Diamonds", "Diamonds", "Diamonds", "Diamonds", "Diamonds"]) == True
    assert hand_evaluation.is_flush(["Diamonds", "Hearts", "Clubs", "Spades", "Hearts"]) == False
    assert hand_evaluation.is_flush(["Hearts", "Hearts", "Hearts", "Hearts", "Hearts"]) == True
    assert hand_evaluation.is_flush(["Hearts", "Clubs", "Hearts", "Hearts", "Hearts"]) == False
    assert hand_evaluation.is_flush(["Clubs", "Clubs", "Clubs", "Clubs", "Clubs"]) == True

def test_is_full_house():
    assert (hand_evaluation.card_frequency_check([5, 2, 2, 5, 4], 3) and hand_evaluation.card_frequency_check([5, 2, 2, 5, 4], 2)) == False
    assert (hand_evaluation.card_frequency_check([5, 2, 5, 2, 5], 3) and hand_evaluation.card_frequency_check([5, 2, 5, 2, 5], 2)) == True
    assert (hand_evaluation.card_frequency_check([1, 1, 3, 4, 5], 3) and hand_evaluation.card_frequency_check([1, 1, 2, 4, 5], 2)) == False
    assert (hand_evaluation.card_frequency_check([2, 14, 2, 14, 14], 3) and hand_evaluation.card_frequency_check([2, 14, 2, 14, 14], 2)) == True

def test_is_four_of_a_kind():
    assert hand_evaluation.card_frequency_check([4, 4, 2, 4, 4], 4) == True
    assert hand_evaluation.card_frequency_check([2, 4, 2, 2, 5], 4) == False
    assert hand_evaluation.card_frequency_check([13, 13, 13, 12, 12], 4) == False
    assert hand_evaluation.card_frequency_check([10, 10, 10, 13, 10], 4) == True
    assert hand_evaluation.card_frequency_check([5, 6, 7, 8, 9], 4) == False
    assert hand_evaluation.card_frequency_check([9, 10, 9, 9, 9], 4) == True
    assert hand_evaluation.card_frequency_check([10, 11, 11, 11, 11], 4) == True

def test_two_pair():
    assert hand_evaluation.two_pair_check([2, 2, 4, 4, 5]) == True
    assert hand_evaluation.two_pair_check([3, 6, 3, 8, 6]) == True
    assert hand_evaluation.two_pair_check([3, 6, 3, 4, 5]) == False
    assert hand_evaluation.two_pair_check([3, 2, 3, 3, 2]) == False
    assert hand_evaluation.two_pair_check([2, 2, 3, 3, 4]) == True
    assert hand_evaluation.two_pair_check([10, 13, 7, 13, 10]) == True
    assert hand_evaluation.two_pair_check([1, 2, 3, 4, 5]) == False
