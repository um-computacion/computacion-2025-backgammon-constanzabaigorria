from core.checker import Checker

class Board:
    def __init__(self):
        self.__points = [[] for _ in range(24)]
        self.__bar = {}
        self.__off_board = {}

    def get_points(self):
        return self.__points

    def setup_initial_position(self, player1, player2):
        self.reset()
        self.__points[0] = [Checker(player1) for _ in range(2)]
        self.__points[11] = [Checker(player1) for _ in range(5)]
        self.__points[16] = [Checker(player1) for _ in range(3)]
        self.__points[18] = [Checker(player1) for _ in range(5)]
        self.__points[23] = [Checker(player2) for _ in range(2)]
        self.__points[12] = [Checker(player2) for _ in range(5)]
        self.__points[7] = [Checker(player2) for _ in range(3)]
        self.__points[5] = [Checker(player2) for _ in range(5)]

    def is_point_empty(self, point):
        return len(self.__points[point]) == 0

    def get_point_owner(self, point):
        if not self.__points[point]:
            return None
        return self.__points[point][0].get_owner()

    def get_checkers_count_on_point(self, point):
        if point < 0 or point > 23:
            raise ValueError("Punto inválido")
        return len(self.__points[point])

    def add_checker_to_point(self, point, checker):
        self.__points[point].append(checker)

    def remove_checker_from_point(self, point):
        if not self.__points[point]:
            raise ValueError("No hay fichas para remover")
        return self.__points[point].pop()

    def can_place_checker(self, point, player):
        if self.is_point_empty(point):
            return True
        owner = self.get_point_owner(point)
        if owner == player:
            return True
        return len(self.__points[point]) == 1

    def is_point_blocked(self, point, player):
        owner = self.get_point_owner(point)
        return owner is not None and owner != player and len(self.__points[point]) > 1

    def has_blot(self, point):
        return len(self.__points[point]) == 1

    def can_hit_blot(self, point, player):
        owner = self.get_point_owner(point)
        return self.has_blot(point) and owner is not None and owner != player

    def hit_blot(self, point, player):
        if not self.can_hit_blot(point, player):
            raise ValueError("No se puede golpear blot")
        return self.remove_checker_from_point(point)

    def get_bar_checkers_count(self, player):
        return len(self.__bar.get(player, []))

    def add_checker_to_bar(self, checker):
        owner = checker.get_owner()
        if owner not in self.__bar:
            self.__bar[owner] = []
        self.__bar[owner].append(checker)

    def remove_checker_from_bar(self, player):
        if self.get_bar_checkers_count(player) == 0:
            raise ValueError("No hay fichas en la barra")
        return self.__bar[player].pop()

    def has_checkers_on_bar(self, player):
        return self.get_bar_checkers_count(player) > 0

    def get_off_board_checkers_count(self, player):
        return len(self.__off_board.get(player, []))

    def add_checker_off_board(self, checker):
        owner = checker.get_owner()
        if owner not in self.__off_board:
            self.__off_board[owner] = []
        self.__off_board[owner].append(checker)

    def is_valid_point(self, point):
        return 0 <= point < 24

    def get_opposite_point(self, point):
        return 23 - point

    def is_in_home_board(self, point, player):
        if player.get_color() == "white":
            return 19 <= point <= 23
        else:
            return 0 <= point <= 5

    def can_bear_off(self, player):
        if self.has_checkers_on_bar(player):
            return False
        home_points = range(19, 24) if player.get_color() == "white" else range(0, 6)
        for i in range(24):
            if i not in home_points:
                for checker in self.__points[i]:
                    if checker.get_owner() == player:
                        return False
        return True

    def get_furthest_checker(self, player):
        if player.get_color() == "white":
            for i in range(24):
                if any(c.get_owner() == player for c in self.__points[i]):
                    return i
        else:
            for i in reversed(range(24)):
                if any(c.get_owner() == player for c in self.__points[i]):
                    return i
        return None

    def count_checkers_on_board(self, player):
        return sum(1 for i in range(24) for c in self.__points[i] if c.get_owner() == player)

    def get_all_checker_positions(self, player):
        return [i for i in range(24) if any(c.get_owner() == player for c in self.__points[i])]

    def clear_point(self, point):
        cleared = self.__points[point][:]
        self.__points[point] = []
        return cleared

    def reset(self):
        self.__points = [[] for _ in range(24)]
        self.__bar = {}
        self.__off_board = {}

    def copy(self):
        import copy
        return copy.deepcopy(self)

    def __str__(self):
        return f"Board({self.__points})"

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        return self.__points == other.__points and self.__bar == other.__bar and self.__off_board == other.__off_board

    def __hash__(self):
        return hash((tuple(tuple(point) for point in self.__points),
                     tuple(sorted((k, tuple(v)) for k, v in self.__bar.items())),
                     tuple(sorted((k, tuple(v)) for k, v in self.__off_board.items()))))

    def calculate_pip_count(self, player):
        pip = 0
        for i in range(24):
            for checker in self.__points[i]:
                if checker.get_owner() == player:
                    pip += (24 - i) if player.get_color() == "white" else (i + 1)
        return pip

    def get_moves_to_bear_off(self, player):
        return []

    def is_race_position(self):
        return True