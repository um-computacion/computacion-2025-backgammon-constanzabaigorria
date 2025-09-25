import unittest
from core.checker import Checker
from core.player import Player


class TestChecker(unittest.TestCase):

    def setUp(self):
        if Checker is None or Player is None:
            self.skipTest("Clase Checker o Player no implementada aún")
        
        self.__player1__ = Player("Jugador1", "white")
        self.__player2__ = Player("Jugador2", "black")
        self.__checker1__ = Checker(self.__player1__)
        self.__checker2__ = Checker(self.__player2__)

    def test_checker_creation_with_player(self):
        checker = Checker(self.__player1__)
        self.assertEqual(checker.get_owner(), self.__player1__)

    def test_checker_owner_getter(self):
        self.assertEqual(self.__checker1__.get_owner(), self.__player1__)

    def test_checker_owner_setter(self):
        self.__checker1__.set_owner(self.__player2__)
        self.assertEqual(self.__checker1__.get_owner(), self.__player2__)

    def test_checker_color_from_owner(self):
        self.assertEqual(self.__checker1__.get_color(), "white")
        self.assertEqual(self.__checker2__.get_color(), "black")

    def test_checker_position_initial(self):
        self.assertIsNone(self.__checker1__.get_position())

    def test_checker_position_getter(self):
        position = self.__checker1__.get_position()
        self.assertIsInstance(position, (int, type(None)))

    def test_checker_position_setter(self):
        self.__checker1__.set_position(5)
        self.assertEqual(self.__checker1__.get_position(), 5)

    def test_checker_position_setter_none(self):
        self.__checker1__.set_position(None)
        self.assertIsNone(self.__checker1__.get_position())

    def test_checker_is_on_board_true(self):
        self.__checker1__.set_position(5)
        self.assertTrue(self.__checker1__.is_on_board())

    def test_checker_is_on_board_false(self):
        self.assertFalse(self.__checker1__.is_on_board())

    def test_checker_is_on_bar_initial(self):
        self.assertFalse(self.__checker1__.is_on_bar())

    def test_checker_is_on_bar_getter(self):
        is_on_bar = self.__checker1__.is_on_bar()
        self.assertIsInstance(is_on_bar, bool)

    def test_checker_is_on_bar_setter_true(self):
        self.__checker1__.set_on_bar(True)
        self.assertTrue(self.__checker1__.is_on_bar())

    def test_checker_is_on_bar_setter_false(self):
        self.__checker1__.set_on_bar(True)
        self.__checker1__.set_on_bar(False)
        self.assertFalse(self.__checker1__.is_on_bar())

    def test_checker_is_off_board_initial(self):
        self.assertFalse(self.__checker1__.is_off_board())

    def test_checker_is_off_board_getter(self):
        is_off_board = self.__checker1__.is_off_board()
        self.assertIsInstance(is_off_board, bool)

    def test_checker_is_off_board_setter_true(self):
        self.__checker1__.set_off_board(True)
        self.assertTrue(self.__checker1__.is_off_board())

    def test_checker_is_off_board_setter_false(self):
        self.__checker1__.set_off_board(True)
        self.__checker1__.set_off_board(False)
        self.assertFalse(self.__checker1__.is_off_board())

    def test_checker_move_to_position(self):
        self.__checker1__.move_to_position(10)
        self.assertEqual(self.__checker1__.get_position(), 10)
        self.assertTrue(self.__checker1__.is_on_board())
        self.assertFalse(self.__checker1__.is_on_bar())
        self.assertFalse(self.__checker1__.is_off_board())

    def test_checker_move_to_bar(self):
        self.__checker1__.set_position(5)
        self.__checker1__.move_to_bar()
        self.assertIsNone(self.__checker1__.get_position())
        self.assertFalse(self.__checker1__.is_on_board())
        self.assertTrue(self.__checker1__.is_on_bar())
        self.assertFalse(self.__checker1__.is_off_board())

    def test_checker_move_off_board(self):
        self.__checker1__.set_position(23)
        self.__checker1__.move_off_board()
        self.assertIsNone(self.__checker1__.get_position())
        self.assertFalse(self.__checker1__.is_on_board())
        self.assertFalse(self.__checker1__.is_on_bar())
        self.assertTrue(self.__checker1__.is_off_board())

    def test_checker_can_move_to_position_true(self):
        self.__checker1__.set_position(5)
        self.assertTrue(self.__checker1__.can_move_to_position(10))

    def test_checker_can_move_to_position_false_same_position(self):
        self.__checker1__.set_position(5)
        self.assertFalse(self.__checker1__.can_move_to_position(5))

    def test_checker_can_move_to_position_false_invalid_position(self):
        self.__checker1__.set_position(5)
        self.assertFalse(self.__checker1__.can_move_to_position(-1))
        self.assertFalse(self.__checker1__.can_move_to_position(24))

    def test_checker_can_move_to_position_from_bar(self):
        self.__checker1__.move_to_bar()
        self.assertTrue(self.__checker1__.can_move_to_position(5))

    def test_checker_can_move_to_position_off_board(self):
        self.__checker1__.move_off_board()
        self.assertFalse(self.__checker1__.can_move_to_position(5))

    def test_checker_get_distance_to_position(self):
        self.__checker1__.set_position(5)
        distance = self.__checker1__.get_distance_to_position(10)
        self.assertEqual(distance, 5)

    def test_checker_get_distance_to_position_negative(self):
        self.__checker1__.set_position(10)
        distance = self.__checker1__.get_distance_to_position(5)
        self.assertEqual(distance, -5)

    def test_checker_get_distance_to_position_from_none(self):
        distance = self.__checker1__.get_distance_to_position(5)
        self.assertIsNone(distance)

    def test_checker_is_blot_true(self):
        self.__checker1__.set_position(5)
        self.assertTrue(self.__checker1__.is_blot())

    def test_checker_is_blot_false_not_on_board(self):
        self.assertFalse(self.__checker1__.is_blot())

    def test_checker_can_be_hit_true(self):
        self.__checker1__.set_position(5)
        self.assertTrue(self.__checker1__.can_be_hit(self.__player2__))

    def test_checker_can_be_hit_false_same_player(self):
        self.__checker1__.set_position(5)
        self.assertFalse(self.__checker1__.can_be_hit(self.__player1__))

    def test_checker_can_be_hit_false_not_on_board(self):
        self.assertFalse(self.__checker1__.can_be_hit(self.__player2__))

    def test_checker_hit_by_opponent(self):
        self.__checker1__.set_position(5)
        self.__checker1__.hit_by_opponent()
        self.assertTrue(self.__checker1__.is_on_bar())
        self.assertFalse(self.__checker1__.is_on_board())

    def test_checker_hit_by_opponent_not_on_board(self):
        with self.assertRaises(ValueError):
            self.__checker1__.hit_by_opponent()

    def test_checker_reset_position(self):
        self.__checker1__.set_position(5)
        self.__checker1__.set_on_bar(True)
        self.__checker1__.set_off_board(True)
        
        self.__checker1__.reset_position()
        
        self.assertIsNone(self.__checker1__.get_position())
        self.assertFalse(self.__checker1__.is_on_bar())
        self.assertFalse(self.__checker1__.is_off_board())

    def test_checker_is_in_home_board_white_true(self):
        self.__checker1__.set_position(20)
        self.assertTrue(self.__checker1__.is_in_home_board())

    def test_checker_is_in_home_board_white_false(self):
        self.__checker1__.set_position(18)
        self.assertFalse(self.__checker1__.is_in_home_board())

    def test_checker_is_in_home_board_black_true(self):
        self.__checker2__.set_position(3)
        self.assertTrue(self.__checker2__.is_in_home_board())

    def test_checker_is_in_home_board_black_false(self):
        self.__checker2__.set_position(6)
        self.assertFalse(self.__checker2__.is_in_home_board())

    def test_checker_is_in_home_board_not_on_board(self):
        self.assertFalse(self.__checker1__.is_in_home_board())

    def test_checker_can_bear_off_true(self):
        self.__checker1__.set_position(23)
        self.assertTrue(self.__checker1__.can_bear_off())

    def test_checker_can_bear_off_false_not_in_home(self):
        self.__checker1__.set_position(18)
        self.assertFalse(self.__checker1__.can_bear_off())

    def test_checker_can_bear_off_false_not_on_board(self):
        self.assertFalse(self.__checker1__.can_bear_off())

    def test_checker_get_pip_value_white(self):
        self.__checker1__.set_position(5)
        pip_value = self.__checker1__.get_pip_value()
        self.assertEqual(pip_value, 19)

    def test_checker_get_pip_value_black(self):
        self.__checker2__.set_position(5)
        pip_value = self.__checker2__.get_pip_value()
        self.assertEqual(pip_value, 6)

    def test_checker_get_pip_value_not_on_board(self):
        pip_value = self.__checker1__.get_pip_value()
        self.assertEqual(pip_value, 0)

    def test_checker_get_direction_white(self):
        direction = self.__checker1__.get_direction()
        self.assertEqual(direction, -1)

    def test_checker_get_direction_black(self):
        direction = self.__checker2__.get_direction()
        self.assertEqual(direction, 1)

    def test_checker_is_moving_forward_white_true(self):
        self.__checker1__.set_position(10)
        self.assertTrue(self.__checker1__.is_moving_forward(5))

    def test_checker_is_moving_forward_white_false(self):
        self.__checker1__.set_position(5)
        self.assertFalse(self.__checker1__.is_moving_forward(10))

    def test_checker_is_moving_forward_black_true(self):
        self.__checker2__.set_position(5)
        self.assertTrue(self.__checker2__.is_moving_forward(10))

    def test_checker_is_moving_forward_black_false(self):
        self.__checker2__.set_position(10)
        self.assertFalse(self.__checker2__.is_moving_forward(5))

    def test_checker_is_moving_forward_not_on_board(self):
        with self.assertRaises(ValueError):
            self.__checker1__.is_moving_forward(5)

    def test_checker_clone(self):
        self.__checker1__.set_position(5)
        self.__checker1__.set_on_bar(True)
        
        cloned_checker = self.__checker1__.clone()
        
        self.assertIsNot(cloned_checker, self.__checker1__)
        self.assertEqual(cloned_checker.get_owner(), self.__checker1__.get_owner())
        self.assertEqual(cloned_checker.get_position(), self.__checker1__.get_position())
        self.assertEqual(cloned_checker.is_on_bar(), self.__checker1__.is_on_bar())

    def test_checker_string_representation(self):
        self.__checker1__.set_position(5)
        expected = "Checker(owner=Jugador1, color=white, position=5)"
        self.assertEqual(str(self.__checker1__), expected)

    def test_checker_string_representation_on_bar(self):
        self.__checker1__.move_to_bar()
        expected = "Checker(owner=Jugador1, color=white, position=BAR)"
        self.assertEqual(str(self.__checker1__), expected)

    def test_checker_string_representation_off_board(self):
        self.__checker1__.move_off_board()
        expected = "Checker(owner=Jugador1, color=white, position=OFF)"
        self.assertEqual(str(self.__checker1__), expected)

    def test_checker_equality_same_checker(self):
        self.assertEqual(self.__checker1__, self.__checker1__)

    def test_checker_equality_different_checkers_same_attributes(self):
        checker3 = Checker(self.__player1__)
        checker3.set_position(5)
        self.__checker1__.set_position(5)
        self.assertEqual(self.__checker1__, checker3)

    def test_checker_equality_different_checkers_different_attributes(self):
        self.__checker1__.set_position(5)
        self.__checker2__.set_position(10)
        self.assertNotEqual(self.__checker1__, self.__checker2__)

    def test_checker_hash_consistency(self):
        self.__checker1__.set_position(5)
        hash1 = hash(self.__checker1__)
        hash2 = hash(self.__checker1__)
        self.assertEqual(hash1, hash2)

    def test_checker_invalid_owner(self):
        with self.assertRaises(ValueError):
            Checker(None)

    def test_checker_invalid_position_negative(self):
        with self.assertRaises(ValueError):
            self.__checker1__.set_position(-1)

    def test_checker_invalid_position_too_high(self):
        with self.assertRaises(ValueError):
            self.__checker1__.set_position(24)

    def test_checker_invalid_owner_setter(self):
        with self.assertRaises(ValueError):
            self.__checker1__.set_owner(None)

    def test_checker_state_consistency_on_board(self):
        self.__checker1__.set_position(5)
        self.assertTrue(self.__checker1__.is_on_board())
        self.assertFalse(self.__checker1__.is_on_bar())
        self.assertFalse(self.__checker1__.is_off_board())

    def test_checker_state_consistency_on_bar(self):
        self.__checker1__.move_to_bar()
        self.assertFalse(self.__checker1__.is_on_board())
        self.assertTrue(self.__checker1__.is_on_bar())
        self.assertFalse(self.__checker1__.is_off_board())

    def test_checker_state_consistency_off_board(self):
        self.__checker1__.move_off_board()
        self.assertFalse(self.__checker1__.is_on_board())
        self.assertFalse(self.__checker1__.is_on_bar())
        self.assertTrue(self.__checker1__.is_off_board())

    def test_checker_multiple_state_changes(self):
        self.__checker1__.set_position(5)
        self.__checker1__.move_to_bar()
        self.__checker1__.move_to_position(10)
        self.__checker1__.move_off_board()
        
        self.assertIsNone(self.__checker1__.get_position())
        self.assertFalse(self.__checker1__.is_on_board())
        self.assertFalse(self.__checker1__.is_on_bar())
        self.assertTrue(self.__checker1__.is_off_board())

    def test_checker_distance_calculation_edge_cases(self):
        self.__checker1__.set_position(0)
        distance_to_end = self.__checker1__.get_distance_to_position(23)
        self.assertEqual(distance_to_end, 23)
        
        distance_to_start = self.__checker1__.get_distance_to_position(0)
        self.assertEqual(distance_to_start, 0)


if __name__ == '__main__':
    unittest.main()