'''Tests unitarios para la clase Player.'''
import unittest
from core.player import Player
# pylint: disable=C0116  # many simple test methods without individual docstrings

class TestPlayer(unittest.TestCase):
    '''Clase de tests para Player.'''

    def setUp(self):
        if Player is None:
            self.skipTest("Clase Player no implementada aún")

        self.__player1__ = Player("Jugador1", "white")
        self.__player2__ = Player("Jugador2", "black")

    def test_player_creation_with_name_and_color(self):
        player = Player("TestPlayer", "white")
        self.assertEqual(player.get_name(), "TestPlayer")
        self.assertEqual(player.get_color(), "white")

    def test_player_name_getter(self):
        self.assertEqual(self.__player1__.get_name(), "Jugador1")

    def test_player_name_setter(self):
        self.__player1__.set_name("NuevoNombre")
        self.assertEqual(self.__player1__.get_name(), "NuevoNombre")

    def test_player_color_getter(self):
        self.assertEqual(self.__player1__.get_color(), "white")
        self.assertEqual(self.__player2__.get_color(), "black")

    def test_player_color_setter(self):
        self.__player1__.set_color("black")
        self.assertEqual(self.__player1__.get_color(), "black")

    def test_player_checkers_count_initial(self):
        self.assertEqual(self.__player1__.get_checkers_count(), 15)
        self.assertEqual(self.__player2__.get_checkers_count(), 15)

    def test_player_checkers_count_getter(self):
        count = self.__player1__.get_checkers_count()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_player_checkers_count_setter(self):
        self.__player1__.set_checkers_count(10)
        self.assertEqual(self.__player1__.get_checkers_count(), 10)

    def test_player_checkers_on_bar_initial(self):
        self.assertEqual(self.__player1__.get_checkers_on_bar(), 0)

    def test_player_checkers_on_bar_getter(self):
        count = self.__player1__.get_checkers_on_bar()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_player_checkers_on_bar_setter(self):
        self.__player1__.set_checkers_on_bar(3)
        self.assertEqual(self.__player1__.get_checkers_on_bar(), 3)

    def test_player_checkers_off_board_initial(self):
        self.assertEqual(self.__player1__.get_checkers_off_board(), 0)

    def test_player_checkers_off_board_getter(self):
        count = self.__player1__.get_checkers_off_board()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_player_checkers_off_board_setter(self):
        self.__player1__.set_checkers_off_board(5)
        self.assertEqual(self.__player1__.get_checkers_off_board(), 5)

    def test_player_is_winner_initial(self):
        self.assertFalse(self.__player1__.is_winner())

    def test_player_is_winner_setter(self):
        self.__player1__.set_winner(True)
        self.assertTrue(self.__player1__.is_winner())

    def test_player_can_move_initial(self):
        self.assertTrue(self.__player1__.can_move())

    def test_player_can_move_setter(self):
        self.__player1__.set_can_move(False)
        self.assertFalse(self.__player1__.can_move())

    def test_player_add_checker_to_bar(self):
        initial_count = self.__player1__.get_checkers_on_bar()
        self.__player1__.add_checker_to_bar()
        self.assertEqual(self.__player1__.get_checkers_on_bar(), initial_count + 1)

    def test_player_remove_checker_from_bar(self):
        self.__player1__.add_checker_to_bar()
        initial_count = self.__player1__.get_checkers_on_bar()
        self.__player1__.remove_checker_from_bar()
        self.assertEqual(self.__player1__.get_checkers_on_bar(), initial_count - 1)

    def test_player_remove_checker_from_bar_when_empty(self):
        with self.assertRaises(ValueError):
            self.__player1__.remove_checker_from_bar()

    def test_player_add_checker_off_board(self):
        initial_count = self.__player1__.get_checkers_off_board()
        self.__player1__.add_checker_off_board()
        self.assertEqual(self.__player1__.get_checkers_off_board(), initial_count + 1)

    def test_player_has_checkers_on_bar_true(self):
        self.__player1__.add_checker_to_bar()
        self.assertTrue(self.__player1__.has_checkers_on_bar())

    def test_player_has_checkers_on_bar_false(self):
        self.assertFalse(self.__player1__.has_checkers_on_bar())

    def test_player_can_bear_off_initial(self):
        self.assertFalse(self.__player1__.can_bear_off())

    def test_player_can_bear_off_setter(self):
        self.__player1__.set_can_bear_off(True)
        self.assertTrue(self.__player1__.can_bear_off())

    def test_player_get_home_board_start_white(self):
        white_player = Player("White", "white")
        self.assertEqual(white_player.get_home_board_start(), 19)

    def test_player_get_home_board_start_black(self):
        black_player = Player("Black", "black")
        self.assertEqual(black_player.get_home_board_start(), 1)

    def test_player_get_direction_white(self):
        white_player = Player("White", "white")
        self.assertEqual(white_player.get_direction(), -1)

    def test_player_get_direction_black(self):
        black_player = Player("Black", "black")
        self.assertEqual(black_player.get_direction(), 1)

    def test_player_invalid_color(self):
        with self.assertRaises(ValueError):
            Player("TestPlayer", "red")

    def test_player_empty_name(self):
        with self.assertRaises(ValueError):
            Player("", "white")

    def test_player_none_name(self):
        with self.assertRaises(ValueError):
            Player(None, "white")

    def test_player_negative_checkers_count(self):
        with self.assertRaises(ValueError):
            self.__player1__.set_checkers_count(-1)

    def test_player_excessive_checkers_count(self):
        with self.assertRaises(ValueError):
            self.__player1__.set_checkers_count(16)

    def test_player_negative_checkers_on_bar(self):
        with self.assertRaises(ValueError):
            self.__player1__.set_checkers_on_bar(-1)

    def test_player_negative_checkers_off_board(self):
        with self.assertRaises(ValueError):
            self.__player1__.set_checkers_off_board(-1)

    def test_player_string_representation(self):
        expected = "Player(name=Jugador1, color=white, checkers=15)"
        self.assertEqual(str(self.__player1__), expected)

    def test_player_equality_same_player(self):
        self.assertEqual(self.__player1__, self.__player1__)

    def test_player_equality_different_players(self):
        self.assertNotEqual(self.__player1__, self.__player2__)

    def test_player_equality_same_attributes(self):
        player3 = Player("Jugador1", "white")
        self.assertEqual(self.__player1__, player3)

    def test_player_hash_consistency(self):
        hash1 = hash(self.__player1__)
        hash2 = hash(self.__player1__)
        self.assertEqual(hash1, hash2)

    def test_player_reset_to_initial_state(self):
        self.__player1__.set_checkers_count(10)
        self.__player1__.add_checker_to_bar()
        self.__player1__.add_checker_off_board()
        self.__player1__.set_winner(True)

        self.__player1__.reset()

        self.assertEqual(self.__player1__.get_checkers_count(), 15)
        self.assertEqual(self.__player1__.get_checkers_on_bar(), 0)
        self.assertEqual(self.__player1__.get_checkers_off_board(), 0)
        self.assertFalse(self.__player1__.is_winner())
        self.assertTrue(self.__player1__.can_move())
        self.assertFalse(self.__player1__.can_bear_off())

    def test_player_checkers_conservation(self):
        self.__player1__.set_checkers_count(10)
        self.__player1__.set_checkers_on_bar(3)
        self.__player1__.set_checkers_off_board(2)

        total = (
            self.__player1__.get_checkers_count()
            + self.__player1__.get_checkers_on_bar()
            + self.__player1__.get_checkers_off_board()
        )

        self.assertEqual(total, 15)


if __name__ == "__main__":
    unittest.main()
