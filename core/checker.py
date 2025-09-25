"""Módulo Checker para Backgammon.

Define la clase Checker que representa una ficha en el juego de Backgammon.
"""

from typing import Optional
from core.player import Player

class Checker:
    """Representa una ficha de Backgammon."""

    def __init__(self, owner: Player) -> None:
        """
        Inicializa una ficha con su propietario.

        Args:
            owner (Player): El jugador propietario de la ficha.
        """
        if owner is None:
            raise ValueError("El propietario no puede ser None")
        self.__owner: Player = owner
        self.__position: Optional[int] = None
        self.__on_bar: bool = False
        self.__off_board: bool = False

    def get_owner(self) -> Player:
        """Devuelve el propietario de la ficha."""
        return self.__owner

    def set_owner(self, owner: Player) -> None:
        """Establece el propietario de la ficha."""
        if owner is None:
            raise ValueError("El propietario no puede ser None")
        self.__owner = owner

    def get_color(self) -> str:
        """Devuelve el color de la ficha."""
        return self.__owner.get_color()

    def get_position(self) -> Optional[int]:
        """Devuelve la posición actual de la ficha en el tablero."""
        return self.__position

    def set_position(self, position: Optional[int]) -> None:
        """Establece la posición de la ficha en el tablero."""
        if position is not None and (position < 0 or position > 23):
            raise ValueError("Posición inválida")
        self.__position = position
        if position is not None:
            self.__on_bar = False
            self.__off_board = False

    def is_on_board(self) -> bool:
        """Indica si la ficha está en el tablero."""
        return self.__position is not None and not self.__on_bar and not self.__off_board

    def is_on_bar(self) -> bool:
        """Indica si la ficha está en la barra."""
        return self.__on_bar

    def set_on_bar(self, value: bool) -> None:
        """Establece si la ficha está en la barra."""
        self.__on_bar = value
        if value:
            self.__position = None
            self.__off_board = False

    def is_off_board(self) -> bool:
        """Indica si la ficha está fuera del tablero."""
        return self.__off_board

    def set_off_board(self, value: bool) -> None:
        """Establece si la ficha está fuera del tablero."""
        self.__off_board = value
        if value:
            self.__position = None
            self.__on_bar = False

    def move_to_position(self, position: int) -> None:
        """Mueve la ficha a una posición específica en el tablero."""
        self.set_position(position)
        self.__on_bar = False
        self.__off_board = False

    def move_to_bar(self) -> None:
        """Mueve la ficha a la barra."""
        self.__position = None
        self.__on_bar = True
        self.__off_board = False

    def move_off_board(self) -> None:
        """Mueve la ficha fuera del tablero."""
        self.__position = None
        self.__on_bar = False
        self.__off_board = True

    def can_move_to_position(self, position: int) -> bool:
        """Indica si la ficha puede moverse a una posición dada."""
        if self.is_off_board():
            return False
        if position < 0 or position > 23:
            return False
        if self.__position == position:
            return False
        return True

    def get_distance_to_position(self, position: int) -> Optional[int]:
        """Devuelve la distancia desde la posición actual a una nueva posición."""
        if self.__position is None:
            return None
        return position - self.__position

    def is_blot(self) -> bool:
        """Indica si la ficha está sola en un punto (blot)."""
        return self.is_on_board()

    def can_be_hit(self, opponent: Player) -> bool:
        """Indica si la ficha puede ser golpeada por el oponente."""
        return self.is_on_board() and self.__owner != opponent

    def hit_by_opponent(self) -> None:
        """Mueve la ficha a la barra tras ser golpeada por el oponente."""
        if not self.is_on_board():
            raise ValueError("La ficha no está en el tablero")
        self.move_to_bar()

    def reset_position(self) -> None:
        """Reinicia la posición de la ficha."""
        self.__position = None
        self.__on_bar = False
        self.__off_board = False

    def is_in_home_board(self) -> bool:
        """Indica si la ficha está en la zona de casa de su propietario."""
        if not self.is_on_board():
            return False
        if self.get_color() == "white":
            return 19 <= self.__position <= 23
        return 0 <= self.__position <= 5

    def can_bear_off(self) -> bool:
        """Indica si la ficha puede ser retirada del tablero."""
        return self.is_on_board() and self.is_in_home_board()

    def get_pip_value(self) -> int:
        """Devuelve el valor pip de la ficha."""
        if not self.is_on_board():
            return 0
        if self.get_color() == "white":
            return 24 - self.__position
        return self.__position + 1

    def get_direction(self) -> int:
        """Devuelve la dirección de movimiento de la ficha."""
        return -1 if self.get_color() == "white" else 1

    def is_moving_forward(self, target_position: int) -> bool:
        """Indica si la ficha se mueve hacia adelante."""
        if not self.is_on_board():
            raise ValueError("La ficha no está en el tablero")
        direction = self.get_direction()
        return (target_position - self.__position) * direction > 0

    def clone(self) -> "Checker":
        """Devuelve una copia de la ficha."""
        new_checker = Checker(self.__owner)
        new_checker.set_position(self.__position)
        new_checker.set_on_bar(self.__on_bar)
        new_checker.set_off_board(self.__off_board)
        return new_checker

    def __str__(self) -> str:
        """Representación en string de la ficha."""
        pos = self.__position
        if self.__on_bar:
            pos_str = "BAR"
        elif self.__off_board:
            pos_str = "OFF"
        else:
            pos_str = str(pos) if pos is not None else "None"
        return f"Checker(owner={self.__owner.get_name()}, color={self.get_color()}, position={pos_str})"

    def __eq__(self, other: object) -> bool:
        """Compara dos fichas."""
        if not isinstance(other, Checker):
            return False
        return (self.__owner == other.__owner and
                self.__position == other.__position and
                self.__on_bar == other.__on_bar and
                self.__off_board == other.__off_board)

    def __hash__(self) -> int:
        """Devuelve el hash de la ficha."""
        return hash((self.__owner, self.__position, self.__on_bar, self.__off_board))