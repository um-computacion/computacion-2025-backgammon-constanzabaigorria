"""Interfaz de línea de comandos (CLI) para Backgammon.

Proporciona interacción básica con el usuario, visualización del tablero
en formato ASCII y manejo de movimientos.
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
        self._last_dice_: Optional[Any] = None

    def show_menu(self) -> None:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Empezar a jugar")
        print("2. Ver comandos")
        print("3. Salir")
        print("=========================\n")

    def show_commands(self) -> None:
        print("\nComandos disponibles:")
        print("  roll           - Tirar los dados")
        print("  move X Y       - Mover ficha del punto X al punto Y")
        print("  tablero        - Mostrar el tablero")
        print("  quit           - Salir del juego\n")

    # =============================
    # Métodos de visualización
    # =============================

    def _display_board_(self) -> None:
        """Muestra el tablero ASCII actual."""
        board = self._game_.get_board()
        print("\n  13 14 15 16 17 18    BAR    19 20 21 22 23 24")
        print(" ┌────────────────────┐     ┌────────────────────┐")
        print(" │                    │     │                    │")
        print(" │      TABLERO       │     │      VACÍO         │")
        print(" │                    │     │                    │")
        print(" └────────────────────┘     └────────────────────┘")
        print("  12 11 10  9  8  7           6  5  4  3  2  1\n")
        print(str(board))

    def _display_dice_(self) -> None:
        """Muestra el último resultado de los dados si existe."""
        if self._last_dice_ is not None:
            print(f"Dados: {self._last_dice_}")
        else:
            print("Todavía no se han tirado los dados.")

    def _display_winner_(self, winner: str) -> None:
        print(f"¡{winner} gana!")

    def _display_message_(self, message: str) -> None:
        print(message)

    def _display_error_(self, error: str) -> None:
        print(f"ERROR: {error}")

    # =============================
    # Entrada y comandos
    # =============================

    def _get_player_move_(self, player_name: str) -> str:
        while True:
            try:
                move = input(f"{player_name}, ingrese un comando: ").strip()
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

    def _parse_command_(self, command: str) -> Dict[str, Any]:
        command = command.strip()
        if not command:
            return {"type": "invalid"}
        parts = command.split()
        if parts[0] == "move" and len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
            return {"type": "move", "from": int(parts[1]), "to": int(parts[2])}
        if parts[0] == "roll":
            return {"type": "roll"}
        if parts[0] == "tablero":
            return {"type": "tablero"}
        if parts[0] == "quit":
            return {"type": "quit"}
        if parts[0] == "comandos":
            return {"type": "comandos"}
        return {"type": "invalid"}

    # =============================
    # Validaciones y formato
    # =============================

    def _validate_move_(self, from_point: int, to_point: int) -> bool:
        """Valida si el movimiento es permitido."""
        return self._game_.is_valid_move(from_point, to_point)

    # =============================
    # Lógica de turnos
    # =============================

    def _process_turn_(self) -> None:
        """
        Procesa el turno actual del jugador.

        Valida que el juego haya comenzado usando 'is_started' antes de permitir movimientos.
        Después de cada comando válido, muestra el tablero actualizado.
        """
        move = self._get_player_move_(str(self._game_.get_current_player()))
        cmd = self._parse_command_(move)
        if cmd["type"] == "move":
            if not self._game_.is_started():
                self._display_error_("El juego no ha comenzado. Debes tirar los dados primero.")
                return
            if self._validate_move_(cmd["from"], cmd["to"]):
                try:
                    self._game_.make_move(cmd["from"], cmd["to"])
                    self._display_board_()  # Mostrar el tablero después del movimiento
                except ValueError as exc:
                    self._display_error_(str(exc))
            else:
                self._display_error_("Movimiento inválido.")
        elif cmd["type"] == "roll":
            self._game_.start_game()
            self._last_dice_ = self._game_.roll_dice()
            self._display_dice_()
            self._display_board_()  # Mostrar el tablero después de tirar los dados
        elif cmd["type"] == "tablero":
            self._display_board_()
        elif cmd["type"] == "comandos":
            self.show_commands()
        elif cmd["type"] == "quit":
            print("Saliendo del juego.")
            raise SystemExit
        else:
            self._display_error_("Comando inválido.")

    # =============================
    # Ejecución principal
    # =============================

    def _run_(self) -> None:
        print("Bienvenido a Backgammon CLI!")
        while True:
            self.show_menu()
            opcion = input("Seleccione una opción (1-3): ").strip()
            if opcion == "1":
                self._display_board_()
                print("Escribe 'comandos' para ver los comandos disponibles.")
                print("Escribe 'quit' para salir.")
                while True:
                    self._process_turn_()
                    if self._game_.is_finished():
                        winner = self._game_.get_winner()
                        if winner:
                            self._display_winner_(winner)
                        break
                break
            elif opcion == "2":
                self.show_commands()
            elif opcion == "3":
                print("Saliendo del programa.")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def run(self) -> None:
        self._run_()


def run_cli() -> None:
    cli = CLIInterface()
    cli.run()


if __name__ == "__main__":
    run_cli()
