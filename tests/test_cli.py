# tests/test_cli_complete.py
"""
Tests completos para la interfaz de línea de comandos (CLI) del Backgammon.
Incluye: integración, unitarios, edge cases y performance.
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import time

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cli.cli_interface import CLIInterface
from core.backgammon_game import BackgammonGame
from core.board import Board
from core.player import Player
from core.dice import Dice


class TestCLIIntegration(unittest.TestCase):
    """Tests de integración para el CLI del Backgammon."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self._cli_ = CLIInterface()
        self._game_ = BackgammonGame()
    
    def test_cli_initialization(self):
        """Test que verifica la correcta inicialización del CLI."""
        self.assertIsNotNone(self._cli_._game_)
        self.assertIsInstance(self._cli_._game_, BackgammonGame)
    
    def test_display_board(self):
        """Test que verifica la visualización del tablero."""
        with patch('builtins.print') as mock_print:
            self._cli_._display_board_()
            # Verificar que se llamó a print varias veces
            self.assertGreater(mock_print.call_count, 0)
    
    def test_display_dice_roll(self):
        """Test que verifica la visualización de los dados."""
        with patch('builtins.print') as mock_print:
            self._cli_._display_dice_([1, 2])
            mock_print.assert_called_with("Dados: [1, 2]")
    
    @patch('builtins.input', return_value='1')
    def test_get_player_move_valid(self, mock_input):
        """Test que verifica la obtención de un movimiento válido."""
        move = self._cli_._get_player_move_("Jugador 1")
        self.assertEqual(move, '1')
    
    @patch('builtins.input', side_effect=['invalid', '2'])
    def test_get_player_move_invalid_then_valid(self, mock_input):
        """Test que verifica manejo de entrada inválida seguida de válida."""
        with patch('builtins.print') as mock_print:
            move = self._cli_._get_player_move_("Jugador 1")
            self.assertEqual(move, '2')
            # Verificar que se mostró mensaje de error
            mock_print.assert_any_call("Entrada inválida. Intente nuevamente.")
    
    def test_display_winner(self):
        """Test que verifica la visualización del ganador."""
        with patch('builtins.print') as mock_print:
            self._cli_._display_winner_("Jugador 1")
            mock_print.assert_called_with("¡Jugador 1 gana!")

    @patch('cli.cli_interface.CLIInterface._display_board_')
    @patch('cli.cli_interface.CLIInterface._display_dice_')
    @patch('cli.cli_interface.CLIInterface._get_player_move_')
    @patch('cli.cli_interface.CLIInterface._display_winner_')
    def test_complete_game_flow(self, mock_winner, mock_move, mock_dice, mock_board):
        """Test del flujo completo del juego."""
        # Configurar mocks
        mock_move.side_effect = ['1', '2', 'quit']
        mock_dice.return_value = None
        mock_board.return_value = None
        mock_winner.return_value = None
        
        # Simular juego que termina temprano
        with patch('core.backgammon_game.BackgammonGame.is_game_over', 
                  side_effect=[False, False, True]):
            with patch('core.backgammon_game.BackgammonGame.get_winner', 
                      return_value="Jugador 1"):
                with self.assertRaises(SystemExit):
                    self._cli_._run_()
        
        # Verificar que se llamaron los métodos esperados
        self.assertEqual(mock_board.call_count, 3)
        self.assertEqual(mock_dice.call_count, 2)
        self.assertEqual(mock_move.call_count, 3)


class TestCLIErrorHandling(unittest.TestCase):
    """Tests para el manejo de errores en CLI."""
    
    def setUp(self):
        self._cli_ = CLIInterface()
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt_handling(self, mock_input):
        """Test que verifica el manejo de KeyboardInterrupt."""
        with self.assertRaises(SystemExit):
            self._cli_._get_player_move_("Jugador 1")
    
    @patch('builtins.input', side_effect=EOFError)
    def test_eof_error_handling(self, mock_input):
        """Test que verifica el manejo de EOFError."""
        with self.assertRaises(SystemExit):
            self._cli_._get_player_move_("Jugador 1")
    
    def test_invalid_game_state(self):
        """Test que verifica el manejo de estados de juego inválidos."""
        with patch('core.backgammon_game.BackgammonGame.get_current_player', 
                  side_effect=Exception("Error interno")):
            with self.assertRaises(Exception):
                self._cli_._run_turn_()


