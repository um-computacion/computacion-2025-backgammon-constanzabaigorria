import unittest
from unittest.mock import patch
from core.dice import Dice


class TestDice(unittest.TestCase):
    
    def setUp(self):
        self.dice = Dice()
    
    @patch('random.randint', side_effect=[3, 5])
    def test_roll_returns_tuple(self, mock_randint):
        result = self.dice.roll()
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, (3, 5))
        self.assertEqual(mock_randint.call_count, 2)
    
    @patch('random.randint', side_effect=[1, 1])
    def test_roll_double_ones(self, mock_randint):
        result = self.dice.roll()
        
        self.assertEqual(result, (1, 1))
        self.assertTrue(self.dice.is_double(result))
        mock_randint.assert_any_call(1, 6)
    
    @patch('random.randint', side_effect=[6, 6])
    def test_roll_double_sixes(self, mock_randint):
        result = self.dice.roll()
        
        self.assertEqual(result, (6, 6))
        self.assertTrue(self.dice.is_double(result))
        self.assertEqual(mock_randint.call_count, 2)
    
    @patch('random.randint', side_effect=[2, 4])
    def test_roll_different_values(self, mock_randint):
        result = self.dice.roll()
        
        self.assertEqual(result, (2, 4))
        self.assertFalse(self.dice.is_double(result))
        self.assertTrue(mock_randint.called)
    
    @patch('random.randint', side_effect=[1, 3, 2, 6, 5, 4])
    def test_multiple_rolls(self, mock_randint):
        
        result1 = self.dice.roll()
        self.assertEqual(result1, (1, 3))
        
        result2 = self.dice.roll()
        self.assertEqual(result2, (2, 6))
        
        result3 = self.dice.roll()
        self.assertEqual(result3, (5, 4))
        
        self.assertEqual(mock_randint.call_count, 6)
    
    def test_is_double_with_doubles(self):
        double_cases = [
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)
        ]
        
        for double_roll in double_cases:
            with self.subTest(roll=double_roll):
                self.assertTrue(self.dice.is_double(double_roll))
    
    def test_is_double_with_non_doubles(self):
        non_double_cases = [
            (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
            (2, 3), (2, 4), (2, 5), (2, 6),
            (3, 4), (3, 5), (3, 6),
            (4, 5), (4, 6),
            (5, 6)
        ]
        
        for non_double_roll in non_double_cases:
            with self.subTest(roll=non_double_roll):
                self.assertFalse(self.dice.is_double(non_double_roll))
    
    def test_get_moves_regular_roll(self):
        test_cases = [
            ((1, 2), [1, 2]),
            ((3, 4), [3, 4]),
            ((2, 6), [2, 6]),
            ((5, 1), [5, 1]),
            ((6, 3), [6, 3]),
            ((4, 5), [4, 5])
        ]
        
        for roll_result, expected_moves in test_cases:
            with self.subTest(roll=roll_result):
                moves = self.dice.get_moves(roll_result)
                self.assertEqual(len(moves), 2)
                self.assertEqual(sorted(moves), sorted(expected_moves))
    
    def test_get_moves_double_roll(self):
        for value in range(1, 7):
            with self.subTest(value=value):
                double_roll = (value, value)
                moves = self.dice.get_moves(double_roll)
                
                self.assertEqual(len(moves), 4)
                self.assertEqual(moves, [value, value, value, value])
                self.assertTrue(all(move == value for move in moves))
    
    @patch('random.randint', side_effect=[4, 4])
    def test_complete_workflow_double(self, mock_randint):
        result = self.dice.roll()
        self.assertEqual(result, (4, 4))
        
        is_double = self.dice.is_double(result)
        self.assertTrue(is_double)
        
        moves = self.dice.get_moves(result)
        self.assertEqual(moves, [4, 4, 4, 4])
        self.assertEqual(len(moves), 4)
        
        self.assertEqual(mock_randint.call_count, 2)
    
    @patch('random.randint', side_effect=[3, 6])
    def test_complete_workflow_regular(self, mock_randint):
        result = self.dice.roll()
        self.assertEqual(result, (3, 6))
        
        is_double = self.dice.is_double(result)
        self.assertFalse(is_double)
        
        moves = self.dice.get_moves(result)
        self.assertEqual(sorted(moves), sorted([3, 6]))
        self.assertEqual(len(moves), 2)
        
        self.assertEqual(mock_randint.call_count, 2)
    
    def test_dice_initialization(self):
        dice = Dice()
        self.assertIsInstance(dice, Dice)
    
    @patch('random.randint', side_effect=[1, 6, 3, 3, 2, 5])
    def test_edge_cases_sequence(self, mock_randint):

        result1 = self.dice.roll()
        self.assertEqual(result1, (1, 6))
        self.assertFalse(self.dice.is_double(result1))
        moves1 = self.dice.get_moves(result1)
        self.assertEqual(sorted(moves1), [1, 6])
        
        result2 = self.dice.roll()
        self.assertEqual(result2, (3, 3))
        self.assertTrue(self.dice.is_double(result2))
        moves2 = self.dice.get_moves(result2)
        self.assertEqual(moves2, [3, 3, 3, 3])

        result3 = self.dice.roll()
        self.assertEqual(result3, (2, 5))
        self.assertFalse(self.dice.is_double(result3))
        moves3 = self.dice.get_moves(result3)
        self.assertEqual(sorted(moves3), [2, 5])
        
        self.assertEqual(mock_randint.call_count, 6)
    
    def test_get_moves_preserves_order_for_regular_rolls(self):
        test_cases = [
            (1, 6),
            (6, 1),
            (2, 5),
            (5, 2),
            (3, 4),
            (4, 3)
        ]
        
        for die1, die2 in test_cases:
            with self.subTest(roll=(die1, die2)):
                moves = self.dice.get_moves((die1, die2))
                self.assertEqual(moves, [die1, die2])
    
    @patch('random.randint', side_effect=Exception("Random generator failed"))
    def test_roll_with_exception(self, mock_randint):
        with self.assertRaises(Exception) as context:
            self.dice.roll()
        
        self.assertEqual(str(context.exception), "Random generator failed")
        self.assertTrue(mock_randint.called)
    
    def test_get_last_roll_before_rolling(self):
        pass
    
    def test_get_sides_count(self):
        with patch('random.randint', side_effect=[1, 2, 3, 4, 5, 6, 1, 6]):
            for _ in range(4):
                result = self.dice.roll()
                self.assertTrue(1 <= result[0] <= 6)
                self.assertTrue(1 <= result[1] <= 6)


if __name__ == "__main__":
    unittest.main()

