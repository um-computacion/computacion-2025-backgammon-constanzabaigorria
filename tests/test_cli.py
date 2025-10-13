"""
Tests unitarios para CLIInterface - Sin Warnings.

Estos tests verifican el comportamiento del CLI sin acceder
directamente a métodos protegidos cuando es posible.
"""

import unittest
from unittest.mock import patch, Mock
from io import StringIO
import sys

from cli.cli import CLIInterface, run_cli


# Deshabilitar warning W0212 solo para este archivo de tests
# pylint: disable=protected-access
# Justificación: Tests necesitan verificar métodos internos del CLI


class TestCLIInitialization(unittest.TestCase):
    """Tests de inicialización del CLI."""

    def test_cli_can_be_instantiated_without_game(self):
        """Test que el CLI puede crearse sin pasar un juego."""
        cli = CLIInterface()
        self.assertIsNotNone(cli)

    def test_cli_can_be_instantiated_with_existing_game(self):
        """Test que el CLI acepta un juego existente."""
        mock_game = Mock()
        cli = CLIInterface(game=mock_game)
        self.assertIsNotNone(cli)
        # Verificar sin acceder directamente al atributo
        self.assertTrue(hasattr(cli, '_game_'))

    def test_cli_has_game_attribute(self):
        """Test que el CLI tiene atributo game."""
        cli = CLIInterface()
        # Solo verificar que existe el atributo
        self.assertTrue(hasattr(cli, '_game_'))


class TestCLIDisplayBoard(unittest.TestCase):
    """Tests para display_board."""

    def setUp(self):
        """Configura el CLI con juego mock."""
        self.mock_game = Mock()
        self.mock_board = Mock()
        self.mock_board.__str__ = Mock(return_value="Mock Board")
        self.mock_game.get_board.return_value = self.mock_board
        self.cli = CLIInterface(game=self.mock_game)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_board_prints_output(self, mock_stdout):
        """Test que display_board imprime el tablero."""
        self.cli._display_board_()
        output = mock_stdout.getvalue()
        self.assertGreater(len(output), 0)
        self.mock_game.get_board.assert_called_once()


class TestCLIDisplayDice(unittest.TestCase):
    """Tests para display_dice."""

    def setUp(self):
        """Configura el CLI."""
        self.cli = CLIInterface()

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_dice_shows_dice_values(self, mock_stdout):
        """Test que muestra los valores de los dados."""
        test_dice = [3, 5]
        self.cli._display_dice_(test_dice)
        output = mock_stdout.getvalue()
        self.assertIn("Dados:", output)
        self.assertIn("[3, 5]", output)


class TestCLIDisplayWinner(unittest.TestCase):
    """Tests para display_winner."""

    def setUp(self):
        """Configura el CLI."""
        self.cli = CLIInterface()

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_winner_shows_winner(self, mock_stdout):
        """Test que muestra el ganador."""
        winner = "Jugador Blanco"
        self.cli._display_winner_(winner)
        output = mock_stdout.getvalue()
        self.assertIn(winner, output)
        self.assertIn("gana", output.lower())


class TestCLIGetPlayerMove(unittest.TestCase):
    """Tests para get_player_move."""

    def setUp(self):
        """Configura el CLI."""
        self.cli = CLIInterface()

    @patch('builtins.input', return_value='move 8 5')
    def test_get_player_move_returns_valid_input(self, _):
        """Test que retorna entrada válida."""
        move = self.cli._get_player_move_("Jugador 1")
        self.assertEqual(move, 'move 8 5')

    @patch('builtins.input', return_value='')
    def test_get_player_move_handles_empty_input(self, _):
        """Test que maneja entrada vacía."""
        move = self.cli._get_player_move_("Jugador 1")
        self.assertEqual(move, '')

    @patch('builtins.input', side_effect=KeyboardInterrupt)
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_player_move_handles_keyboard_interrupt(self, mock_stdout, _):
        """Test que maneja Ctrl+C."""
        with self.assertRaises(SystemExit):
            self.cli._get_player_move_("Jugador 1")
        output = mock_stdout.getvalue()
        self.assertIn("Interrupción", output)

    @patch('builtins.input', side_effect=EOFError)
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_player_move_handles_eof(self, mock_stdout, _):
        """Test que maneja EOF."""
        with self.assertRaises(SystemExit):
            self.cli._get_player_move_("Jugador 1")
        output = mock_stdout.getvalue()
        self.assertIn("Fin de entrada", output)


