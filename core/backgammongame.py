from typing import Optional, List, Dict, Any
from core.player import Player
from core.board import Board
from core.dice import Dice
from core.checker import Checker  

class BackgammonGame:

    def __init__(self, player1_name: str = "Player 1", player2_name: str = "Player 2") -> None:
       
        if not player1_name or not player2_name:
            raise ValueError("Los nombres de los jugadores no pueden estar vacíos")
        if player1_name == player2_name:
            raise ValueError("Los nombres de los jugadores deben ser distintos")
        self.__player1: Player = Player(player1_name, "white")
        self.__player2: Player = Player(player2_name, "black")
        self.__board: Board = Board()
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

    def setup_initial_position(self) -> None:
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
        return self.__player1_checkers

    def get_player2_checkers(self) -> List[Checker]:
        return self.__player2_checkers

    def get_player1(self) -> Player:
        return self.__player1

    def get_player2(self) -> Player:
        return self.__player2

    def get_board(self) -> Board:
        return self.__board

    def get_dice(self) -> Dice:
        return self.__dice

    def get_current_player(self) -> Player:
        return self.__current_player

    def set_current_player(self, player: Player) -> None:
        if player not in [self.__player1, self.__player2]:
            raise ValueError("Jugador inválido")
        self.__current_player = player

    def is_started(self) -> bool:
        return self.__started

    def start_game(self) -> None:
        self.__started = True
        self.__finished = False
        self.__winner = None
        self.__turn_number = 1
        self.__moves_count = 0
        self.__dice_rolled = False
        self.__last_dice_roll = None
        self.__move_history.clear()
        self.__board.reset()
        self.__current_player = self.__player1

    def is_finished(self) -> bool:
        return self.__finished

    def finish_game(self) -> None:
        self.__finished = True
        self.__started = False

    def get_winner(self) -> Optional[Player]:
        return self.__winner

    def set_winner(self, player: Player) -> None:
        if player not in [self.__player1, self.__player2]:
            raise ValueError("Jugador inválido")
        self.__winner = player

    def switch_player(self) -> None:
        self.__current_player = self.__player2 if self.__current_player == self.__player1 else self.__player1

    def roll_dice(self) -> tuple:
        if self.__finished:
            raise ValueError("El juego ha finalizado")
    
        roll = self.__dice.roll()
        self.__last_dice_roll = tuple(roll[:2])
        self.__dice_rolled = True
        return self.__last_dice_roll

    def get_last_dice_roll(self) -> tuple:
        return self.__last_dice_roll if self.__last_dice_roll else (1, 1)

    def has_dice_been_rolled(self) -> bool:
        return self.__dice_rolled

    def get_available_moves(self) -> List[Any]:
        return []

    def is_valid_move(self, from_point: int, to_point: int) -> bool:
        return True

    def make_move(self, from_point: int, to_point: int) -> bool:
        if not self.__started:
            raise ValueError("El juego no ha comenzado")
        if self.__finished:
            raise ValueError("El juego ha finalizado")
        if not  self.__dice_rolled:
            raise ValueError("Debe tirar los dados antes de mover")
        self.__moves_count += 1
        return True

    def can_player_move(self, player: Player) -> bool:
        return True

    def must_enter_from_bar(self, player: Player) -> bool:
        return False

    def can_bear_off(self, player: Player) -> bool:
        return True

    def check_win_condition(self) -> bool:
        return self.__winner is not None

    def get_game_state(self) -> Dict[str, Any]:
        return {
            "started": self.__started,
            "finished": self.__finished,
            "current_player": self.__current_player.get_name()
        }

    def get_moves_count(self) -> int:
        return self.__moves_count

    def get_turn_number(self) -> int:
        return self.__turn_number

    def end_turn(self) -> None:
        self.__turn_number += 1
        self.switch_player()
        self.__dice_rolled = False
        self.__last_dice_roll = None

    def reset_game(self) -> None:
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
        return 0

    def is_race_position(self) -> bool:
        return True

    def get_match_score(self, player: Player) -> int:
        return self.__match_score.get(player, 0)

    def set_match_score(self, player: Player, score: int) -> None:
        if score < 0:
            raise ValueError("El puntaje no puede ser negativo")
        self.__match_score[player] = score

    def is_double_offered(self) -> bool:
        return self.__double_offered

    def offer_double(self, player: Player) -> None:
        if self.__double_offered:
            raise ValueError("Ya se ha ofrecido el doble")
        self.__double_offered = True
        self.__doubling_cube_owner = player

    def accept_double(self) -> None:
        if not self.__double_offered:
            raise ValueError("No se ha ofrecido el doble")
        self.__doubling_cube_value *= 2
        self.__double_offered = False

    def decline_double(self) -> None:
        if not self.__double_offered:
            raise ValueError("No se ha ofrecido el doble")
        self.__finished = True

    def get_doubling_cube_value(self) -> int:
        return self.__doubling_cube_value

    def get_doubling_cube_owner(self) -> Optional[Player]:
        return self.__doubling_cube_owner

    def can_offer_double(self, player: Player) -> bool:
        return not self.__double_offered

    def get_game_type(self) -> str:
        return self.__game_type

    def calculate_game_value(self) -> int:
        return self.__doubling_cube_value

    def save_game_state(self) -> Dict[str, Any]:
        return {
            "turn_number": self.__turn_number
        }

    def load_game_state(self, state: Dict[str, Any]) -> None:
        if "turn_number" not in state:
            raise ValueError("Estado inválido")
        self.__turn_number = state["turn_number"]

    def get_move_history(self) -> List[Any]:
        return self.__move_history

    def add_move_to_history(self, move: Any) -> None:
        self.__move_history.append(move)

    def undo_last_move(self) -> bool:
        if not self.__move_history:
            return False
        self.__move_history.pop()
        return True

    def can_undo_move(self) -> bool:
        return bool(self.__move_history)

    def get_possible_moves_count(self) -> int:
        return 0

    def is_forced_move(self) -> bool:
        return False

    def get_forced_moves(self) -> List[Any]:
        return []

    def validate_game_state(self) -> bool:
        return True

    def get_statistics(self) -> Dict[str, Any]:
        return {}

    def __str__(self) -> str:
        return f"BackgammonGame(turn={self.__turn_number}, started={self.__started})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BackgammonGame):
            return False
        return self.__turn_number == other.__turn_number and self.__started == other.__started

    def __hash__(self) -> int:
        return hash((self.__turn_number, self.__started))