"""Interfaz de línea de comandos mejorada para Backgammon.

Proporciona una experiencia interactiva completa con comandos,
visualización mejorada del tablero y feedback claro al usuario.
"""

from typing import Optional
from core.backgammongame import BackgammonGame


class CLIInterface:
    """Interfaz CLI mejorada para el juego de Backgammon."""

    def __init__(self, game: Optional[BackgammonGame] = None) -> None:
        """
        Inicializa la interfaz CLI con un juego existente o uno nuevo.

        Args:
            game (Optional[BackgammonGame]): Instancia de juego a utilizar.
        """
        self._game_: BackgammonGame = game or BackgammonGame()
        self._running_ = False
        self._moves_remaining_ = 0

    def _display_board_(self) -> None:
        """
        Muestra el tablero actual con visualización mejorada.
        
        Incluye:
        - Estado de fichas en cada punto
        - Fichas en la barra
        - Fichas fuera del tablero
        - Jugador actual resaltado
        """
        print("\n" + "╔" + "═" * 58 + "╗")
        print("║" + " " * 18 + "BACKGAMMON" + " " * 18 + "    ║")
        print("╚" + "═" * 58 + "╝")
        # Mostrar jugador actual
        try:
            current = self._game_.get_current_player()
            if hasattr(current, 'get_name'):
                player_name = current.get_name()
                player_color = current.get_color() if hasattr(current, 'get_color') else ''
            elif hasattr(current, 'name'):
                player_name = current.name
                player_color = current.color if hasattr(current, 'color') else ''
            else:
                player_name = str(current)
                player_color = ''
            print(f"\n  ► Turno de: {player_name} {f'({player_color})' if player_color else ''}")
        except AttributeError:
            print("\n  ► Turno del jugador actual")
        # Obtener el tablero y mostrar visualización completa
        try:
            board = self._game_.get_board()
            self._display_board_visualization_(board)
        except (AttributeError, TypeError) as e:
            print(f"\n  Error al mostrar tablero: {e}")
            # Fallback a visualización simple
            self._display_simple_board_()
        print("  " + "─" * 54)

    def _display_board_visualization_(self, board) -> None:
        """
        Muestra una visualización completa del tablero de Backgammon.
        
        Args:
            board: Instancia del tablero
        """
        # Obtener información del tablero
        points = board.get_points()
        bar = board.get_bar()
        bear_off = board.get_off_board()
        # Contar fichas por color en cada punto
        white_points = {}
        black_points = {}
        for i, point in enumerate(points):
            white_count = sum(1 for checker in point if checker.get_owner().get_color() == "white")
            black_count = sum(1 for checker in point if checker.get_owner().get_color() == "black")
            if white_count > 0:
                white_points[i] = white_count
            if black_count > 0:
                black_points[i] = black_count
        # Contar fichas en la barra
        white_bar = 0
        black_bar = 0
        # La barra puede usar objetos Player como claves
        for key, checkers in bar.items():
            if isinstance(key, str):
                if key == "white":
                    white_bar = len(checkers)
                elif key == "black":
                    black_bar = len(checkers)
            else:
                # Es un objeto Player
                if hasattr(key, 'get_color'):
                    color = key.get_color()
                    if color == "white":
                        white_bar = len(checkers)
                    elif color == "black":
                        black_bar = len(checkers)
        # Contar fichas fuera del tablero
        white_off = 0
        black_off = 0
        # Bear off puede usar objetos Player como claves
        for key, checkers in bear_off.items():
            if isinstance(key, str):
                if key == "white":
                    white_off = len(checkers)
                elif key == "black":
                    black_off = len(checkers)
            else:
                # Es un objeto Player
                if hasattr(key, 'get_color'):
                    color = key.get_color()
                    if color == "white":
                        white_off = len(checkers)
                    elif color == "black":
                        black_off = len(checkers)
        # Mostrar el tablero
        print("\n  " + "═" * 58)
        print("  │ 13  14  15  16  17  18 │ BAR │ 19  20  21  22  23  24 │")
        print("  │" + "─" * 20 + "│" + "─" * 5 + "│" + "─" * 20 + "│")
        # Fila superior (puntos 13-18 y 19-24)
        top_row = "  │"
        for i in range(12, 18):  # Índices 12-17 (puntos 13-18)
            if i in white_points:
                top_row += f" W{white_points[i]:2d}"
            elif i in black_points:
                top_row += f" B{black_points[i]:2d}"
            else:
                top_row += "   ·"
        top_row += " │"
        # Barra central
        if white_bar > 0 and black_bar > 0:
            top_row += f"W{white_bar}B{black_bar}"
        elif white_bar > 0:
            top_row += f"W{white_bar:2d} "
        elif black_bar > 0:
            top_row += f"B{black_bar:2d} "
        else:
            top_row += "   ·"
        top_row += "│"
        for i in range(18, 24):  # Puntos 19-24
            if i in white_points:
                top_row += f" W{white_points[i]:2d}"
            elif i in black_points:
                top_row += f" B{black_points[i]:2d}"
            else:
                top_row += "   ·"
        top_row += " │"
        print(top_row)
        # Línea divisoria
        print("  │" + "─" * 20 + "│" + "─" * 5 + "│" + "─" * 20 + "│")
        # Fila inferior (puntos 12-7 y 6-1)
        bottom_row = "  │"
        for i in range(11, 5, -1):  # Puntos 12-7
            if i in white_points:
                bottom_row += f" W{white_points[i]:2d}"
            elif i in black_points:
                bottom_row += f" B{black_points[i]:2d}"
            else:
                bottom_row += "   ·"
        bottom_row += " │"
        # Barra central (vacía en la fila inferior)
        bottom_row += "   ·│"
        for i in range(5, -1, -1):  # Puntos 6-1
            if i in white_points:
                bottom_row += f" W{white_points[i]:2d}"
            elif i in black_points:
                bottom_row += f" B{black_points[i]:2d}"
            else:
                bottom_row += "   ·"
        bottom_row += " │"
        print(bottom_row)
        print("  │ 12  11  10   9   8   7 │     │  6   5   4   3   2   1 │")
        print("  " + "═" * 58)
        # Mostrar fichas fuera del tablero
        print(f"\n  Fuera del tablero: Blanco: {white_off} | Negro: {black_off}")
        # Mostrar información adicional
        if white_bar > 0 or black_bar > 0:
            print(f"  Fichas en la barra: Blanco: {white_bar} | Negro: {black_bar}")

    def _display_simple_board_(self) -> None:
        """Muestra una visualización simple del tablero como fallback."""
        print("\n  ┌─ Puntos 13-24 ─┬─ BAR ─┬─ Puntos 19-24 ─┐")
        print("  │                │       │                │")
        print("  │  [Fichas aquí] │ W:0|B:0│  [Fichas aquí] │")
        print("  │                │       │                │")
        print("  └────────────────┴───────┴────────────────┘")
        print("  ┌────────────────┬───────┬────────────────┐")
        print("  │                │       │                │")
        print("  │  [Fichas aquí] │       │  [Fichas aquí] │")
        print("  │                │       │                │")
        print("  └─ Puntos 12-1  ─┴───────┴─ Puntos 6-1  ──┘")
        print("\n Fuera del tablero → Blanco: 0 | Negro: 0")

    def _display_dice_(self, dice: list) -> None:
        """
        Muestra los dados de forma visual.
        
        Args:
            dice: Lista con valores de los dados
        """
        print(f"\n Dados lanzados: [{dice[0]}] [{dice[1]}]")

    def _get_player_move_(self, player_name: str) -> str:
        """
        Solicita un movimiento al jugador con manejo de errores.
        
        Args:
            player_name: Nombre del jugador actual
            
        Returns:
            Comando ingresado por el usuario
        """
        while True:
            try:
                prompt = f"\n  [{player_name}] ▶ "
                move = input(prompt).strip()
                return move
            except KeyboardInterrupt:
                print("\n\n Interrupción detectada. Saliendo...")
                raise SystemExit from None
            except EOFError:
                print("\n\n Fin de entrada. Saliendo...")
                raise SystemExit from None
            except Exception:
                print("Entrada inválida. Intente nuevamente.")

    def _display_winner_(self, winner: str) -> None:
        """
        Muestra el ganador con estilo.
        
        Args:
            winner: Nombre del ganador
        """
        print("\n" + "╔" + "═" * 58 + "╗")
        print("║" + " " * 18 + "¡JUEGO TERMINADO!" + " " * 18 + "║")
        print("╠" + "═" * 58 + "╣")
        print(f"║  Ganador: {winner:^40}  ║")
        print("╚" + "═" * 58 + "╝\n")

    def _display_welcome_(self) -> None:
        """Muestra mensaje de bienvenida mejorado."""
        print("\n" + "╔" + "═" * 58 + "╗")
        print("║" + " " * 15 + "BIENVENIDO A BACKGAMMON" + " " * 15 + "║")
        print("╠" + "═" * 58 + "╣")
        print("║  Un juego clásico de estrategia y dados" + " " * 14 + "║")
        print("║" + " " * 58 + "║")
        print("║  Comandos principales:" + " " * 32 + "║")
        print("║    • help (h)  - Ver ayuda completa" + " " * 19 + "║")
        print("║    • roll (r)  - Tirar dados" + " " * 26 + "║")
        print("║    • move (m)  - Hacer movimiento" + " " * 20 + "║")
        print("║    • quit (q)  - Salir del juego" + " " * 21 + "║")
        print("╚" + "═" * 58 + "╝")

    def run(self) -> None:
        """
        Ejecuta el loop principal del CLI.
        
        Maneja la interacción con el usuario y el flujo del juego.
        """
        self._running_ = True
        self._display_welcome_()
        # Iniciar el juego automáticamente
        try:
            self._game_.start_game()
            print("\n  ✓ Juego iniciado")
        except Exception as e:
            print(f"\n  Error al iniciar juego: {e}")
        self._display_board_()
        while self._running_:
            try:
                current_player = self._game_.get_current_player()
                command = self._get_player_move_(str(current_player))
                if not command:
                    continue
                self._handle_command_(command)
            except SystemExit:
                break
            except Exception as e:
                print(f"Error: {e}")

    def _handle_command_(self, command: str) -> None:
        """
        Procesa y ejecuta un comando del usuario.
        
        Args:
            command: Comando ingresado por el usuario
        """
        parts = command.strip().lower().split()
        if not parts:
            return
        cmd = parts[0]
        # Mapeo de comandos a métodos
        handlers = {
            'h': self._cmd_help_,
            'help': self._cmd_help_,
            'ayuda': self._cmd_help_,
            'b': self._cmd_board_,
            'board': self._cmd_board_,
            'tablero': self._cmd_board_,
            'r': self._cmd_roll_,
            'roll': self._cmd_roll_,
            'tirar': self._cmd_roll_,
            'm': self._cmd_move_,
            'move': self._cmd_move_,
            'mover': self._cmd_move_,
            's': self._cmd_status_,
            'status': self._cmd_status_,
            'estado': self._cmd_status_,
            'e': self._cmd_end_turn_,
            'end': self._cmd_end_turn_,
            'terminar': self._cmd_end_turn_,
            'q': self._cmd_quit_,
            'quit': self._cmd_quit_,
            'exit': self._cmd_quit_,
            'salir': self._cmd_quit_,
        }
        handler = handlers.get(cmd)
        if handler:
            handler()
        else:
            print(f"\n Comando desconocido: '{cmd}'")
            print("Escribe 'help' para ver comandos disponibles")

    def _cmd_help_(self) -> None:
        """Muestra la ayuda de comandos."""
        print("\n" + "╔" + "═" * 58 + "╗")
        print("║" + " " * 18 + "COMANDOS DISPONIBLES" + " " * 18 + "║")
        print("╠" + "═" * 58 + "╣")
        print("║  INFORMACIÓN:" + " " * 43 + "║")
        print("║    help (h)     - Mostrar esta ayuda" + " " * 17 + "║")
        print("║    board (b)    - Mostrar tablero" + " " * 20 + "║")
        print("║    status (s)   - Ver estado del turno" + " " * 15 + "║")
        print("║" + " " * 58 + "║")
        print("║  JUEGO:" + " " * 49 + "║")
        print("║    roll (r)     - Tirar los dados" + " " * 20 + "║")
        print("║    move (m)     - Hacer un movimiento" + " " * 16 + "║")
        print("║    end (e)      - Terminar turno" + " " * 21 + "║")
        print("║" + " " * 58 + "║")
        print("║  SISTEMA:" + " " * 47 + "║")
        print("║    quit (q)     - Salir del juego" + " " * 20 + "║")
        print("╚" + "═" * 58 + "╝")
        print("\n Tip: Puedes usar comandos en español o inglés")

    def _cmd_board_(self) -> None:
        """Muestra el tablero."""
        self._display_board_()

    def _cmd_roll_(self) -> None:
        """Maneja el comando de tirar dados."""
        # Verificar si el juego ha comenzado
        if not self._game_.is_started():
            print("\n  ⚠️  El juego no ha comenzado. Iniciando juego...")
            try:
                self._game_.start_game()
                print("  ✓ Juego iniciado")
            except Exception as e:
                print(f"  Error al iniciar juego: {e}")
                return
        try:
            dice = self._game_.roll_dice()
            self._display_dice_(dice)
            # Calcular movimientos disponibles
            if isinstance(dice, (list, tuple)) and len(dice) >= 2:
                if dice[0] == dice[1]:  # Doble
                    self._moves_remaining_ = 4
                else:
                    self._moves_remaining_ = 2
            else:
                self._moves_remaining_ = 2
            
            print(f" Movimientos disponibles: {self._moves_remaining_}")
            print("  Ahora puedes usar 'move' para hacer un movimiento")
        except Exception as e:
            print(f" Error al tirar dados: {e}")

    def _cmd_move_(self) -> None:
        """Maneja el comando de hacer un movimiento."""
        print("\n Movimiento:")
        # Verificar si el juego ha comenzado
        if not self._game_.is_started():
            print("\n  ⚠️  El juego no ha comenzado. Usa 'roll' para tirar dados primero.")
            return
        # Verificar si los dados han sido tirados
        if not self._game_.has_dice_been_rolled():
            print("\n  ⚠️  Debes tirar los dados antes de mover. Usa 'roll'.")
            return
        try:
            from_point = self._get_integer_input_("    Desde punto (1-24): ", 1, 24)
            if from_point is None:
                return
            to_point = self._get_integer_input_("    Hacia punto (1-24): ", 1, 24)
            if to_point is None:
                return
            # Intentar hacer el movimiento
            success = self._game_.make_move(from_point, to_point)
            if success:
                print(f"\n Movimiento exitoso: {from_point} → {to_point}")
                self._moves_remaining_ -= 1
                print(f" Movimientos restantes: {self._moves_remaining_}")
                
                self._display_board_()
                
                # Verificar si se completaron todos los movimientos
                if self._moves_remaining_ <= 0:
                    print("\n  ✓ Todos los movimientos completados. Cambiando de jugador...")
                    try:
                        self._game_.end_turn()
                        print("  ✓ Turno terminado")
                    except Exception as e:
                        print(f"  Error al terminar turno: {e}")
                    self._display_board_()
                
                # Verificar si hay ganador
                if self._game_.is_finished():
                    winner = self._game_.get_winner()
                    if winner:
                        self._display_winner_(str(winner))
                        self._running_ = False
            else:
                print("\n Movimiento inválido. Intenta de nuevo.")
        except ValueError as e:
            print(f"\n  Error: {e}")
        except Exception as e:
            print(f"\n  Error inesperado: {e}")

    def _cmd_status_(self) -> None:
        """Muestra el estado actual del juego."""
        print("\n  ╔═══════════════════════════════╗")
        print("  ║       ESTADO DEL JUEGO        ║")
        print("  ╠═══════════════════════════════╣")
        try:
            current = self._game_.get_current_player()
            # Manejar diferentes tipos de retorno
            if hasattr(current, 'get_name'):
                player_name = current.get_name()
                player_color = current.get_color() if hasattr(current, 'get_color') else ''
                player_str = f"{player_name} ({player_color})"
            else:
                player_str = str(current)
            print(f"  ║  Jugador: {player_str:^18} ║")
        except Exception:
            print("  ║  Jugador: No disponible      ║")
        # Mostrar estado de dados
        if self._game_.has_dice_been_rolled():
            dice = self._game_.get_last_dice_roll()
            print(f"  ║  Dados: {dice[0]}, {dice[1]}" + " " * 8 + "║")
        else:
            print("  ║  Dados: Aún no tirados" + " " * 7 + "║")
        
        # Mostrar movimientos restantes
        print(f"  ║  Movimientos restantes: {self._moves_remaining_}" + " " * 8 + "║")
        print("  ╚═══════════════════════════════╝")

    def _cmd_end_turn_(self) -> None:
        """Termina el turno del jugador actual."""
        try:
            current = self._game_.get_current_player()
            current_str = current.get_name() if hasattr(current, 'get_name') else str(current)
            print(f"\n Terminando turno de {current_str}")
        except Exception:
            print("\n Terminando turno...")
        
        # Cambiar de jugador
        try:
            self._game_.end_turn()
            print("  ✓ Turno terminado")
        except Exception as e:
            print(f"  Error al terminar turno: {e}")
        
        self._display_board_()

    def _cmd_quit_(self) -> None:
        """Maneja la salida del juego."""
        print("\n ¡Gracias por jugar Backgammon!")
        print("  " + "─" * 54)
        self._running_ = False

    def _get_integer_input_(
        self,
        prompt: str,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None
    ) -> Optional[int]:
        """
        Solicita un número entero con validación.
        
        Args:
            prompt: Mensaje a mostrar
            min_value: Valor mínimo aceptado
            max_value: Valor máximo aceptado
            
        Returns:
            Número ingresado o None si es inválido
        """
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print(" Por favor ingrese un número")
                    continue
                value = int(user_input)
                if min_value is not None and value < min_value:
                    print(f" Valor debe ser >= {min_value}")
                    continue
                if max_value is not None and value > max_value:
                    print(f" Valor debe ser <= {max_value}")
                    continue
                return value
            except ValueError:
                print(" Por favor ingrese un número válido")
                continue
            except (KeyboardInterrupt, EOFError):
                print("\n Operación cancelada")
                return None

    def _parse_command_(self, command: str) -> dict:
        """
        Parsea un comando del usuario.
        
        Args:
            command: Comando a parsear
            
        Returns:
            Diccionario con el comando parseado
        """
        command = command.strip().lower()
        if command.startswith("move "):
            parts = command.split()
            if len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
                return {
                    "type": "move",
                    "from": int(parts[1]),
                    "to": int(parts[2])
                }
            return {"type": "invalid"}
        if command == "roll":
            return {"type": "roll"}
        if command in ["quit", "exit"]:
            return {"type": "quit"}
        return {"type": "invalid"}

    def _validate_move_(self, from_point: int, to_point: int) -> bool:
        """
        Valida si un movimiento es permitido.
        
        Args:
            from_point: Punto de origen
            to_point: Punto de destino
            
        Returns:
            True si el movimiento es válido
        """
        return self._game_.is_valid_move(from_point, to_point)

    def _format_board_display_(
        self,
        board_state: Optional[dict] = None
    ) -> str:
        """
        Formatea el tablero para display.
        
        Args:
            board_state: Estado opcional del tablero
            
        Returns:
            String con el tablero formateado
        """
        if board_state is None:
            board_state = self._game_.get_board().get_state()
        display = []
        display.append("╔" + "═" * 58 + "╗")
        display.append("║" + " " * 18 + "TABLERO" + " " * 19 + "    ║")
        display.append("╠" + "═" * 58 + "╣")
        # Aquí agregar lógica de formateo según board_state
        display.append("╚" + "═" * 58 + "╝")
        return "\n".join(display)

    def _display_message_(self, message: str) -> None:
        """
        Muestra un mensaje informativo.
        
        Args:
            message: Mensaje a mostrar
        """
        print(f"{message}")

    def _display_error_(self, error: str) -> None:
        """
        Muestra un mensaje de error.
        
        Args:
            error: Mensaje de error
        """
        print(f"ERROR: {error}")

    def _process_turn_(self) -> None:
        """Procesa el turno actual del jugador."""
        move = self._get_player_move_(
            str(self._game_.get_current_player())
        )
        cmd = self._parse_command_(move)
        if cmd["type"] == "move":
            self._game_.make_move(cmd["from"], cmd["to"])
        elif cmd["type"] == "roll":
            self._cmd_roll_()
        elif cmd["type"] == "quit":
            self._cmd_quit_()

    def _run_turn_(self) -> None:
        """Ejecuta un turno del juego."""
        self._display_board_()
        dice = self._game_.roll_dice()
        self._display_dice_(dice)

    def _run_(self) -> None:
        """
        Loop principal privado del juego.
        
        Maneja la lógica del juego hasta que termine.
        """
        while not self._game_.is_game_over():
            self._display_board_()
            dice = self._game_.roll_dice()
            self._display_dice_(dice)
            move = self._get_player_move_(
                str(self._game_.get_current_player())
            )
            if move == "quit":
                raise SystemExit
            if self._game_.is_game_over():
                winner = self._game_.get_winner()
                self._display_winner_(str(winner))
                raise SystemExit


def run_cli(game: Optional[BackgammonGame] = None) -> None:
    """
    Función de conveniencia para ejecutar el CLI.
    
    Args:
        game: Instancia opcional de juego existente
    
    Esta función puede ser llamada desde otro módulo.
    """
    cli = CLIInterface(game=game)
    cli.run()


# No incluir ejecución directa para mantener modularidad