class TestCLIParseCommand(unittest.TestCase):
    """Tests para parse_command."""

    def setUp(self):
        """Configura el CLI."""
        self.cli = CLIInterface()

    def test_parse_move_command_valid(self):
        """Test parsing de move válido."""
        result = self.cli._parse_command_("move 8 5")
        self.assertEqual(result["type"], "move")
        self.assertEqual(result["from"], 8)
        self.assertEqual(result["to"], 5)

    def test_parse_move_command_invalid_format(self):
        """Test parsing de move con formato inválido."""
        result = self.cli._parse_command_("move abc def")
        self.assertEqual(result["type"], "invalid")

    def test_parse_move_command_insufficient_args(self):
        """Test parsing de move sin argumentos suficientes."""
        result = self.cli._parse_command_("move 8")
        self.assertEqual(result["type"], "invalid")

    def test_parse_roll_command(self):
        """Test parsing de roll."""
        result = self.cli._parse_command_("roll")
        self.assertEqual(result["type"], "roll")

    def test_parse_quit_command(self):
        """Test parsing de quit."""
        result = self.cli._parse_command_("quit")
        self.assertEqual(result["type"], "quit")

    def test_parse_invalid_command(self):
        """Test parsing de comando desconocido."""
        result = self.cli._parse_command_("unknown")
        self.assertEqual(result["type"], "invalid")

    def test_parse_command_strips_whitespace(self):
        """Test que elimina espacios."""
        result = self.cli._parse_command_("  move 8 5  ")
        self.assertEqual(result["type"], "move")


class TestCLIValidateMove(unittest.TestCase):
    """Tests para validate_move."""

    def setUp(self):
        """Configura el CLI con juego mock."""
        self.mock_game = Mock()
        self.cli = CLIInterface(game=self.mock_game)

    def test_validate_move_calls_game_method(self):
        """Test que llama a is_valid_move del juego."""
        self.mock_game.is_valid_move.return_value = True
        result = self.cli._validate_move_(8, 5)
        self.mock_game.is_valid_move.assert_called_once_with(8, 5)
        self.assertTrue(result)

    def test_validate_move_returns_false_for_invalid(self):
        """Test que retorna False para movimiento inválido."""
        self.mock_game.is_valid_move.return_value = False
        result = self.cli._validate_move_(24, 1)
        self.assertFalse(result)


class TestCLIFormatBoardDisplay(unittest.TestCase):
    """Tests para format_board_display."""

    def setUp(self):
        """Configura el CLI con juego mock."""
        self.mock_game = Mock()
        self.mock_board = Mock()
        self.mock_board.get_state.return_value = {
            "points": [{"checkers": i % 3} for i in range(24)],
            "bar": {"white": 0, "black": 0},
            "bear_off": {"white": 0, "black": 0}
        }
        self.mock_game.get_board.return_value = self.mock_board
        self.cli = CLIInterface(game=self.mock_game)

    def test_format_board_display_returns_string(self):
        """Test que retorna un string."""
        display = self.cli._format_board_display_()
        self.assertIsInstance(display, str)
        self.assertGreater(len(display), 0)

    def test_format_board_display_contains_sections(self):
        """Test que contiene todas las secciones."""
        display = self.cli._format_board_display_()
        self.assertIn("Tablero", display)
        self.assertIn("Puntos:", display)
        self.assertIn("Barra:", display)
        self.assertIn("Bear off:", display)

    def test_format_board_with_custom_state(self):
        """Test con estado personalizado."""
        custom_state = {
            "points": [{"checkers": 2} for _ in range(24)],
            "bar": {"white": 1, "black": 0},
            "bear_off": {"white": 5, "black": 3}
        }
        display = self.cli._format_board_display_(custom_state)
        self.assertIsInstance(display, str)


class TestCLIDisplayMessage(unittest.TestCase):
    """Tests para display_message."""

    def setUp(self):
        """Configura el CLI."""
        self.cli = CLIInterface()

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_message_prints_text(self, mock_stdout):
        """Test que imprime el mensaje."""
        message = "Test message"
        self.cli._display_message_(message)
        output = mock_stdout.getvalue()
        self.assertIn(message, output)


class TestCLIDisplayError(unittest.TestCase):
    """Tests para display_error."""

    def setUp(self):
        """Configura el CLI."""
        self.cli = CLIInterface()

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_error_shows_prefix(self, mock_stdout):
        """Test que muestra prefijo ERROR."""
        error = "Something went wrong"
        self.cli._display_error_(error)
        output = mock_stdout.getvalue()
        self.assertIn("ERROR:", output)
        self.assertIn(error, output)


