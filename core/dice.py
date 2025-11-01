"""Módulo Dice para Backgammon.

Define la clase Dice que representa los dados utilizados en el juego de Backgammon.
"""

import random
from typing import List, Tuple


class Dice:
    """Representa los dados del juego de Backgammon."""

    def __init__(self, sides: int = 6) -> None:
        """
        Inicializa los dados.

        Args:
            sides (int): Número de caras de los dados.
        """
        self.__sides: int = sides
        self.__last_roll: Tuple[int, int] = (1, 1)

    def roll(self) -> Tuple[int, int]:
        """
        Lanza los dados y guarda el resultado.

        Returns:
            Tuple[int, int]: Resultado del lanzamiento de los dos dados.
        """
        die1: int = random.randint(1, self.__sides)
        die2: int = random.randint(1, self.__sides)
        self.__last_roll = (die1, die2)
        return self.__last_roll

    def get_last_roll(self) -> Tuple[int, int]:
        """
        Devuelve el último lanzamiento de los dados.

        Returns:
            Tuple[int, int]: Último resultado de los dados.
        """
        return self.__last_roll

    def set_last_roll(self, roll: Tuple[int, int]) -> None:
        """
        Establece el último lanzamiento de los dados.

        Args:
            roll (Tuple[int, int]): Resultado a establecer.
        """
        self.__last_roll = roll

    def get_sides(self) -> int:
        """
        Devuelve el número de caras de los dados.

        Returns:
            int: Número de caras.
        """
        return self.__sides

    def set_sides(self, sides: int) -> None:
        """
        Establece el número de caras de los dados.

        Args:
            sides (int): Número de caras.
        """
        self.__sides = sides

    def is_double(self, roll: Tuple[int, int]) -> bool:
        """
        Indica si el lanzamiento es doble.

        Args:
            roll (Tuple[int, int]): Resultado de los dados.

        Returns:
            bool: True si ambos dados tienen el mismo valor, False en caso contrario.
        """
        return roll[0] == roll[1]

    def get_moves(self, roll: Tuple[int, int]) -> List[int]:
        """
        Devuelve los movimientos posibles según el lanzamiento.

        Args:
            roll (Tuple[int, int]): Resultado de los dados.

        Returns:
            List[int]: Lista de movimientos posibles.
        """
        if self.is_double(roll):
            return [roll[0]] * 4
        return [roll[0], roll[1]]
