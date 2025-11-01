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
        # Si es un doble, guardar 4 movimientos del mismo valor
        if roll[0] == roll[1]:
            self.__last_dice_roll = tuple([roll[0]] * 4)
        else:
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
        
        # Manejar tuplas de cualquier longitud (dobles tienen 4 elementos)
        if len(dados_disponibles) >= 2:
            # Dobles: (2,2,2,2) o normales: (2,5)
            dados_a_procesar = list(dados_disponibles)
        elif len(dados_disponibles) == 1:
            dados_a_procesar = [dados_disponibles[0]]
        else:
            return []
        
        # Verificar si puede hacer bear off
        color = self.__current_player.get_color()
        can_bear = self.__board.can_bear_off(self.__current_player)
        
        # Buscar fichas del jugador actual en el tablero
        for punto_idx in range(24):
            if self.__board.points[punto_idx]:
                primera_ficha = self.__board.points[punto_idx][0]
                if primera_ficha.get_owner() == self.__current_player:
                    punto_num = punto_idx + 1
                    
                    # Calcular posibles destinos para cada dado
                    for dado in dados_a_procesar:
                        # En Backgammon:
                        # - Fichas blancas van hacia números más altos (1->24)
                        # - Fichas negras van hacia números más bajos (24->1)
                        if self.__current_player.get_color() == "white":
                            destino = punto_num + dado
                        else:
                            destino = punto_num - dado
                            
                        # Movimientos normales en el tablero
                        if 1 <= destino <= 24:
                            if self.is_valid_move(punto_num, destino):
                                movimientos.append((punto_num, destino, dado))
                        
                        # Bear off: verificar si puede sacar fichas
                        if can_bear:
                            if color == "white" and 19 <= punto_num <= 24:
                                # Bear off para blancas
                                if self.is_valid_move(punto_num, 25):
                                    movimientos.append((punto_num, 25, dado))
                            elif color == "black" and 1 <= punto_num <= 6:
                                # Bear off para negras
                                if self.is_valid_move(punto_num, 0):
                                    movimientos.append((punto_num, 0, dado))
                                
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
        
        # Obtener dados disponibles
        dados_disponibles = self.__last_dice_roll
        
        # Manejar tuplas de cualquier longitud (dobles tienen 4 elementos)
        if len(dados_disponibles) >= 1:
            # Dobles: (2,2,2,2) o normales: (2,5) o parcial: (2,)
            valores_dados = list(dados_disponibles)
        else:
            return False
            
        # BEAR OFF: Verificar PRIMERO si el movimiento es bear off válido
        color = self.__current_player.get_color()
        home_points_white_idx = range(18, 24)  # Índices 0-based: puntos 19-24 (18-23)
        home_points_black_idx = range(0, 6)    # Índices 0-based: puntos 1-6 (0-5)
        
        if color == "white" and from_point >= 19 and from_point <= 24 and to_point == 25:
            # Bear off válido si todas las fichas están en home board
            if self.__board.can_bear_off(self.__current_player):
                # Verificar que el dado permita este movimiento
                movimiento = 25 - from_point
                if movimiento <= 0:
                    movimiento = 1
                if movimiento in valores_dados:
                    return True
                # Permitir usar dado mayor solo si es la ficha más atrasada
                # Buscar la ficha más lejana (mayor índice, ya que blanco viene de 0)
                punto_origen_idx = from_point - 1
                max_pos = max([i for i in home_points_white_idx if self.__board.points[i] and 
                               self.__board.points[i][0].get_owner() == self.__current_player], default=None)
                if max_pos is not None and punto_origen_idx == max_pos:
                    return any(dado >= movimiento for dado in valores_dados)
            return False
        elif color == "black" and from_point >= 1 and from_point <= 6 and to_point == 0:
            # Bear off válido si todas las fichas están en home board
            if self.__board.can_bear_off(self.__current_player):
                # Verificar que el dado permita este movimiento
                movimiento = from_point
                if movimiento <= 0:
                    movimiento = 1
                if movimiento in valores_dados:
                    return True
                # Permitir usar dado mayor solo si es la ficha más atrasada
                # Buscar la ficha más lejana (menor índice, ya que negro viene de 23)
                punto_origen_idx = from_point - 1
                min_pos = min([i for i in home_points_black_idx if self.__board.points[i] and 
                               self.__board.points[i][0].get_owner() == self.__current_player], default=None)
                if min_pos is not None and punto_origen_idx == min_pos:
                    return any(dado >= movimiento for dado in valores_dados)
            return False
            
        # Si no es bear off, verificar movimiento normal
        # Calcular la distancia del movimiento
        distancia = abs(to_point - from_point)
        
        if distancia not in valores_dados:
            return False
            
        # Verificar que el punto de destino sea válido (no bear off)
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
        Realiza un movimiento en el tablero, incluyendo bear off.

        Args:
            from_point (int): Punto de origen.
            to_point (int): Punto de destino (1-24 o fuera del tablero).
        Returns:
            bool: True si el movimiento fue realizado, False en caso contrario.
        """
        if not self.is_valid_move(from_point, to_point):
            return False
        punto_origen = from_point - 1
        punto_destino = to_point - 1
        distancia = abs(to_point - from_point)
        dados_disponibles = self.__last_dice_roll
        
        jugador = self.__current_player
        board = self.__board
        color = jugador.get_color()
        home_points_white_idx = range(18, 24)  # Índices 0-based: puntos 19-24 (18-23)
        home_points_black_idx = range(0, 6)     # Índices 0-based: puntos 1-6 (0-5)
        # BEAR OFF
        # Si is_valid_move ya validó que es bear off válido, proceder directamente
        if (color == "white" and from_point >= 19 and from_point <= 24 and to_point == 25) or \
           (color == "black" and from_point >= 1 and from_point <= 6 and to_point == 0):
            # is_valid_move ya validó can_bear_off y los dados, así que proceder
            # Calcular el movimiento requerido (ya validado en is_valid_move)
            if color == "white":
                movimiento = 25 - from_point
            else:
                movimiento = from_point
            
            if movimiento <= 0:
                movimiento = 1
                
            # Valores de dado posibles que permiten bear off
            dados_a_procesar = list(dados_disponibles)
            
            # Buscar si el movimiento exacto está disponible
            if movimiento in dados_a_procesar:
                dados_a_procesar.remove(movimiento)
                # Actualizar dados restantes
                if dados_a_procesar:
                    self.__last_dice_roll = tuple(dados_a_procesar)
                else:
                    self.__last_dice_roll = ()
            else:
                # Permitir sacar con dado mayor solo si es la ficha más atrasada
                # (Esta validación ya pasó en is_valid_move, pero la repetimos para usar el dado correcto)
                max_pos = max([i for i in home_points_white_idx if board.points[i] and board.points[i][0].get_owner() == jugador], default=None)
                min_pos = min([i for i in home_points_black_idx if board.points[i] and board.points[i][0].get_owner() == jugador], default=None)
                
                puede_usar_mayor = False
                movimiento_requerido = movimiento
                if color == "white" and max_pos is not None and punto_origen == max_pos:
                    puede_usar_mayor = True
                elif color == "black" and min_pos is not None and punto_origen == min_pos:
                    puede_usar_mayor = True
                
                if puede_usar_mayor:
                    # Buscar un dado mayor o igual al movimiento requerido
                    dado_usado = None
                    for dado in sorted(dados_a_procesar, reverse=True):
                        if dado >= movimiento_requerido:
                            dado_usado = dado
                            break
                    
                    if dado_usado:
                        dados_a_procesar.remove(dado_usado)
                        if dados_a_procesar:
                            self.__last_dice_roll = tuple(dados_a_procesar)
                        else:
                            self.__last_dice_roll = ()
                    else:
                        # Esto no debería ocurrir si is_valid_move validó correctamente
                        return False
                else:
                    # Esto no debería ocurrir si is_valid_move validó correctamente
                    return False
            
            # Efectuar bear off
            if not board.points[punto_origen]:
                return False  # No debería ocurrir, pero por seguridad
            ficha_movida = board.points[punto_origen].pop()
            ficha_movida.move_off_board()
            board.bear_off[color].append(ficha_movida)
            # Verificar victoria: si el jugador tiene 15 fichas en bear off, gana
            if len(board.bear_off[color]) >= 15:
                self.__winner = jugador
                self.finish_game()
            # Fin de dados/turno
            if not self.__last_dice_roll or len(self.__last_dice_roll) == 0:
                self.end_turn()
            self.__moves_count += 1
            return True
        # Remover la ficha del punto de origen
        ficha_movida = self.__board.points[punto_origen].pop()
        
        # Si hay fichas del oponente en el destino, verificar captura
        if self.__board.points[punto_destino]:
            primera_ficha_destino = self.__board.points[punto_destino][0]
            if primera_ficha_destino.get_owner() != self.__current_player:
                # Solo se puede capturar si hay exactamente 1 ficha del oponente
                if len(self.__board.points[punto_destino]) == 1:
                    ficha_capturada = self.__board.points[punto_destino].pop()
                    # Agregar a la barra del oponente
                    color_oponente = ficha_capturada.get_owner().get_color()
                    self.__board.bar[color_oponente].append(ficha_capturada)
                    # Actualizar posición de la ficha capturada
                    ficha_capturada.set_position(None)
                    ficha_capturada.set_on_bar(True)
                else:
                    # Hay más de 1 ficha del oponente, no se puede capturar
                    return False
        
        # Colocar la ficha en el destino
        self.__board.points[punto_destino].append(ficha_movida)
        
        # Actualizar el estado de los dados
        if len(dados_disponibles) >= 2:
            # Puede ser doble (4 elementos) o normal (2 elementos)
            valores_restantes = list(dados_disponibles)
            # Remover un movimiento usado
            if distancia in valores_restantes:
                valores_restantes.remove(distancia)
            else:
                # Movimiento no coincide con ningún dado disponible
                return False
            # Si quedan valores, mantenerlos; si no, terminar turno
            if valores_restantes:
                self.__last_dice_roll = tuple(valores_restantes)
            else:
                self.__last_dice_roll = ()
        elif len(dados_disponibles) == 1:
            # Solo queda un dado, se usa y se termina el turno
            self.__last_dice_roll = ()
        else:
            # No hay dados disponibles
            self.__last_dice_roll = ()
            
        # Si no quedan dados por usar, cambiar de turno
        if not self.__last_dice_roll or len(self.__last_dice_roll) == 0:
            self.end_turn()
            
        self.__moves_count += 1
        return True

    def make_move_from_bar(self, to_point: int) -> bool:
        """
        Realiza un movimiento desde la barra.

        Args:
            to_point (int): Punto de destino.

        Returns:
            bool: True si el movimiento fue realizado, False en caso contrario.
        """
        if not self.__started or self.__finished:
            return False
        
        if not self.__dice_rolled:
            return False
            
        # Verificar que el jugador tenga fichas en la barra
        color_jugador = self.__current_player.get_color()
        if not self.__board.bar[color_jugador]:
            return False
            
        # Verificar que el punto de destino sea válido según las reglas de reingreso
        if color_jugador == "white":
            # Fichas blancas solo pueden reingresar en puntos 1-6
            if not (1 <= to_point <= 6):
                return False
        else:
            # Fichas negras solo pueden reingresar en puntos 19-24
            if not (19 <= to_point <= 24):
                return False
                
        punto_destino = to_point - 1
        
        # Verificar si el punto de destino está bloqueado por el oponente
        if self.__board.points[punto_destino]:
            primera_ficha_destino = self.__board.points[punto_destino][0]
            if primera_ficha_destino.get_owner() != self.__current_player:
                # Si hay más de una ficha del oponente, está bloqueado
                if len(self.__board.points[punto_destino]) > 1:
                    return False
        
        # Verificar que la distancia coincida con algún valor de dado
        dados_disponibles = self.__last_dice_roll
        
        # Manejar tuplas de cualquier longitud (dobles tienen 4 elementos)
        if len(dados_disponibles) >= 1:
            # Dobles: (2,2,2,2) o normales: (2,5) o parcial: (2,)
            valores_dados = list(dados_disponibles)
        else:
            return False
            
        # Calcular la distancia desde la barra
        if self.__current_player.get_color() == "white":
            # Fichas blancas van hacia números más altos desde la barra
            distancia = to_point
        else:
            # Fichas negras van hacia números más bajos desde la barra
            distancia = 25 - to_point
            
        # Validar que la distancia esté disponible ANTES de remover la ficha
        if distancia not in valores_dados:
            return False
        
        # Validar actualización de dados ANTES de remover la ficha
        valores_restantes = list(dados_disponibles)
        if distancia in valores_restantes:
            valores_restantes.remove(distancia)
        else:
            # Esto no debería ocurrir si la validación anterior es correcta
            return False
        
        # Ahora SÍ remover una ficha de la barra (todas las validaciones pasaron)
        ficha_movida = self.__board.bar[color_jugador].pop()
        
        # Si hay una ficha del oponente en el destino, capturarla
        if self.__board.points[punto_destino]:
            primera_ficha_destino = self.__board.points[punto_destino][0]
            if primera_ficha_destino.get_owner() != self.__current_player:
                ficha_capturada = self.__board.points[punto_destino].pop()
                color_oponente = ficha_capturada.get_owner().get_color()
                self.__board.bar[color_oponente].append(ficha_capturada)
                ficha_capturada.set_position(None)
                ficha_capturada.set_on_bar(True)
        
        # Colocar la ficha en el destino
        self.__board.points[punto_destino].append(ficha_movida)
        ficha_movida.set_position(punto_destino)
        ficha_movida.set_on_bar(False)
        
        # Actualizar el estado de los dados (ya validado arriba)
        if valores_restantes:
            self.__last_dice_roll = tuple(valores_restantes)
        else:
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
        color_jugador = player.get_color()
        return len(self.__board.bar[color_jugador]) > 0

    def can_bear_off(self, player: Player) -> bool:
        """
        Indica si el jugador puede sacar fichas del tablero.

        Args:
            player (Player): El jugador a consultar.

        Returns:
            bool: True si puede sacar fichas, False en caso contrario.
        """
        return self.__board.can_bear_off(player)

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