class TestCLIUnit(unittest.TestCase):
    """Tests unitarios para componentes específicos del CLI."""
    
    def setUp(self):
        self._cli_ = CLIInterface()
    
    def test_command_parsing_valid(self):
        """Test del parsing de comandos válidos."""
        # Test comando de movimiento
        result = self._cli_._parse_command_("move 1 2")
        self.assertEqual(result, {"type": "move", "from": 1, "to": 2})
        
        # Test comando de dados
        result = self._cli_._parse_command_("roll")
        self.assertEqual(result, {"type": "roll"})
        
        # Test comando de salida
        result = self._cli_._parse_command_("quit")
        self.assertEqual(result, {"type": "quit"})
    
    def test_command_parsing_invalid(self):
        """Test del parsing de comandos inválidos."""
        result = self._cli_._parse_command_("invalid command")
        self.assertEqual(result, {"type": "invalid"})
        
        result = self._cli_._parse_command_("move invalid 2")
        self.assertEqual(result, {"type": "invalid"})
    
    def test_validate_move_valid(self):
        """Test de validación de movimientos válidos."""
        with patch('core.backgammon_game.BackgammonGame.is_valid_move', 
                  return_value=True):
            is_valid = self._cli_._validate_move_(1, 2, "Jugador 1")
            self.assertTrue(is_valid)
    
    def test_validate_move_invalid(self):
        """Test de validación de movimientos inválidos."""
        with patch('core.backgammon_game.BackgammonGame.is_valid_move', 
                  return_value=False):
            is_valid = self._cli_._validate_move_(1, 2, "Jugador 1")
            self.assertFalse(is_valid)
    
    def test_format_board_display(self):
        """Test del formateo del tablero para display."""
        board_state = {
            "points": [{"checkers": 2, "player": "white"} for _ in range(24)],
            "bar": {"white": 0, "black": 0},
            "bear_off": {"white": 0, "black": 0}
        }
        
        with patch('core.board.Board.get_state', return_value=board_state):
            display = self._cli_._format_board_display_()
            self.assertIsInstance(display, str)
            self.assertGreater(len(display), 0)


class TestCLIUserInteraction(unittest.TestCase):
    """Tests para la interacción con el usuario."""
    
    def setUp(self):
        self._cli_ = CLIInterface()
    
    @patch('builtins.print')
    def test_display_message(self, mock_print):
        """Test de visualización de mensajes."""
        self._cli_._display_message_("Test message")
        mock_print.assert_called_with("Test message")
    
    @patch('builtins.print')
    def test_display_error(self, mock_print):
        """Test de visualización de errores."""
        self._cli_._display_error_("Error message")
        mock_print.assert_called_with("ERROR: Error message")
    
    def test_get_integer_input_valid(self):
        """Test de obtención de entrada entera válida."""
        with patch('builtins.input', return_value='5'):
            result = self._cli_._get_integer_input_("Ingrese número: ")
            self.assertEqual(result, 5)
    
    def test_get_integer_input_invalid(self):
        """Test de obtención de entrada entera inválida."""
        with patch('builtins.input', side_effect=['invalid', '5']):
            with patch('builtins.print') as mock_print:
                result = self._cli_._get_integer_input_("Ingrese número: ")
                self.assertEqual(result, 5)
                mock_print.assert_called_with("Por favor ingrese un número válido.")


class TestCLIEdgeCases(unittest.TestCase):
    """Tests para casos extremos y edge cases del CLI."""
    
    def setUp(self):
        self._cli_ = CLIInterface()
    
    def test_empty_input_handling(self):
        """Test del manejo de entrada vacía."""
        with patch('builtins.input', return_value=''):
            with patch('builtins.print') as mock_print:
                result = self._cli_._get_player_move_("Jugador 1")
                self.assertEqual(result, '')
                mock_print.assert_not_called()  # No debería mostrar error
    
    def test_whitespace_input_handling(self):
        """Test del manejo de entrada con espacios en blanco."""
        with patch('builtins.input', return_value='   move 1 2  '):
            result = self._cli_._parse_command_('   move 1 2  ')
            self.assertEqual(result, {"type": "move", "from": 1, "to": 2})
    
    def test_very_long_input(self):
        """Test del manejo de entrada muy larga."""
        long_input = "a" * 1000
        with patch('builtins.input', return_value=long_input):
            result = self._cli_._get_player_move_("Jugador 1")
            self.assertEqual(result, long_input)
    
    def test_special_characters_input(self):
        """Test del manejo de caracteres especiales."""
        special_input = "move 1@ 2#"
        with patch('builtins.input', return_value=special_input):
            result = self._cli_._parse_command_(special_input)
            self.assertEqual(result, {"type": "invalid"})
    
    def test_unicode_input(self):
        """Test del manejo de caracteres Unicode."""
        unicode_input = "movimiento 1 2 ñáéíóú"
        with patch('builtins.input', return_value=unicode_input):
            result = self._cli_._get_player_move_("Jugador 1")
            self.assertEqual(result, unicode_input)


