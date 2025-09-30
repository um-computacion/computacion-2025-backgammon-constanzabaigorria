"""CLI minimal para Backgammon.

Proporciona un bucle interactivo básico y un renderizador de tablero en ASCII.
Este esqueleto puede ser extendido para agregar acciones del juego.
"""

from typing import Optional
from core.backgammongame import BackgammonGame

class BackgammonCLI:
    """CLI mínima para el juego de Backgammon."""

    def __init__(self, game: Optional[BackgammonGame] = None) -> None:
        """
        Inicializa el CLI con un juego existente o uno nuevo.

        Args:
            game (Optional[BackgammonGame]): Instancia de juego a utilizar.
        """
        self.game: BackgammonGame = game or BackgammonGame()

    def render_board(self) -> None:
        """
        Muestra el esqueleto del tablero en la terminal.
        """
        print("\n  13 14 15 16 17 18    BAR    19 20 21 22 23 24")
        print(" ┌────────────────────┐     ┌────────────────────┐")
        # Aquí se agregarán las filas de fichas en el futuro
        print(" └────────────────────┘     └────────────────────┘")
        print("  12 11 10  9  8  7           6  5  4  3  2  1\n")

    def run(self) -> None:
        """
        Ejecuta un bucle mínimo mostrando el tablero una vez y saliendo.
        """
        self.render_board()
        # Futuro: manejar entrada de usuario, tirar dados, realizar movimientos, etc.

def run_cli() -> None:
    """
    Función de conveniencia para ejecutar el CLI.
    """
    BackgammonCLI().run()

if __name__ == "__main__":
    run_cli()