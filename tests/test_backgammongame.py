"""
Tests unitarios para la clase BackgammonGame.
"""
import unittest
from core.backgammongame import BackgammonGame
from core.player import Player
from core.board import Board
from core.dice import Dice
# pylint: disable=C0116  # many simple test methods without individual docstrings

class TestBackgammonGame(unittest.TestCase):
    """Clase de tests para BackgammonGame."""

    def setUp(self):
        if BackgammonGame is None:
            self.skipTest("Clase BackgammonGame no implementada aún")
        self.__game__ = BackgammonGame()

    def test_game_creation(self):
        game = BackgammonGame()
        self.assertIsNotNone(game)

    def test_game_initialization_with_player_names(self):
        game = BackgammonGame("Player1", "Player2")
        self.assertEqual(game.get_player1().get_name(), "Player1")
        self.assertEqual(game.get_player2().get_name(), "Player2")

    def test_game_default_player_names(self):
        self.assertEqual(self.__game__.get_player1().get_name(), "Player 1")
        self.assertEqual(self.__game__.get_player2().get_name(), "Player 2")

    def test_game_player1_getter(self):
        player1 = self.__game__.get_player1()
        self.assertIsInstance(player1, Player)
        self.assertEqual(player1.get_color(), "white")

    def test_game_player2_getter(self):
        player2 = self.__game__.get_player2()
        self.assertIsInstance(player2, Player)
        self.assertEqual(player2.get_color(), "black")

    def test_game_board_getter(self):
        board = self.__game__.get_board()
        self.assertIsInstance(board, Board)

    def test_game_dice_getter(self):
        dice = self.__game__.get_dice()
        self.assertIsInstance(dice, Dice)

    def test_game_current_player_initial(self):
        current_player = self.__game__.get_current_player()
        self.assertIn(current_player, [self.__game__.get_player1(), self.__game__.get_player2()])

    def test_game_current_player_setter(self):
        player1 = self.__game__.get_player1()
        self.__game__.set_current_player(player1)
        self.assertEqual(self.__game__.get_current_player(), player1)

    def test_game_is_started_initial(self):
        self.assertFalse(self.__game__.is_started())

    def test_game_start_game(self):
        self.__game__.start_game()
        self.assertTrue(self.__game__.is_started())

    def test_game_is_finished_initial(self):
        self.assertFalse(self.__game__.is_finished())

    def test_game_finish_game(self):
        self.__game__.finish_game()
        self.assertTrue(self.__game__.is_finished())

    def test_game_get_winner_initial(self):
        winner = self.__game__.get_winner()
        self.assertIsNone(winner)

    def test_game_set_winner(self):
        player1 = self.__game__.get_player1()
        self.__game__.set_winner(player1)
        self.assertEqual(self.__game__.get_winner(), player1)

    def test_game_switch_player(self):
        initial_player = self.__game__.get_current_player()
        self.__game__.switch_player()
        new_player = self.__game__.get_current_player()
        self.assertNotEqual(initial_player, new_player)

    def test_game_switch_player_twice(self):
        initial_player = self.__game__.get_current_player()
        self.__game__.switch_player()
        self.__game__.switch_player()
        final_player = self.__game__.get_current_player()
        self.assertEqual(initial_player, final_player)

    def test_game_roll_dice(self):
        dice_values = self.__game__.roll_dice()
        self.assertIsInstance(dice_values, tuple)
        self.assertEqual(len(dice_values), 2)
        for value in dice_values:
            self.assertIn(value, [1, 2, 3, 4, 5, 6])

    def test_game_get_last_dice_roll(self):
        self.__game__.roll_dice()
        last_roll = self.__game__.get_last_dice_roll()
        self.assertIsInstance(last_roll, tuple)
        self.assertEqual(len(last_roll), 2)

    def test_game_has_dice_been_rolled_initial(self):
        self.assertFalse(self.__game__.has_dice_been_rolled())

    def test_game_has_dice_been_rolled_after_roll(self):
        self.__game__.roll_dice()
        self.assertTrue(self.__game__.has_dice_been_rolled())

    def test_game_get_available_moves(self):
        self.__game__.roll_dice()
        moves = self.__game__.get_available_moves()
        self.assertIsInstance(moves, list)

    def test_game_is_valid_move(self):
        """Verifica la validación de movimientos."""
        self.__game__.start_game()
        self.__game__.roll_dice()
        is_valid = self.__game__.is_valid_move(0, 5)
        self.assertIsInstance(is_valid, bool)

    def test_game_make_move(self):
        self.__game__.start_game()
        self.__game__.roll_dice()
        result = self.__game__.make_move(0, 5)
        self.assertIsInstance(result, bool)

    def test_game_make_move_invalid_not_started(self):
        with self.assertRaises(ValueError):
            self.__game__.make_move(0, 5)

    def test_game_make_move_invalid_no_dice_roll(self):
        self.__game__.reset_game()  # Asegura que el juego está en estado inicial y los dados NO han sido lanzados
        self.__game__.start_game()  # Esto lanza los dados automáticamente
        self.__game__.reset_game()  # Resetea el juego, ahora __dice_rolled es False
        with self.assertRaises(ValueError):
            self.__game__.make_move(0, 5)

    def test_game_can_player_move(self):
        self.__game__.start_game()
        self.__game__.roll_dice()
        current_player = self.__game__.get_current_player()
        can_move = self.__game__.can_player_move(current_player)
        self.assertIsInstance(can_move, bool)

    def test_game_must_enter_from_bar(self):
        current_player = self.__game__.get_current_player()
        must_enter = self.__game__.must_enter_from_bar(current_player)
        self.assertIsInstance(must_enter, bool)

    def test_game_can_bear_off(self):
        current_player = self.__game__.get_current_player()
        can_bear = self.__game__.can_bear_off(current_player)
        self.assertIsInstance(can_bear, bool)

    def test_game_check_win_condition(self):
        self.__game__.start_game()
        result = self.__game__.check_win_condition()
        self.assertIsInstance(result, bool)

    def test_game_get_game_state(self):
        state = self.__game__.get_game_state()
        self.assertIsInstance(state, dict)
        self.assertIn('started', state)
        self.assertIn('finished', state)
        self.assertIn('current_player', state)

    def test_game_get_moves_count(self):
        count = self.__game__.get_moves_count()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_game_get_turn_number(self):
        turn = self.__game__.get_turn_number()
        self.assertIsInstance(turn, int)
        self.assertGreaterEqual(turn, 1)

    def test_game_end_turn(self):
        initial_turn = self.__game__.get_turn_number()
        self.__game__.end_turn()
        final_turn = self.__game__.get_turn_number()
        self.assertEqual(final_turn, initial_turn + 1)

    def test_game_reset_game(self):
        self.__game__.start_game()
        self.__game__.roll_dice()
        self.__game__.reset_game()
        self.assertFalse(self.__game__.is_started())
        self.assertFalse(self.__game__.is_finished())
        self.assertIsNone(self.__game__.get_winner())
        self.assertFalse(self.__game__.has_dice_been_rolled())

    def test_game_get_pip_count(self):
        player1 = self.__game__.get_player1()
        pip_count = self.__game__.get_pip_count(player1)
        self.assertIsInstance(pip_count, int)
        self.assertGreaterEqual(pip_count, 0)

    def test_game_is_race_position(self):
        is_race = self.__game__.is_race_position()
        self.assertIsInstance(is_race, bool)

    def test_game_get_match_score(self):
        player1 = self.__game__.get_player1()
        score = self.__game__.get_match_score(player1)
        self.assertIsInstance(score, int)
        self.assertGreaterEqual(score, 0)

    def test_game_set_match_score(self):
        player1 = self.__game__.get_player1()
        self.__game__.set_match_score(player1, 3)
        score = self.__game__.get_match_score(player1)
        self.assertEqual(score, 3)

    def test_game_is_double_offered(self):
        is_offered = self.__game__.is_double_offered()
        self.assertIsInstance(is_offered, bool)

    def test_game_offer_double(self):
        player1 = self.__game__.get_player1()
        self.__game__.offer_double(player1)
        self.assertTrue(self.__game__.is_double_offered())

    def test_game_accept_double(self):
        player1 = self.__game__.get_player1()
        self.__game__.offer_double(player1)
        self.__game__.accept_double()
        self.assertFalse(self.__game__.is_double_offered())

    def test_game_decline_double(self):
        player1 = self.__game__.get_player1()
        self.__game__.offer_double(player1)
        self.__game__.decline_double()
        self.assertTrue(self.__game__.is_finished())

    def test_game_get_doubling_cube_value(self):
        value = self.__game__.get_doubling_cube_value()
        self.assertIsInstance(value, int)
        self.assertGreaterEqual(value, 1)

    def test_game_get_doubling_cube_owner(self):
        owner = self.__game__.get_doubling_cube_owner()
        self.assertIn(owner, [None, self.__game__.get_player1(), self.__game__.get_player2()])

    def test_game_can_offer_double(self):
        player1 = self.__game__.get_player1()
        can_offer = self.__game__.can_offer_double(player1)
        self.assertIsInstance(can_offer, bool)

    def test_game_get_game_type(self):
        game_type = self.__game__.get_game_type()
        self.assertIn(game_type, ["single", "gammon", "backgammon"])

    def test_game_calculate_game_value(self):
        value = self.__game__.calculate_game_value()
        self.assertIsInstance(value, int)
        self.assertGreaterEqual(value, 1)

    def test_game_save_game_state(self):
        saved_state = self.__game__.save_game_state()
        self.assertIsInstance(saved_state, dict)

    def test_game_load_game_state(self):
        saved_state = self.__game__.save_game_state()
        new_game = BackgammonGame()
        new_game.load_game_state(saved_state)
        self.assertEqual(new_game.get_turn_number(), self.__game__.get_turn_number())

    def test_game_get_move_history(self):
        history = self.__game__.get_move_history()
        self.assertIsInstance(history, list)

    def test_game_add_move_to_history(self):
        initial_count = len(self.__game__.get_move_history())
        self.__game__.add_move_to_history("0-5")
        final_count = len(self.__game__.get_move_history())
        self.assertEqual(final_count, initial_count + 1)

    def test_game_undo_last_move(self):
        self.__game__.start_game()
        self.__game__.roll_dice()
        result = self.__game__.undo_last_move()
        self.assertIsInstance(result, bool)

    def test_game_can_undo_move(self):
        can_undo = self.__game__.can_undo_move()
        self.assertIsInstance(can_undo, bool)

    def test_game_get_possible_moves_count(self):
        self.__game__.start_game()
        self.__game__.roll_dice()
        count = self.__game__.get_possible_moves_count()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_game_is_forced_move(self):
        self.__game__.start_game()
        self.__game__.roll_dice()
        is_forced = self.__game__.is_forced_move()
        self.assertIsInstance(is_forced, bool)

    def test_game_get_forced_moves(self):
        forced_moves = self.__game__.get_forced_moves()
        self.assertIsInstance(forced_moves, list)

    def test_game_validate_game_state(self):
        is_valid = self.__game__.validate_game_state()
        self.assertIsInstance(is_valid, bool)

    def test_game_get_statistics(self):
        stats = self.__game__.get_statistics()
        self.assertIsInstance(stats, dict)

    def test_game_string_representation(self):
        game_str = str(self.__game__)
        self.assertIsInstance(game_str, str)
        self.assertTrue(len(game_str) > 0)

    def test_game_equality_same_game(self):
        self.assertEqual(self.__game__, self.__game__)

    def test_game_equality_different_games(self):
        game2 = BackgammonGame()
        game2.start_game()
        self.assertNotEqual(self.__game__, game2)

    def test_game_hash_consistency(self):
        hash1 = hash(self.__game__)
        hash2 = hash(self.__game__)
        self.assertEqual(hash1, hash2)

    def test_game_invalid_player_names(self):
        with self.assertRaises(ValueError):
            BackgammonGame("", "Player2")
        with self.assertRaises(ValueError):
            BackgammonGame("Player1", "")

    def test_game_same_player_names(self):
        with self.assertRaises(ValueError):
            BackgammonGame("Player1", "Player1")

    def test_game_invalid_current_player(self):
        invalid_player = Player("Invalid", "white")
        with self.assertRaises(ValueError):
            self.__game__.set_current_player(invalid_player)

    def test_game_invalid_winner(self):
        invalid_player = Player("Invalid", "white")
        with self.assertRaises(ValueError):
            self.__game__.set_winner(invalid_player)

    def test_game_make_move_after_finish(self):
        self.__game__.start_game()
        self.__game__.roll_dice()
        self.__game__.finish_game()
        with self.assertRaises(ValueError):
            self.__game__.make_move(0, 5)

    def test_game_roll_dice_when_finished(self):
        self.__game__.finish_game()
        with self.assertRaises(ValueError):
            self.__game__.roll_dice()

    def test_game_negative_match_score(self):
        player1 = self.__game__.get_player1()
        with self.assertRaises(ValueError):
            self.__game__.set_match_score(player1, -1)

    def test_game_offer_double_when_already_offered(self):
        player1 = self.__game__.get_player1()
        self.__game__.offer_double(player1)
        with self.assertRaises(ValueError):
            self.__game__.offer_double(player1)

    def test_game_accept_double_when_not_offered(self):
        with self.assertRaises(ValueError):
            self.__game__.accept_double()

    def test_game_decline_double_when_not_offered(self):
        with self.assertRaises(ValueError):
            self.__game__.decline_double()

    def test_game_load_invalid_game_state(self):
        with self.assertRaises(ValueError):
            self.__game__.load_game_state({})

    def test_game_undo_move_when_no_moves(self):
        result = self.__game__.undo_last_move()
        self.assertFalse(result)

    def test_game_move_sequence_integration(self):
        self.__game__.start_game()
        initial_player = self.__game__.get_current_player()
        self.assertTrue(self.__game__.has_dice_been_rolled())
        self.__game__.end_turn()
        final_player = self.__game__.get_current_player()
        self.assertNotEqual(initial_player, final_player)

    def test_game_win_condition_integration(self):
        self.__game__.start_game()
        winner = self.__game__.get_player1()
        self.__game__.set_winner(winner)
        self.assertTrue(self.__game__.check_win_condition())
        self.assertEqual(self.__game__.get_winner(), winner)

    def test_game_doubling_cube_sequence(self):
        player1 = self.__game__.get_player1()
        initial_value = self.__game__.get_doubling_cube_value()
        self.__game__.offer_double(player1)
        self.assertTrue(self.__game__.is_double_offered())
        self.__game__.accept_double()
        self.assertFalse(self.__game__.is_double_offered())
        self.assertGreater(self.__game__.get_doubling_cube_value(), initial_value)


if __name__ == '__main__':
    unittest.main()