"""Módulo Board para Backgammon.

Gestiona el estado del tablero, las fichas, la barra y las fichas fuera del tablero.
"""
import copy

from typing import List, Dict, Any, Optional
from core.checker import Checker
from core.player import Player

class Board:
    """Representa el tablero de Backgammon."""

    def __init__(self) -> None:
        """
        Inicializa el tablero con 24 puntos vacíos.
        """
        self.points: List[List['Checker']] = [[] for _ in range(24)]
        self.bar: Dict[str, List['Checker']] = {"white": [], "black": []}
        self.bear_off: Dict[str, List['Checker']] = {"white": [], "black": []}

    def get_points(self) -> List[List[Checker]]:
        """Devuelve la lista de puntos del tablero."""
        return self.points

    def setup_initial_position(self, player1: 'Player', player2: 'Player') -> None:
        """
        Coloca las fichas en la posición inicial estándar de Backgammon.

        Args:
            player1 (Player): Jugador blanco.
            player2 (Player): Jugador negro.
        """
        self.points = [[] for _ in range(24)]
        # Blanco (white)
        self.points[0] = [Checker(player1) for _ in range(2)]      # Punto 1: 2 fichas blancas
        self.points[11] = [Checker(player1) for _ in range(5)]     # Punto 12: 5 fichas blancas
        self.points[16] = [Checker(player1) for _ in range(3)]     # Punto 17: 3 fichas blancas
        self.points[18] = [Checker(player1) for _ in range(5)]     # Punto 19: 5 fichas blancas
        # Negro (black)
        self.points[23] = [Checker(player2) for _ in range(2)]     # Punto 24: 2 fichas negras
        self.points[12] = [Checker(player2) for _ in range(5)]     # Punto 13: 5 fichas negras
        self.points[7] = [Checker(player2) for _ in range(3)]      # Punto 8: 3 fichas negras
        self.points[5] = [Checker(player2) for _ in range(5)]      # Punto 6: 5 fichas negras

    def is_point_empty(self, point: int) -> bool:
        """Indica si el punto está vacío."""
        return len(self.points[point]) == 0

    def get_point_owner(self, point: int) -> Optional[Player]:
        """Devuelve el propietario del punto."""
        if not self.points[point]:
            return None
        return self.points[point][0].get_owner()

    def get_checkers_count_on_point(self, point: int) -> int:
        """Devuelve la cantidad de fichas en el punto."""
        if point < 0 or point > 23:
            raise ValueError("Punto inválido")
        return len(self.points[point])

    def add_checker_to_point(self, point: int, checker: Checker) -> None:
        """Agrega una ficha al punto."""
        self.points[point].append(checker)

    def remove_checker_from_point(self, point: int) -> Checker:
        """Remueve una ficha del punto."""
        if not self.points[point]:
            raise ValueError("No hay fichas para remover")
        return self.points[point].pop()

    def can_place_checker(self, point: int, player: Player) -> bool:
        """Indica si se puede colocar una ficha en el punto."""
        if self.is_point_empty(point):
            return True
        owner = self.get_point_owner(point)
        if owner == player:
            return True
        return len(self.points[point]) == 1

    def is_point_blocked(self, point: int, player: Player) -> bool:
        """Indica si el punto está bloqueado para el jugador."""
        owner = self.get_point_owner(point)
        return owner is not None and owner != player and len(self.points[point]) > 1

    def has_blot(self, point: int) -> bool:
        """Indica si el punto tiene un blot (solo una ficha)."""
        return len(self.points[point]) == 1

    def can_hit_blot(self, point: int, player: Player) -> bool:
        """Indica si el jugador puede golpear el blot en el punto."""
        owner = self.get_point_owner(point)
        return self.has_blot(point) and owner is not None and owner != player

    def hit_blot(self, point: int, player: Player) -> Checker:
        """Golpea el blot en el punto y lo remueve."""
        if not self.can_hit_blot(point, player):
            raise ValueError("No se puede golpear blot")
        return self.remove_checker_from_point(point)

    def get_bar_checkers_count(self, player: Player) -> int:
        """Devuelve la cantidad de fichas en la barra para el jugador."""
        color = player.get_color()
        return len(self.bar.get(color, []))

    def add_checker_to_bar(self, checker: Checker) -> None:
        """Agrega una ficha a la barra."""
        owner = checker.get_owner()
        if owner not in self.bar:
            self.bar[owner] = []
        self.bar[owner].append(checker)

    def remove_checker_from_bar(self, player: Player) -> Checker:
        """Remueve una ficha de la barra del jugador."""
        if self.get_bar_checkers_count(player) == 0:
            raise ValueError("No hay fichas en la barra")
        return self.bar[player].pop()

    def has_checkers_on_bar(self, player: Player) -> bool:
        """Indica si el jugador tiene fichas en la barra."""
        return self.get_bar_checkers_count(player) > 0

    def get_off_board_checkers_count(self, player: Player) -> int:
        """Devuelve la cantidad de fichas fuera del tablero para el jugador."""
        return len(self.bear_off.get(player, []))

    def add_checker_off_board(self, checker: Checker) -> None:
        """Agrega una ficha fuera del tablero."""
        owner = checker.get_owner()
        if owner not in self.bear_off:
            self.bear_off[owner] = []
        self.bear_off[owner].append(checker)

    def get_bar(self) -> Dict[Player, List[Checker]]:
        """Devuelve la barra de fichas."""
        return self.bar

    def get_off_board(self) -> Dict[Player, List[Checker]]:
        """Devuelve las fichas fuera del tablero."""
        return self.bear_off

    def is_valid_point(self, point: int) -> bool:
        """Indica si el punto es válido en el tablero."""
        return 0 <= point < 24

    def get_opposite_point(self, point: int) -> int:
        """Devuelve el punto opuesto en el tablero."""
        return 23 - point

    def is_in_home_board(self, point: int, player: Player) -> bool:
        """Indica si el punto está en la zona de casa del jugador."""
        if player.get_color() == "white":
            return 19 <= point <= 23
        return 0 <= point <= 5

    def can_bear_off(self, player: Player) -> bool:
        """Indica si el jugador puede sacar fichas del tablero."""
        if self.has_checkers_on_bar(player):
            return False
        # Los puntos del tablero usan índices 0-based (0-23)
        # Home board de blancas: puntos 19-24 (índices 18-23)
        # Home board de negras: puntos 1-6 (índices 0-5)
        home_points = range(18, 24) if player.get_color() == "white" else range(0, 6)
        for i in range(24):
            if i not in home_points:
                for checker in self.points[i]:
                    if checker.get_owner() == player:
                        return False
        return True

    def get_furthest_checker(self, player: Player) -> Optional[int]:
        """Devuelve la posición de la ficha más lejana del jugador."""
        if player.get_color() == "white":
            for i in range(24):
                if any(c.get_owner() == player for c in self.points[i]):
                    return i
        else:
            for i in reversed(range(24)):
                if any(c.get_owner() == player for c in self.points[i]):
                    return i
        return None

    def count_checkers_on_board(self, player: Player) -> int:
        """Cuenta las fichas del jugador en el tablero."""
        return sum(1 for i in range(24) for c in self.points[i] if c.get_owner() == player)

    def get_all_checker_positions(self, player: Player) -> List[int]:
        """Devuelve todas las posiciones de fichas del jugador en el tablero."""
        return [i for i in range(24) if any(c.get_owner() == player for c in self.points[i])]

    def clear_point(self, point: int) -> List[Checker]:
        """Limpia el punto y devuelve las fichas que había."""
        cleared = self.points[point][:]
        self.points[point] = []
        return cleared

    def reset(self) -> None:
        """
        Reinicia el tablero a la posición inicial vacía.
        """
        self.points = [[] for _ in range(24)]
        self.bar = {"white": [], "black": []}
        self.bear_off = {"white": [], "black": []}

    def copy(self) -> "Board":
        """Devuelve una copia profunda del tablero."""
        return copy.deepcopy(self)

    def __str__(self) -> str:
        """
        Devuelve una representación simple del tablero mostrando la cantidad de fichas en cada punto.
        """
        return str([len(point) for point in self.points])

    def __eq__(self, other: object) -> bool:
        """Compara dos tableros."""
        if not isinstance(other, Board):
            return False
        # Comparación usando getters para respetar el encapsulamiento
        # y evitar acceso directo a atributos privados
        return (
            self.get_points() == other.get_points() and
            self.get_bar() == other.get_bar() and
            self.get_off_board() == other.get_off_board()
        )

    def __hash__(self) -> int:
        """Devuelve el hash del tablero."""
        return hash((tuple(tuple(point) for point in self.points),
                     tuple(sorted((k, tuple(v)) for k, v in self.bar.items())),
                     tuple(sorted((k, tuple(v)) for k, v in self.bear_off.items()))))

    def calculate_pip_count(self, player: Player) -> int:
        """Calcula el pip count del jugador."""
        pip = 0
        for i in range(24):
            for checker in self.points[i]:
                if checker.get_owner() == player:
                    pip += (24 - i) if player.get_color() == "white" else (i + 1)
        return pip

    def get_moves_to_bear_off(self, player: Player) -> List[Any]:
        """
        Devuelve los movimientos posibles para sacar fichas del tablero.

        Args:
            player (Player): El jugador para el que se calculan los movimientos.

        Returns:
            List[Any]: Lista de movimientos posibles para sacar fichas.
        """
        # Implementación de ejemplo: retorna una lista vacía.
        return []

    def is_race_position(self) -> bool:
        """Indica si la posición es de carrera."""
        players = set()
        for point in self.points:
            for checker in point:
                players.add(checker.get_owner())
        if len(players) != 2:
            return True
        white_outside_home = any(
            checker.get_owner().get_color() == "white" and not (18 <= i <= 23)
            for i, point in enumerate(self.points)
            for checker in point
        )
        black_outside_home = any(
            checker.get_owner().get_color() == "black" and not (0 <= i <= 5)
            for i, point in enumerate(self.points)
            for checker in point
        )
        if white_outside_home and black_outside_home:
            return False
        return True
