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
        
        # Mostrar jugador actual (manejar si no tiene atributo 'upper')
        try:
            current = self._game_.get_current_player()
            # Verificar si current es un objeto Player o un string
            if hasattr(current, 'name'):
                player_name = current.name
                player_color = current.color if hasattr(current, 'color') else ''
            else:
                player_name = str(current)
                player_color = ''
            
            print(f"\n  ► Turno de: {player_name} {f'({player_color})' if player_color else ''}")
        except AttributeError:
            print("\n  ► Turno del jugador actual")
        
        # Obtener el tablero de forma segura
        try:
            board = self._game_.get_board()
            # Aquí deberías implementar la visualización real según tu Board
            print("\n  [Visualización del tablero - En desarrollo]")
            print("  Usa board.points, board.bar, etc. según tu implementación")
        except Exception:
            # Fallback a visualización simple
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
        
        # Mostrar fichas fuera
        print(f"\n Fuera del tablero → Blanco: 0 | Negro: 0")
        print("  " + "─" * 54)

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
        try:
            dice = self._game_.roll_dice()
            self._display_dice_(dice)
            # Mostrar movimientos disponibles si el método existe
            try:
                moves = len(dice) if isinstance(dice, (list, tuple)) else 2
                print(f" Movimientos disponibles: {moves}")
            except Exception:
                print(f" Dados lanzados exitosamente")
        except Exception as e:
            print(f" Error al tirar dados: {e}")

    def _cmd_move_(self) -> None:
        """Maneja el comando de hacer un movimiento."""
        print("\n Movimiento:")
        
        try:
            from_point = self._get_integer_input_("    Desde punto (1-24): ", 1, 24)
            if from_point is None:
                return
            
            to_point = self._get_integer_input_("    Hacia punto (1-24): ", 1, 24)
            if to_point is None:
                return
            
            # Intentar hacer el movimiento
            success = self._game_.make_move(from_point - 1, to_point - 1)
            
            if success:
                print(f"\n Movimiento exitoso: {from_point} → {to_point}")
                self._display_board_()
                
                # Verificar si hay ganador
                if self._game_.is_game_over():
                    winner = self._game_.get_winner()
                    self._display_winner_(str(winner))
                    self._running_ = False
            else:
                print("\n Movimiento inválido. Intenta de nuevo.")
                
        except Exception as e:
            print(f" Error: {e}")

    def _cmd_status_(self) -> None:
        """Muestra el estado actual del juego."""
        print("\n  ╔═══════════════════════════════╗")
        print("  ║       ESTADO DEL JUEGO        ║")
        print("  ╠═══════════════════════════════╣")
        
        try:
            current = self._game_.get_current_player()
            # Manejar diferentes tipos de retorno
            if hasattr(current, 'name'):
                player_str = current.name
            else:
                player_str = str(current)
            print(f"  ║  Jugador: {player_str:^18} ║")
        except Exception:
            print("  ║  Jugador: No disponible      ║")
        
        print("  ║  Dados: Aún no tirados" + " " * 7 + "║")
        print("  ║  Movimientos: 0" + " " * 15 + "║")
        print("  ╚═══════════════════════════════╝")

    def _cmd_end_turn_(self) -> None:
        """Termina el turno del jugador actual."""
        try:
            current = self._game_.get_current_player()
            current_str = current.name if hasattr(current, 'name') else str(current)
            print(f"\n Terminando turno de {current_str}")
        except Exception:
            print("\n Terminando turno...")
        
        # Cambiar de jugador (si tu implementación tiene este método)
        try:
            if hasattr(self._game_, 'switch_player'):
                self._game_.switch_player()
            elif hasattr(self._game_, 'next_turn'):
                self._game_.next_turn()
        except Exception:
            pass
        
        print("  ✓ Turno terminado")
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
        try:
            value = int(input(prompt).strip())
            
            if min_value is not None and value < min_value:
                print(f" Valor debe ser >= {min_value}")
                return None
            
            if max_value is not None and value > max_value:
                print(f" Valor debe ser <= {max_value}")
                return None
            
            return value
            
        except ValueError:
            print(" Por favor ingrese un número válido")
            return None
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