class TestCLIBoundaryConditions(unittest.TestCase):
    """Tests para condiciones de borde del CLI."""
    
    def setUp(self):
        self._cli_ = CLIInterface()
    
    def test_minimum_board_display(self):
        """Test de visualización con estado mínimo del tablero."""
        minimal_state = {
            "points": [{"checkers": 0, "player": None} for _ in range(24)],
            "bar": {"white": 0, "black": 0},
            "bear_off": {"white": 0, "black": 0}
        }
        
        with patch('core.board.Board.get_state', return_value=minimal_state):
            display = self._cli_._format_board_display_()
            self.assertIsInstance(display, str)
            self.assertGreater(len(display), 0)
    
    def test_maximum_board_display(self):
        """Test de visualización con estado máximo del tablero."""
        max_state = {
            "points": [{"checkers": 5, "player": "white"} for _ in range(24)],
            "bar": {"white": 10, "black": 10},
            "bear_off": {"white": 15, "black": 15}
        }
        
        with patch('core.board.Board.get_state', return_value=max_state):
            display = self._cli_._format_board_display_()
            self.assertIsInstance(display, str)
            self.assertGreater(len(display), 0)
    
    @patch('builtins.input', side_effect=['-1', '25', '5'])
    def test_out_of_bounds_input(self, mock_input):
        """Test de entrada fuera de los límites válidos."""
        with patch('builtins.print') as mock_print:
            result = self._cli_._get_integer_input_("Ingrese posición: ", 0, 24)
            self.assertEqual(result, 5)
            # Debería mostrar mensajes de error
            self.assertGreaterEqual(mock_print.call_count, 2)


class TestCLIPerformance(unittest.TestCase):
    """Tests de performance del CLI."""
    
    def setUp(self):
        self._cli_ = CLIInterface()
    
    def test_board_display_performance(self):
        """Test de performance para la visualización del tablero."""
        start_time = time.time()
        
        # Ejecutar display del tablero múltiples veces
        for _ in range(100):
            with patch('core.board.Board.get_state'):
                self._cli_._format_board_display_()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Debería ejecutarse en menos de 1 segundo
        self.assertLess(execution_time, 1.0)
    
    def test_command_parsing_performance(self):
        """Test de performance para el parsing de comandos."""
        test_commands = ["move 1 2", "roll", "quit", "invalid command"] * 25
        
        start_time = time.time()
        
        for command in test_commands:
            self._cli_._parse_command_(command)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Debería ejecutarse en menos de 0.1 segundos
        self.assertLess(execution_time, 0.1)


class TestCLIWithMockGame(unittest.TestCase):
    """Tests del CLI usando un juego mock."""
    
    def setUp(self):
        self._mock_game_ = MagicMock()
        self._mock_game_.get_current_player.return_value = "white"
        self._mock_game_.roll_dice.return_value = [1, 2]
        self._mock_game_.is_game_over.return_value = False
        self._mock_game_.get_winner.return_value = None
        self._mock_game_.make_move.return_value = True
        self._mock_game_.is_valid_move.return_value = True
        
        self._cli_ = CLIInterface()
        self._cli_._game_ = self._mock_game_
    
    def test_cli_with_mock_game_initialization(self):
        """Test que verifica el CLI funciona con juego mock."""
        self.assertEqual(self._cli_._game_, self._mock_game_)
        self.assertEqual(self._cli_._game_.get_current_player(), "white")
    
    def test_cli_with_mock_game_roll_dice(self):
        """Test que verifica el roll de dados con juego mock."""
        dice_result = self._cli_._game_.roll_dice()
        self.assertEqual(dice_result, [1, 2])
        self._mock_game_.roll_dice.assert_called_once()
    
    @patch('builtins.input', return_value='move 1 2')
    def test_cli_with_mock_game_make_move(self, mock_input):
        """Test que verifica hacer movimiento con juego mock."""
        with patch('builtins.print'):
            self._cli_._process_turn_()
            self._mock_game_.make_move.assert_called()


class TestCLIGameStates(unittest.TestCase):
    """Tests para diferentes estados del juego en CLI."""
    
    def setUp(self):
        self._cli_ = CLIInterface()
    
    def test_game_not_started_state(self):
        """Test para estado cuando el juego no ha comenzado."""
        with patch('core.backgammon_game.BackgammonGame.is_game_over', 
                  return_value=False):
            with patch('core.backgammon_game.BackgammonGame.get_winner', 
                      return_value=None):
                # El juego debería continuar
                game_over = self._cli_._game_.is_game_over()
                winner = self._cli_._game_.get_winner()
                
                self.assertFalse(game_over)
                self.assertIsNone(winner)
    
    def test_game_finished_state(self):
        """Test para estado cuando el juego ha terminado."""
        with patch('core.backgammon_game.BackgammonGame.is_game_over', 
                  return_value=True):
            with patch('core.backgammon_game.BackgammonGame.get_winner', 
                      return_value="white"):
                game_over = self._cli_._game_.is_game_over()
                winner = self._cli_._game_.get_winner()
                
                self.assertTrue(game_over)
                self.assertEqual(winner, "white")


def run_all_tests():
    """Función para ejecutar todos los tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de test
    test_classes = [
        TestCLIIntegration,
        TestCLIErrorHandling,
        TestCLIUnit,
        TestCLIUserInteraction,
        TestCLIEdgeCases,
        TestCLIBoundaryConditions,
        TestCLIPerformance,
        TestCLIWithMockGame,
        TestCLIGameStates
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Ejecutar todos los tests
    success = run_all_tests()
    
    # Salir con código apropiado
    sys.exit(0 if success else 1)