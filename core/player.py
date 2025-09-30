"""Módulo Player para Backgammon.

Define la clase Player que representa un jugador en el juego de Backgammon.
"""

from typing import Any


class Player:
    """Representa un jugador de Backgammon."""

    def __init__(self, name: str, color: str) -> None:
        """
        Inicializa un jugador con nombre y color.

        Args:
            name (str): Nombre del jugador.
            color (str): Color del jugador ("white" o "black").
        """
        if not name:
            raise ValueError("El nombre no puede estar vacío")
        if color not in ("white", "black"):
            raise ValueError("Color inválido")
        self.__name: str = name
        self.__color: str = color
        self.__checkers_count: int = 15
        self.__checkers_on_bar: int = 0
        self.__checkers_off_board: int = 0
        self.__winner: bool = False
        self.__can_move: bool = True
        self.__can_bear_off: bool = False

    def get_name(self) -> str:
        """Devuelve el nombre del jugador."""
        return self.__name

    def set_name(self, name: str) -> None:
        """Establece el nombre del jugador."""
        if not name:
            raise ValueError("El nombre no puede estar vacío")
        self.__name = name

    def get_color(self) -> str:
        """Devuelve el color del jugador."""
        return self.__color

    def set_color(self, color: str) -> None:
        """Establece el color del jugador."""
        if color not in ("white", "black"):
            raise ValueError("Color inválido")
        self.__color = color

    def get_checkers_count(self) -> int:
        """Devuelve la cantidad de fichas del jugador."""
        return self.__checkers_count

    def set_checkers_count(self, count: int) -> None:
        """Establece la cantidad de fichas del jugador."""
        if not 0 <= count <= 15:
            raise ValueError("Cantidad de fichas inválida")
        self.__checkers_count = count

    def get_checkers_on_bar(self) -> int:
        """Devuelve la cantidad de fichas en la barra."""
        return self.__checkers_on_bar

    def set_checkers_on_bar(self, count: int) -> None:
        """Establece la cantidad de fichas en la barra."""
        if count < 0:
            raise ValueError("Cantidad de fichas en la barra inválida")
        self.__checkers_on_bar = count

    def get_checkers_off_board(self) -> int:
        """Devuelve la cantidad de fichas fuera del tablero."""
        return self.__checkers_off_board

    def set_checkers_off_board(self, count: int) -> None:
        """Establece la cantidad de fichas fuera del tablero."""
        if count < 0:
            raise ValueError("Cantidad de fichas fuera del tablero inválida")
        self.__checkers_off_board = count

    def is_winner(self) -> bool:
        """Indica si el jugador es el ganador."""
        return self.__winner

    def set_winner(self, winner: bool) -> None:
        """Establece si el jugador es el ganador."""
        self.__winner = bool(winner)

    def can_move(self) -> bool:
        """Indica si el jugador puede mover."""
        return self.__can_move

    def set_can_move(self, can_move: bool) -> None:
        """Establece si el jugador puede mover."""
        self.__can_move = bool(can_move)

    def add_checker_to_bar(self) -> None:
        """Agrega una ficha a la barra."""
        self.__checkers_on_bar += 1

    def remove_checker_from_bar(self) -> None:
        """Remueve una ficha de la barra."""
        if self.__checkers_on_bar == 0:
            raise ValueError("No hay fichas en la barra para remover")
        self.__checkers_on_bar -= 1

    def add_checker_off_board(self) -> None:
        """Agrega una ficha fuera del tablero."""
        self.__checkers_off_board += 1

    def has_checkers_on_bar(self) -> bool:
        """Indica si el jugador tiene fichas en la barra."""
        return self.__checkers_on_bar > 0

    def can_bear_off(self) -> bool:
        """Indica si el jugador puede sacar fichas del tablero."""
        return self.__can_bear_off

    def set_can_bear_off(self, can_bear_off: bool) -> None:
        """Establece si el jugador puede sacar fichas del tablero."""
        self.__can_bear_off = bool(can_bear_off)

    def get_home_board_start(self) -> int:
        """Devuelve el inicio de la zona de casa del jugador."""
        return 19 if self.__color == "white" else 1

    def get_direction(self) -> int:
        """Devuelve la dirección de movimiento del jugador."""
        return -1 if self.__color == "white" else 1

    def __str__(self) -> str:
        """Representación en string del jugador."""
        return f"Player(name={self.__name}, color={self.__color}, checkers={self.__checkers_count})"

    def __eq__(self, other: Any) -> bool:
        """Compara dos jugadores."""
        if not isinstance(other, Player):
            return False
        # Comparación usando getters para respetar el encapsulamiento
        return self.get_name() == other.get_name() and self.get_color() == other.get_color()

    def __hash__(self) -> int:
        """Devuelve el hash del jugador."""
        return hash((self.__name, self.__color))

    def reset(self) -> None:
        """Reinicia el estado del jugador."""
        self.__checkers_count = 15
        self.__checkers_on_bar = 0
        self.__checkers_off_board = 0
        self.__winner = False
        self.__can_move = True
        self.__can_bear_off = False