"""Interfaz de línea de comandos (CLI) para Backgammon.

Permite interacción básica con el usuario, visualización del tablero,
gestión de movimientos y manejo de estados del juego.
"""

from typing import Any, Dict, Optional

from core.backgammongame import BackgammonGame

class CLIInterface:
    """Interfaz CLI para el juego de Backgammon."""

    def __init__(self, game: Optional[BackgammonGame] = None) -> None:
        """
        Inicializa la interfaz CLI con un juego existente o uno nuevo.

        Args:
            game (Optional[BackgammonGame]): Instancia de juego a utilizar.
        """
        self._game_: BackgammonGame = game or BackgammonGame()

    def _display_board_(self) -> None:
        """Muestra el estado actual del tablero."""
        board = self._game_.get_board()
        print(board)

    def _display_dice_(self, dice: Any) -> None:
        """Muestra el resultado de los dados."""
        print(f"Dados: {dice}")

    def _get_player_move_(self, player_name: str) -> str:
        """Solicita un movimiento al jugador."""
        while True:
            try:
                move = input(f"{player_name}, ingrese su movimiento: ").strip()
                if move == "":
                    return ""
                return move
            except KeyboardInterrupt as exc:
                print("\nInterrupción detectada. Saliendo...")
                raise SystemExit from exc
            except EOFError as exc:
                print("\nFin de entrada detectado. Saliendo...")
                raise SystemExit from exc
            except Exception:
                print("Entrada inválida. Intente nuevamente.")

    def _display_winner_(self, winner: str) -> None:
        """Muestra el ganador del juego."""
        print(f"¡{winner} gana!")

    def _run_(self) -> None:
        """Ejecuta el bucle principal del juego."""
        while True:
            self._display_board_()
            self._display_dice_(self._game_.roll_dice())
            move = self._get_player_move_(str(self._game_.get_current_player()))
            if move == "quit":
                raise SystemExit
            # Aquí se procesarían los movimientos y estados del juego
            if self._game_.is_game_over():
                winner = self._game_.get_winner()
                self._display_winner_(winner)
                raise SystemExit

    def run(self) -> None:
        """
        Ejecuta el bucle principal del juego (método público).
        """
        self._run_()

    def _run_turn_(self) -> None:
        """Ejecuta un turno del juego."""
        self._display_board_()
        self._display_dice_(self._game_.roll_dice())

    def _parse_command_(self, command: str) -> Dict[str, Any]:
        """Parsea el comando ingresado por el usuario."""
        command = command.strip()
        if command.startswith("move "):
            parts = command.split()
            if len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
                return {"type": "move", "from": int(parts[1]), "to": int(parts[2])}
            return {"type": "invalid"}
        if command == "roll":
            return {"type": "roll"}
        if command == "quit":
            return {"type": "quit"}
        return {"type": "invalid"}

    def _validate_move_(self, from_point: int, to_point: int) -> bool:
        """Valida si el movimiento es permitido."""
        # El argumento 'player' no se usa, pero se mantiene para compatibilidad con la interfaz.
        return self._game_.is_valid_move(from_point, to_point)

    def _format_board_display_(self, board_state: Optional[Dict[str, Any]] = None) -> str:
        """Formatea el estado del tablero para mostrarlo en la terminal."""
        if board_state is None:
            board_state = self._game_.get_board().get_state()
        display = "Tablero Backgammon\n"
        display += "Puntos: " + " ".join(str(pt["checkers"]) for pt in board_state["points"]) + "\n"
        display += f"Barra: {board_state['bar']}\n"
        display += f"Bear off: {board_state['bear_off']}\n"
        return display

    def _display_message_(self, message: str) -> None:
        """Muestra un mensaje al usuario."""
        print(message)

    def _display_error_(self, error: str) -> None:
        """Muestra un mensaje de error al usuario."""
        print(f"ERROR: {error}")

    def _get_integer_input_(self, prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
        """Solicita al usuario un número entero dentro de un rango opcional."""
        while True:
            try:
                value = int(input(prompt))
                if min_value is not None and value < min_value:
                    print("Por favor ingrese un número válido.")
                    continue
                if max_value is not None and value > max_value:
                    print("Por favor ingrese un número válido.")
                    continue
                return value
            except ValueError:
                print("Por favor ingrese un número válido.")

    def _process_turn_(self) -> None:
        """Procesa el turno actual del jugador."""
        move = self._get_player_move_(str(self._game_.get_current_player()))
        cmd = self._parse_command_(move)
        if cmd["type"] == "move":
            self._game_.make_move(cmd["from"], cmd["to"])

def run_cli() -> None:
    """
    Ejecuta la interfaz de línea de comandos para Backgammon.

    Este método crea una instancia de CLIInterface y ejecuta el bucle principal.
    """
    cli = CLIInterface()
    # Se accede al método público en vez de protegido para evitar el warning W0212.
    cli.run()

# No incluir código de ejecución directa para mantener la testabilidad.