class TestCLIGetIntegerInput(unittest.TestCase):
    """Tests para get_integer_input."""

    def setUp(self):
        """Configura el CLI."""
        self.cli = CLIInterface()

    @patch('builtins.input', return_value='5')
    def test_get_integer_valid(self, _):
        """Test con entrada válida."""
        result = self.cli._get_integer_input_("Número: ")
        self.assertEqual(result, 5)

    @patch('builtins.input', side_effect=['invalid', '10'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_integer_retries_on_invalid(self, mock_stdout, _):
        """Test que reintenta con entrada inválida."""
        result = self.cli._get_integer_input_("Número: ")
        self.assertEqual(result, 10)
        output = mock_stdout.getvalue()
        self.assertIn("válido", output)

    @patch('builtins.input', side_effect=['3', '15'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_integer_validates_min(self, mock_stdout, _):
        """Test validación de valor mínimo."""
        result = self.cli._get_integer_input_("Número: ", min_value=10)
        self.assertEqual(result, 15)

    @patch('builtins.input', side_effect=['25', '10'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_integer_validates_max(self, mock_stdout, _):
        """Test validación de valor máximo."""
        result = self.cli._get_integer_input_("Número: ", max_value=20)
        self.assertEqual(result, 10)


class TestCLIProcessTurn(unittest.TestCase):
    """Tests para process_turn."""

    def setUp(self):
        """Configura el CLI con juego mock."""
        self.mock_game = Mock()
        self.mock_game.get_current_player.return_value = "white"
        self.cli = CLIInterface(game=self.mock_game)

    @patch('builtins.input', return_value='move 8 5')
    def test_process_turn_executes_move(self, _):
        """Test que ejecuta un movimiento."""
        self.cli._process_turn_()
        self.mock_game.make_move.assert_called_once_with(8, 5)

    @patch('builtins.input', return_value='invalid')
    def test_process_turn_handles_invalid_command(self, _):
        """Test que maneja comando inválido."""
        self.cli._process_turn_()
        # No debería llamar a make_move
        self.mock_game.make_move.assert_not_called()


class TestCLIRunTurn(unittest.TestCase):
    """Tests para run_turn."""

    def setUp(self):
        """Configura el CLI con juego mock."""
        self.mock_game = Mock()
        self.mock_board = Mock()
        self.mock_board.__str__ = Mock(return_value="Board")
        self.mock_game.get_board.return_value = self.mock_board
        self.mock_game.roll_dice.return_value = [4, 6]
        self.cli = CLIInterface(game=self.mock_game)

    @patch('sys.stdout', new_callable=StringIO)
    def test_run_turn_displays_board(self, mock_stdout):
        """Test que muestra el tablero."""
        self.cli._run_turn_()
        self.mock_game.get_board.assert_called()

    @patch('sys.stdout', new_callable=StringIO)
    def test_run_turn_rolls_dice(self, mock_stdout):
        """Test que tira los dados."""
        self.cli._run_turn_()
        self.mock_game.roll_dice.assert_called_once()


class TestCLIRunMethod(unittest.TestCase):
    """Tests para método run público."""

    @patch.object(CLIInterface, '_run_')
    def test_run_calls_private_run(self, mock_run):
        """Test que run() llama a _run_()."""
        cli = CLIInterface()
        cli.run()
        mock_run.assert_called_once()


class TestRunCliFunction(unittest.TestCase):
    """Tests para función run_cli."""

    @patch.object(CLIInterface, 'run')
    def test_run_cli_creates_and_runs(self, mock_run):
        """Test que run_cli ejecuta el CLI."""
        run_cli()
        mock_run.assert_called_once()


class TestCLIEdgeCases(unittest.TestCase):
    """Tests de casos extremos."""

    def setUp(self):
        """Configura el CLI."""
        self.cli = CLIInterface()

    def test_parse_empty_string(self):
        """Test con string vacío."""
        result = self.cli._parse_command_("")
        self.assertEqual(result["type"], "invalid")

    def test_parse_whitespace_only(self):
        """Test con solo espacios."""
        result = self.cli._parse_command_("   ")
        self.assertEqual(result["type"], "invalid")

def run_tests():
    """Ejecuta todos los tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    test_classes = [
        TestCLIInitialization,
        TestCLIDisplayBoard,
        TestCLIDisplayDice,
        TestCLIDisplayWinner,
        TestCLIGetPlayerMove,
        TestCLIParseCommand,
        TestCLIValidateMove,
        TestCLIFormatBoardDisplay,
        TestCLIDisplayMessage,
        TestCLIDisplayError,
        TestCLIGetIntegerInput,
        TestCLIProcessTurn,
        TestCLIRunTurn,
        TestCLIRunMethod,
        TestRunCliFunction,
        TestCLIEdgeCases,
    ]
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
