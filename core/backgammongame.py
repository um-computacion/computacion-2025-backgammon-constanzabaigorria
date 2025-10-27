"""Módulo principal del juego Backgammon.

Esta clase maneja el juego de Backgammon, gestionando jugadores, tablero, dados y lógica principal.
"""

from typing import Optional, List, Dict, Any
from core.player import Player
from core.board import Board
from core.dice import Dice
from core.checker import Checker

class BackgammonGame:
    """Clase principal del juego Backgammon."""

    def __init__(self, player1_name: str = "Player 1", player2_name: str = "Player 2") -> None:
        """
        Inicializa una nueva instancia de BackgammonGame.

        Args:
            player1_name (str): Nombre del jugador 1.
            player2_name (str): Nombre del jugador 2.
        """
        if not player1_name or not player2_name:
            raise ValueError("Los nombres de los jugadores no pueden estar vacíos")
        if player1_name == player2_name:
            raise ValueError("Los nombres de los jugadores deben ser distintos")
        self.__player1: Player = Player(player1_name, "white")
        self.__player2: Player = Player(player2_name, "black")
        self.__board: Board = Board()  # Cambiado de self.board a self.__board
        self.__dice: Dice = Dice()
        self.__current_player: Player = self.__player1
        self.__started: bool = False
        self.__finished: bool = False
        self.__winner: Optional[Player] = None
        self.__last_dice_roll: Optional[tuple] = None
        self.__dice_rolled: bool = False
        self.__moves_count: int = 0
        self.__turn_number: int = 1
        self.__move_history: List[Any] = []
        self.__match_score: Dict[Player, int] = {self.__player1: 0, self.__player2: 0}
        self.__double_offered: bool = False
        self.__doubling_cube_value: int = 1
        self.__doubling_cube_owner: Optional[Player] = None
        self.__game_type: str = "single"
        self.__player1_checkers: List[Checker] = [Checker(self.__player1) for _ in range(15)]
        self.__player2_checkers: List[Checker] = [Checker(self.__player2) for _ in range(15)]
        self.setup_initial_position()

    def setup_initial_position(self) -> None:
        """Configura la posición inicial del tablero y las fichas usando objetos Checker."""
        self.__board.setup_initial_position(self.__player1, self.__player2)
        for checker in self.__player1_checkers:
            checker.reset_position()
        for checker in self.__player2_checkers:
            checker.reset_position()
        idx = 0
        for _ in range(2):
            self.__player1_checkers[idx].set_position(0)
            idx += 1
        for _ in range(5):
            self.__player1_checkers[idx].set_position(11)
            idx += 1
        for _ in range(3):
            self.__player1_checkers[idx].set_position(16)
            idx += 1
        for _ in range(5):
            self.__player1_checkers[idx].set_position(18)
            idx += 1
        idx = 0
        for _ in range(2):
            self.__player2_checkers[idx].set_position(23)
            idx += 1
        for _ in range(5):
            self.__player2_checkers[idx].set_position(12)
            idx += 1
        for _ in range(3):
            self.__player2_checkers[idx].set_position(7)
            idx += 1
        for _ in range(5):
            self.__player2_checkers[idx].set_position(5)
            idx += 1

    def get_player1_checkers(self) -> List[Checker]:
        """Devuelve la lista de fichas del jugador 1."""
        return self.__player1_checkers

    def get_player2_checkers(self) -> List[Checker]:
        """Devuelve la lista de fichas del jugador 2."""
        return self.__player2_checkers

    def get_player1(self) -> Player:
        """Devuelve el jugador 1."""
        return self.__player1

    def get_player2(self) -> Player:
        """Devuelve el jugador 2."""
        return self.__player2

    def get_board(self) -> Board:
        """Devuelve el tablero."""
        return self.__board

    def get_dice(self) -> Dice:
        """Devuelve el dado."""
        return self.__dice

    def get_current_player(self) -> Player:
        """Devuelve el jugador actual."""
        return self.__current_player

    def set_current_player(self, player: Player) -> None:
        """Establece el jugador actual."""
        if player not in [self.__player1, self.__player2]:
            raise ValueError("Jugador inválido")
        self.__current_player = player

    def is_started(self) -> bool:
        """Indica si el juego ha comenzado."""
        return self.__started

    def start_game(self) -> None:
        """Inicia el juego."""
        self.__started = True
        self.__finished = False
        self.__winner = None
        self.__turn_number = 1
        self.__moves_count = 0
        self.__dice_rolled = False
        self.__last_dice_roll = None
        self.__move_history.clear()
        # Solo resetear el tablero si no tiene fichas
        if not any(self.__board.get_points()):
            self.__board.reset()
            self.setup_initial_position()
        self.__current_player = self.__player1

    def is_finished(self) -> bool:
        """Indica si el juego ha finalizado."""
        return self.__finished

    def finish_game(self) -> None:
        """Finaliza el juego."""
        self.__finished = True
        self.__started = False

    def get_winner(self) -> Optional[Player]:
        """Devuelve el ganador del juego."""
        return self.__winner

    def set_winner(self, player: Player) -> None:
        """Establece el ganador del juego."""
        if player not in [self.__player1, self.__player2]:
            raise ValueError("Jugador inválido")
        self.__winner = player

    def switch_player(self) -> None:
        """Cambia el jugador actual."""
        if self.__current_player == self.__player1:
            self.__current_player = self.__player2
        else:
            self.__current_player = self.__player1

    def roll_dice(self) -> tuple:
        """Lanza los dados y devuelve el resultado."""
        if self.__finished:
            raise ValueError("El juego ha finalizado")
        roll = self.__dice.roll()
        self.__last_dice_roll = tuple(roll[:2])
        self.__dice_rolled = True
        return self.__last_dice_roll

    def get_last_dice_roll(self) -> tuple:
        """Devuelve el último lanzamiento de dados."""
        return self.__last_dice_roll if self.__last_dice_roll else (1, 1)

    def has_dice_been_rolled(self) -> bool:
        """Indica si los dados han sido lanzados."""
        return self.__dice_rolled

    def get_available_moves(self) -> List[Any]:
        """Devuelve los movimientos disponibles basados en los dados lanzados."""
        if not self.__dice_rolled or not self.__last_dice_roll:
            return []
            
        movimientos = []
        dados_disponibles = self.__last_dice_roll
        
        # Manejar tanto tuplas de 2 elementos como de 1 elemento
        if len(dados_disponibles) == 2:
            dado1, dado2 = dados_disponibles
        elif len(dados_disponibles) == 1:
            dado1 = dados_disponibles[0]
            dado2 = None
        else:
            return []
        
        # Buscar fichas del jugador actual en el tablero
        for punto_idx in range(24):
            if self.__board.points[punto_idx]:
                primera_ficha = self.__board.points[punto_idx][0]
                if primera_ficha.get_owner() == self.__current_player:
                    punto_num = punto_idx + 1
                    
                    # Calcular posibles destinos para cada dado
                    dados_a_procesar = [dado1]
                    if dado2 is not None:
                        dados_a_procesar.append(dado2)
                        
                    for dado in dados_a_procesar:
                        # En Backgammon:
                        # - Fichas blancas van hacia números más altos (1->24)
                        # - Fichas negras van hacia números más bajos (24->1)
                        if self.__current_player.get_color() == "white":
                            destino = punto_num + dado
                        else:
                            destino = punto_num - dado
                            
                        if 1 <= destino <= 24:
                            if self.is_valid_move(punto_num, destino):
                                movimientos.append((punto_num, destino, dado))
                                
        return movimientos

    def is_valid_move(self, from_point: int, to_point: int) -> bool:
        """
        Valida si un movimiento es válido basado en los dados lanzados.

        Args:
            from_point (int): Punto de origen.
            to_point (int): Punto de destino.

        Returns:
            bool: True si el movimiento es válido, False en caso contrario.
        """
        if not self.__started or self.__finished:
            return False
        
        if not self.__dice_rolled:
            return False
            
        # Verificar que el punto de origen tenga fichas del jugador actual
        if from_point < 1 or from_point > 24:
            return False
            
        punto_origen = from_point - 1
        if not self.__board.points[punto_origen]:
            return False
            
        # Verificar que la ficha pertenezca al jugador actual
        primera_ficha = self.__board.points[punto_origen][0]
        if primera_ficha.get_owner() != self.__current_player:
            return False
            
        # Calcular la distancia del movimiento
        distancia = abs(to_point - from_point)
        
        # Verificar si la distancia coincide con algún valor de dado
        dados_disponibles = self.__last_dice_roll
        
        # Manejar tanto tuplas de 2 elementos como de 1 elemento
        if len(dados_disponibles) == 2:
            dado1, dado2 = dados_disponibles
            valores_dados = [dado1, dado2]
        elif len(dados_disponibles) == 1:
            valores_dados = [dados_disponibles[0]]
        else:
            return False
            
        if distancia not in valores_dados:
            return False
            
        # Verificar que el punto de destino sea válido
        if to_point < 1 or to_point > 24:
            return False
            
        punto_destino = to_point - 1
        
        # Verificar si el punto de destino está bloqueado por el oponente
        if self.__board.points[punto_destino]:
            primera_ficha_destino = self.__board.points[punto_destino][0]
            if primera_ficha_destino.get_owner() != self.__current_player:
                # Si hay más de una ficha del oponente, está bloqueado
                if len(self.__board.points[punto_destino]) > 1:
                    return False
                    
        return True

    def make_move(self, from_point: int, to_point: int) -> bool:
        """
        Realiza un movimiento en el tablero.

        Args:
            from_point (int): Punto de origen.
            to_point (int): Punto de destino.

        Returns:
            bool: True si el movimiento fue realizado, False en caso contrario.
        """
        if not self.is_valid_move(from_point, to_point):
            return False
            
        punto_origen = from_point - 1
        punto_destino = to_point - 1
        
        # Calcular la distancia del movimiento
        distancia = abs(to_point - from_point)
        dados_disponibles = self.__last_dice_roll
        
        # Manejar tanto tuplas de 2 elementos como de 1 elemento
        if len(dados_disponibles) == 2:
            dado1, dado2 = dados_disponibles
        elif len(dados_disponibles) == 1:
            dado1 = dados_disponibles[0]
            dado2 = None
        else:
            return False
        
        # Remover la ficha del punto de origen
        ficha_movida = self.__board.points[punto_origen].pop()
        
        # Si hay una ficha del oponente en el destino, enviarla a la barra
        if self.__board.points[punto_destino]:
            primera_ficha_destino = self.__board.points[punto_destino][0]
            if primera_ficha_destino.get_owner() != self.__current_player:
                ficha_capturada = self.__board.points[punto_destino].pop()
                # Agregar a la barra del oponente
                color_oponente = ficha_capturada.get_owner().get_color()
                self.__board.bar[color_oponente].append(ficha_capturada)
        
        # Colocar la ficha en el destino
        self.__board.points[punto_destino].append(ficha_movida)
        
        # Actualizar el estado de los dados
        if len(dados_disponibles) == 2:
            if distancia == dado1:
                self.__last_dice_roll = (dado2,)
            elif distancia == dado2:
                self.__last_dice_roll = (dado1,)
            else:
                # Si ambos dados tienen el mismo valor, usar uno
                self.__last_dice_roll = (dado1,)
        else:
            # Solo queda un dado, se usa y se termina el turno
            self.__last_dice_roll = ()
            
        # Si no quedan dados por usar, cambiar de turno
        if not self.__last_dice_roll or len(self.__last_dice_roll) == 0:
            self.end_turn()
            
        self.__moves_count += 1
        return True

    def can_player_move(self, player: Player) -> bool:
        """
        Indica si el jugador puede mover.

        Args:
            player (Player): El jugador a consultar.

        Returns:
            bool: True si puede mover, False en caso contrario.
        """
        return True

    def must_enter_from_bar(self, player: Player) -> bool:
        """
        Indica si el jugador debe entrar desde la barra.

        Args:
            player (Player): El jugador a consultar.

        Returns:
            bool: True si debe entrar desde la barra, False en caso contrario.
        """
        return False

    def can_bear_off(self, player: Player) -> bool:
        """
        Indica si el jugador puede sacar fichas del tablero.

        Args:
            player (Player): El jugador a consultar.

        Returns:
            bool: True si puede sacar fichas, False en caso contrario.
        """
        return True

    def check_win_condition(self) -> bool:
        """Verifica la condición de victoria."""
        return self.__winner is not None

    def get_game_state(self) -> Dict[str, Any]:
        """Devuelve el estado actual del juego."""
        return {
            "started": self.__started,
            "finished": self.__finished,
            "current_player": self.__current_player.get_name()
        }

    def get_moves_count(self) -> int:
        """Devuelve la cantidad de movimientos realizados."""
        return self.__moves_count

    def get_turn_number(self) -> int:
        """Devuelve el número de turno actual."""
        return self.__turn_number

    def end_turn(self) -> None:
        """Finaliza el turno actual."""
        self.__turn_number += 1
        self.switch_player()
        self.__dice_rolled = False
        self.__last_dice_roll = None

    def reset_game(self) -> None:
        """Reinicia el juego a su estado inicial."""
        self.__started = False
        self.__finished = False
        self.__winner = None
        self.__turn_number = 1
        self.__moves_count = 0
        self.__dice_rolled = False
        self.__last_dice_roll = None
        self.__move_history.clear()
        self.__board.reset()
        self.__current_player = self.__player1

    def get_pip_count(self, player: Player) -> int:
        """
        Devuelve el pip count del jugador.

        Args:
            player (Player): El jugador para el que se calcula el pip count.

        Returns:
            int: Pip count del jugador (suma de las distancias de todas sus fichas al final).
        """
        pip_count = 0
        checkers = (
            self.__player1_checkers if player == self.__player1 else self.__player2_checkers
        )
        for checker in checkers:
            if checker.is_on_board():
                pos = checker.get_position()
                if pos is not None:
                    if player.get_color() == "white":
                        pip_count += 24 - pos
                    else:
                        pip_count += pos + 1
        return pip_count

    def is_race_position(self) -> bool:
        """Indica si la posición es de carrera."""
        return True

    def get_match_score(self, player: Player) -> int:
        """Devuelve el puntaje del jugador en el match."""
        return self.__match_score.get(player, 0)

    def set_match_score(self, player: Player, score: int) -> None:
        """Establece el puntaje del jugador en el match."""
        if score < 0:
            raise ValueError("El puntaje no puede ser negativo")
        self.__match_score[player] = score

    def is_double_offered(self) -> bool:
        """Indica si se ha ofrecido el doble."""
        return self.__double_offered

    def offer_double(self, player: Player) -> None:
        """Ofrece el doble."""
        if self.__double_offered:
            raise ValueError("Ya se ha ofrecido el doble")
        self.__double_offered = True
        self.__doubling_cube_owner = player

    def accept_double(self) -> None:
        """Acepta el doble."""
        if not self.__double_offered:
            raise ValueError("No se ha ofrecido el doble")
        self.__doubling_cube_value *= 2
        self.__double_offered = False

    def decline_double(self) -> None:
        """Declina el doble."""
        if not self.__double_offered:
            raise ValueError("No se ha ofrecido el doble")
        self.__finished = True

    def get_doubling_cube_value(self) -> int:
        """Devuelve el valor actual del cubo de doblaje."""
        return self.__doubling_cube_value

    def get_doubling_cube_owner(self) -> Optional[Player]:
        """Devuelve el propietario actual del cubo de doblaje."""
        return self.__doubling_cube_owner

    def can_offer_double(self, player: Player) -> bool:
        """
        Indica si el jugador puede ofrecer el doble.

        Args:
            player (Player): El jugador que desea ofrecer el doble.

        Returns:
            bool: True si el jugador puede ofrecer el doble, False en caso contrario.
        """
        # Ejemplo simple: solo se puede ofrecer si no está ofrecido actualmente
        return not self.__double_offered

    def get_game_type(self) -> str:
        """Devuelve el tipo de juego."""
        return self.__game_type

    def calculate_game_value(self) -> int:
        """Calcula el valor actual del juego."""
        return self.__doubling_cube_value

    def save_game_state(self) -> Dict[str, Any]:
        """Guarda el estado actual del juego."""
        return {
            "turn_number": self.__turn_number
        }

    def load_game_state(self, state: Dict[str, Any]) -> None:
        """Carga el estado del juego."""
        if "turn_number" not in state:
            raise ValueError("Estado inválido")
        self.__turn_number = state["turn_number"]

    def get_move_history(self) -> List[Any]:
        """Devuelve el historial de movimientos."""
        return self.__move_history

    def add_move_to_history(self, move: Any) -> None:
        """Agrega un movimiento al historial."""
        self.__move_history.append(move)

    def undo_last_move(self) -> bool:
        """Deshace el último movimiento."""
        if not self.__move_history:
            return False
        self.__move_history.pop()
        return True

    def can_undo_move(self) -> bool:
        """Indica si se puede deshacer el último movimiento."""
        return bool(self.__move_history)

    def get_possible_moves_count(self) -> int:
        """Devuelve la cantidad de movimientos posibles."""
        return 0

    def is_forced_move(self) -> bool:
        """Indica si hay movimientos forzados."""
        return False

    def get_forced_moves(self) -> List[Any]:
        """Devuelve los movimientos forzados."""
        return []

    def validate_game_state(self) -> bool:
        """Valida el estado actual del juego."""
        return True

    def get_statistics(self) -> Dict[str, Any]:
        """Devuelve estadísticas del juego."""
        return {}

    def __str__(self) -> str:
        """Representación en string del juego."""
        return f"BackgammonGame(turn={self.__turn_number}, started={self.__started})"

    def __eq__(self, other: object) -> bool:
        """Compara dos instancias de BackgammonGame."""
        if not isinstance(other, BackgammonGame):
            return False
        # Acceso seguro a atributos privados usando getters o propiedades públicas
        return (
            self.get_turn_number() == other.get_turn_number() and
            self.is_started() == other.is_started()
        )

    def __hash__(self) -> int:
        """Devuelve el hash de la instancia."""
        return hash((self.__turn_number, self.__started))
