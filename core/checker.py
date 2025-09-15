from typing import Optional
from core.player import Player

class Checker:

    def __init__(self, owner: Player) -> None:
       
        if owner is None:
            raise ValueError("El propietario no puede ser None")
        self.__owner: Player = owner
        self.__position: Optional[int] = None
        self.__on_bar: bool = False
        self.__off_board: bool = False

    def get_owner(self) -> Player:
        return self.__owner

    def set_owner(self, owner: Player) -> None:
     
        if owner is None:
            raise ValueError("El propietario no puede ser None")
        self.__owner = owner

    def get_color(self) -> str:
        return self.__owner.get_color()

    def get_position(self) -> Optional[int]:
        return self.__position

    def set_position(self, position: Optional[int]) -> None:

        if position is not None and (position < 0 or position > 23):
            raise ValueError("Posición inválida")
        self.__position = position
        if position is not None:
            self.__on_bar = False
            self.__off_board = False

    def is_on_board(self) -> bool:
        return self.__position is not None and not self.__on_bar and not self.__off_board

    def is_on_bar(self) -> bool:
        return self.__on_bar

    def set_on_bar(self, value: bool) -> None:

        self.__on_bar = value
        if value:
            self.__position = None
            self.__off_board = False

    def is_off_board(self) -> bool:
        return self.__off_board

    def set_off_board(self, value: bool) -> None:

        self.__off_board = value
        if value:
            self.__position = None
            self.__on_bar = False

    def move_to_position(self, position: int) -> None:

        self.set_position(position)
        self.__on_bar = False
        self.__off_board = False

    def move_to_bar(self) -> None:

        self.__position = None
        self.__on_bar = True
        self.__off_board = False

    def move_off_board(self) -> None:

        self.__position = None
        self.__on_bar = False
        self.__off_board = True

    def can_move_to_position(self, position: int) -> bool:

        if self.is_off_board():
            return False
        if position < 0 or position > 23:
            return False
        if self.__position == position:
            return False
        return True

    def get_distance_to_position(self, position: int) -> Optional[int]:

        if self.__position is None:
            return None
        return position - self.__position

    def is_blot(self) -> bool:

        return self.is_on_board()

    def can_be_hit(self, opponent: Player) -> bool:

        return self.is_on_board() and self.__owner != opponent

    def hit_by_opponent(self) -> None:

        if not self.is_on_board():
            raise ValueError("La ficha no está en el tablero")
        self.move_to_bar()

    def reset_position(self) -> None:
 
        self.__position = None
        self.__on_bar = False
        self.__off_board = False

    def is_in_home_board(self) -> bool:
  
        if not self.is_on_board():
            return False
        if self.get_color() == "white":
            return 19 <= self.__position <= 23
        else:
            return 0 <= self.__position <= 5

    def can_bear_off(self) -> bool:

        return self.is_on_board() and self.is_in_home_board()

    def get_pip_value(self) -> int:

        if not self.is_on_board():
            return 0
        if self.get_color() == "white":
            return 24 - self.__position
        else:
            return self.__position + 1

    def get_direction(self) -> int:

        return -1 if self.get_color() == "white" else 1

    def is_moving_forward(self, target_position: int) -> bool:

        if not self.is_on_board():
            raise ValueError("La ficha no está en el tablero")
        direction = self.get_direction()
        return (target_position - self.__position) * direction > 0

    def clone(self) -> "Checker":

        new_checker = Checker(self.__owner)
        new_checker.set_position(self.__position)
        new_checker.set_on_bar(self.__on_bar)
        new_checker.set_off_board(self.__off_board)
        return new_checker

    def __str__(self) -> str:

        pos = self.__position
        if self.__on_bar:
            pos_str = "BAR"
        elif self.__off_board:
            pos_str = "OFF"
        else:
            pos_str = str(pos) if pos is not None else "None"
        return f"Checker(owner={self.__owner.get_name()}, color={self.get_color()}, position={pos_str})"

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Checker):
            return False
        return (self.__owner == other.__owner and
                self.__position == other.__position and
                self.__on_bar == other.__on_bar and
                self.__off_board == other.__off_board)

    def __hash__(self) -> int:

        return hash((self.__owner, self.__position, self.__on_bar, self.__off_board))