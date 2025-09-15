import unittest
from core.board import Board
from core.checker import Checker
from core.player import Player

class TestBoard(unittest.TestCase):

    def setUp(self):
        if Board is None or Player is None:
            self.skipTest("Clase Board o Player no implementada aún")
        
        self.__player1__ = Player("Jugador1", "white")
        self.__player2__ = Player("Jugador2", "black")
        self.__board__ = Board()

    def test_board_creation(self):
        board = Board()
        self.assertIsNotNone(board)

    def test_board_has_24_points(self):
        self.assertEqual(len(self.__board__.get_points()), 24)

    def test_board_points_getter(self):
        points = self.__board__.get_points()
        self.assertIsInstance(points, list)
        self.assertEqual(len(points), 24)

    def test_board_initial_setup(self):
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        points = self.__board__.get_points()
        
        self.assertEqual(len(points[0]), 2)
        self.assertEqual(len(points[11]), 5)
        self.assertEqual(len(points[16]), 3)
        self.assertEqual(len(points[18]), 5)

    def test_board_point_is_empty_true(self):
        self.assertTrue(self.__board__.is_point_empty(5))

    def test_board_point_is_empty_false(self):
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        self.assertFalse(self.__board__.is_point_empty(0))

    def test_board_get_point_owner(self):
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        owner = self.__board__.get_point_owner(0)
        self.assertEqual(owner, self.__player1__)

    def test_board_get_point_owner_empty_point(self):
        owner = self.__board__.get_point_owner(5)
        self.assertIsNone(owner)

    def test_board_get_checkers_count_on_point(self):
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        count = self.__board__.get_checkers_count_on_point(0)
        self.assertEqual(count, 2)

    def test_board_get_checkers_count_empty_point(self):
        count = self.__board__.get_checkers_count_on_point(5)
        self.assertEqual(count, 0)

    def test_board_add_checker_to_point(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_point(5, checker)
        self.assertEqual(self.__board__.get_checkers_count_on_point(5), 1)

    def test_board_remove_checker_from_point(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_point(5, checker)
        removed_checker = self.__board__.remove_checker_from_point(5)
        self.assertEqual(removed_checker, checker)
        self.assertEqual(self.__board__.get_checkers_count_on_point(5), 0)

    def test_board_remove_checker_from_empty_point(self):
        with self.assertRaises(ValueError):
            self.__board__.remove_checker_from_point(5)

    def test_board_can_place_checker_on_empty_point(self):
        self.assertTrue(self.__board__.can_place_checker(5, self.__player1__))

    def test_board_can_place_checker_on_own_point(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_point(5, checker)
        self.assertTrue(self.__board__.can_place_checker(5, self.__player1__))

    def test_board_can_place_checker_on_opponent_single(self):
        checker = Checker(self.__player2__)
        self.__board__.add_checker_to_point(5, checker)
        self.assertTrue(self.__board__.can_place_checker(5, self.__player1__))

    def test_board_cannot_place_checker_on_opponent_multiple(self):
        checker1 = Checker(self.__player2__)
        checker2 = Checker(self.__player2__)
        self.__board__.add_checker_to_point(5, checker1)
        self.__board__.add_checker_to_point(5, checker2)
        self.assertFalse(self.__board__.can_place_checker(5, self.__player1__))

    def test_board_is_point_blocked_true(self):
        checker1 = Checker(self.__player2__)
        checker2 = Checker(self.__player2__)
        self.__board__.add_checker_to_point(5, checker1)
        self.__board__.add_checker_to_point(5, checker2)
        self.assertTrue(self.__board__.is_point_blocked(5, self.__player1__))

    def test_board_is_point_blocked_false(self):
        self.assertFalse(self.__board__.is_point_blocked(5, self.__player1__))

    def test_board_has_blot_true(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_point(5, checker)
        self.assertTrue(self.__board__.has_blot(5))

    def test_board_has_blot_false_empty(self):
        self.assertFalse(self.__board__.has_blot(5))

    def test_board_has_blot_false_multiple(self):
        checker1 = Checker(self.__player1__)
        checker2 = Checker(self.__player1__)
        self.__board__.add_checker_to_point(5, checker1)
        self.__board__.add_checker_to_point(5, checker2)
        self.assertFalse(self.__board__.has_blot(5))

    def test_board_can_hit_blot_true(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_point(5, checker)
        self.assertTrue(self.__board__.can_hit_blot(5, self.__player2__))

    def test_board_can_hit_blot_false_own_checker(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_point(5, checker)
        self.assertFalse(self.__board__.can_hit_blot(5, self.__player1__))

    def test_board_can_hit_blot_false_multiple_checkers(self):
        checker1 = Checker(self.__player1__)
        checker2 = Checker(self.__player1__)
        self.__board__.add_checker_to_point(5, checker1)
        self.__board__.add_checker_to_point(5, checker2)
        self.assertFalse(self.__board__.can_hit_blot(5, self.__player2__))

    def test_board_hit_blot(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_point(5, checker)
        hit_checker = self.__board__.hit_blot(5, self.__player2__)
        self.assertEqual(hit_checker, checker)
        self.assertTrue(self.__board__.is_point_empty(5))

    def test_board_hit_blot_invalid(self):
        with self.assertRaises(ValueError):
            self.__board__.hit_blot(5, self.__player1__)

    def test_board_get_bar_checkers_count_initial(self):
        self.assertEqual(self.__board__.get_bar_checkers_count(self.__player1__), 0)

    def test_board_add_checker_to_bar(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_bar(checker)
        self.assertEqual(self.__board__.get_bar_checkers_count(self.__player1__), 1)

    def test_board_remove_checker_from_bar(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_bar(checker)
        removed_checker = self.__board__.remove_checker_from_bar(self.__player1__)
        self.assertEqual(removed_checker, checker)
        self.assertEqual(self.__board__.get_bar_checkers_count(self.__player1__), 0)

    def test_board_remove_checker_from_empty_bar(self):
        with self.assertRaises(ValueError):
            self.__board__.remove_checker_from_bar(self.__player1__)

    def test_board_has_checkers_on_bar_true(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_bar(checker)
        self.assertTrue(self.__board__.has_checkers_on_bar(self.__player1__))

    def test_board_has_checkers_on_bar_false(self):
        self.assertFalse(self.__board__.has_checkers_on_bar(self.__player1__))

    def test_board_get_off_board_checkers_count_initial(self):
        self.assertEqual(self.__board__.get_off_board_checkers_count(self.__player1__), 0)

    def test_board_add_checker_off_board(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_off_board(checker)
        self.assertEqual(self.__board__.get_off_board_checkers_count(self.__player1__), 1)

    def test_board_is_valid_point_true(self):
        self.assertTrue(self.__board__.is_valid_point(0))
        self.assertTrue(self.__board__.is_valid_point(23))

    def test_board_is_valid_point_false(self):
        self.assertFalse(self.__board__.is_valid_point(-1))
        self.assertFalse(self.__board__.is_valid_point(24))

    def test_board_get_opposite_point(self):
        self.assertEqual(self.__board__.get_opposite_point(0), 23)
        self.assertEqual(self.__board__.get_opposite_point(23), 0)
        self.assertEqual(self.__board__.get_opposite_point(12), 11)

    def test_board_is_in_home_board_white_true(self):
        self.assertTrue(self.__board__.is_in_home_board(19, self.__player1__))
        self.assertTrue(self.__board__.is_in_home_board(23, self.__player1__))

    def test_board_is_in_home_board_white_false(self):
        self.assertFalse(self.__board__.is_in_home_board(18, self.__player1__))
        self.assertFalse(self.__board__.is_in_home_board(0, self.__player1__))

    def test_board_is_in_home_board_black_true(self):
        self.assertTrue(self.__board__.is_in_home_board(0, self.__player2__))
        self.assertTrue(self.__board__.is_in_home_board(5, self.__player2__))

    def test_board_is_in_home_board_black_false(self):
        self.assertFalse(self.__board__.is_in_home_board(6, self.__player2__))
        self.assertFalse(self.__board__.is_in_home_board(23, self.__player2__))

    def test_board_can_bear_off_true(self):
        for i in range(19, 24):
            checker = Checker(self.__player1__)
            self.__board__.add_checker_to_point(i, checker)
        self.assertTrue(self.__board__.can_bear_off(self.__player1__))

    def test_board_can_bear_off_false_checkers_outside_home(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_point(18, checker)
        self.assertFalse(self.__board__.can_bear_off(self.__player1__))

    def test_board_can_bear_off_false_checkers_on_bar(self):
        checker = Checker(self.__player1__)
        self.__board__.add_checker_to_bar(checker)
        self.assertFalse(self.__board__.can_bear_off(self.__player1__))

    def test_board_get_furthest_checker_white(self):
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        furthest = self.__board__.get_furthest_checker(self.__player1__)
        self.assertEqual(furthest, 0)

    def test_board_get_furthest_checker_black(self):
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        furthest = self.__board__.get_furthest_checker(self.__player2__)
        self.assertEqual(furthest, 23)

    def test_board_get_furthest_checker_no_checkers(self):
        furthest = self.__board__.get_furthest_checker(self.__player1__)
        self.assertIsNone(furthest)

    def test_board_count_checkers_on_board(self):
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        count = self.__board__.count_checkers_on_board(self.__player1__)
        self.assertEqual(count, 15)

    def test_board_count_checkers_on_board_empty(self):
        count = self.__board__.count_checkers_on_board(self.__player1__)
        self.assertEqual(count, 0)

    def test_board_get_all_checker_positions(self):
        checker1 = Checker(self.__player1__)
        checker2 = Checker(self.__player1__)
        self.__board__.add_checker_to_point(5, checker1)
        self.__board__.add_checker_to_point(10, checker2)
        
        positions = self.__board__.get_all_checker_positions(self.__player1__)
        self.assertIn(5, positions)
        self.assertIn(10, positions)
        self.assertEqual(len(positions), 2)

    def test_board_clear_point(self):
        checker1 = Checker(self.__player1__)
        checker2 = Checker(self.__player1__)
        self.__board__.add_checker_to_point(5, checker1)
        self.__board__.add_checker_to_point(5, checker2)
        
        cleared_checkers = self.__board__.clear_point(5)
        self.assertEqual(len(cleared_checkers), 2)
        self.assertTrue(self.__board__.is_point_empty(5))

    def test_board_clear_empty_point(self):
        cleared_checkers = self.__board__.clear_point(5)
        self.assertEqual(len(cleared_checkers), 0)

    def test_board_reset_board(self):
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        self.__board__.reset()
        
        for i in range(24):
            self.assertTrue(self.__board__.is_point_empty(i))
        
        self.assertEqual(self.__board__.get_bar_checkers_count(self.__player1__), 0)
        self.assertEqual(self.__board__.get_bar_checkers_count(self.__player2__), 0)

    def test_board_copy_board(self):
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        board_copy = self.__board__.copy()
        
        self.assertIsNot(board_copy, self.__board__)
        self.assertEqual(board_copy.get_checkers_count_on_point(0), 
                        self.__board__.get_checkers_count_on_point(0))

    def test_board_string_representation(self):
        board_str = str(self.__board__)
        self.assertIsInstance(board_str, str)
        self.assertTrue(len(board_str) > 0)

    def test_board_equality_same_board(self):
        self.assertEqual(self.__board__, self.__board__)

    def test_board_equality_different_boards(self):
        board2 = Board()
        checker = Checker(self.__player1__)
        board2.add_checker_to_point(5, checker)
        self.assertNotEqual(self.__board__, board2)

    def test_board_equality_same_configuration(self):
        board2 = Board()
        self.assertEqual(self.__board__, board2)

    def test_board_hash_consistency(self):
        hash1 = hash(self.__board__)
        hash2 = hash(self.__board__)
        self.assertEqual(hash1, hash2)

    def test_board_invalid_point_operations(self):
        with self.assertRaises(ValueError):
            self.__board__.get_checkers_count_on_point(-1)
        
        with self.assertRaises(ValueError):
            self.__board__.get_checkers_count_on_point(24)

    def test_board_pip_count_calculation(self):
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        pip_count = self.__board__.calculate_pip_count(self.__player1__)
        self.assertIsInstance(pip_count, int)
        self.assertGreater(pip_count, 0)

    def test_board_pip_count_empty_board(self):
        pip_count = self.__board__.calculate_pip_count(self.__player1__)
        self.assertEqual(pip_count, 0)

    def test_board_get_moves_to_bear_off(self):
        for i in range(19, 24):
            checker = Checker(self.__player1__)
            self.__board__.add_checker_to_point(i, checker)
        
        moves = self.__board__.get_moves_to_bear_off(self.__player1__)
        self.assertIsInstance(moves, list)

    def test_board_is_race_position_true(self):
        for i in range(19, 24):
            checker = Checker(self.__player1__)
            self.__board__.add_checker_to_point(i, checker)
        
        for i in range(0, 6):
            checker = Checker(self.__player2__)
            self.__board__.add_checker_to_point(i, checker)
        
        self.assertTrue(self.__board__.is_race_position())

    def test_board_is_race_position_false(self):
        self.__board__.setup_initial_position(self.__player1__, self.__player2__)
        self.assertFalse(self.__board__.is_race_position())

if __name__ == '__main__':
    unittest.main()