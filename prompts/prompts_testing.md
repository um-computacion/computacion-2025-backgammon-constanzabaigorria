## Prompt [1] 

**Fecha**: 28-08-2025 
**Modelo/Herramienta**: ChatGPT (GPT-5) 
**Contexto**: creación de código para test de Dice

## Prompt enviado

crea un código de test para la clase de Dice

### Respuesta recibida

Los tests definidos comprueban lo siguiente:
- Que el método `roll()` devuelva una tupla con dos valores enteros.  
- Que los valores estén entre 1 y 6.  
- Que se detecten correctamente los dobles con un método `is_double()`.  

El código sugerido fue el siguiente:

```
import unittest
from core.dice import Dice

class TestDice(unittest.TestCase):

    def setUp(self):
        self.dice = Dice()

    def test_roll_returns_two_integers(self):
        result = self.dice.roll()
        self.assertIsInstance(result, tuple, "El resultado debe ser una tupla")
        self.assertEqual(len(result), 2, "Debe devolver dos valores")
        for value in result:
            self.assertIsInstance(value, int, "Cada valor debe ser entero")

    def test_roll_values_between_1_and_6(self):
        result = self.dice.roll()
        for value in result:
            self.assertGreaterEqual(value, 1, "El valor debe ser mayor o igual a 1")
            self.assertLessEqual(value, 6, "El valor debe ser menor o igual a 6")

    def test_double_detection(self):
        result = self.dice.roll()
        if result[0] == result[1]:
            self.assertTrue(self.dice.is_double(result), "Debe detectar dobles correctamente")
        else:
            self.assertFalse(self.dice.is_double(result), "No debe detectar doble cuando los valores son distintos")

if __name__ == "__main__":
    unittest.main()
```
## Uso de la respuesta

El código fue incorporado al archivo tal cual lo dió la IA, queda pendiente de revisión una vez que se cree tambien la clase Dice. Este se encuentra en rojo porque todavía no se implementó la clase Dice.

## Prompt [2] 

**Fecha**: 03-09-2025 
**Modelo/Herramienta**: GitHub Copilot (GPT-4.1)
**Contexto**: creación de código para test de Dice

## Prompt enviado

crea varios tests unitarios para la clase dice proporcionada

### Respuesta recibida

```
import unittest
from core.dice import Dice

class TestDice(unittest.TestCase):

    def setUp(self):
        self.dice = Dice()

    def test_roll_returns_list(self):
        result = self.dice.roll()
        self.assertIsInstance(result, list, "El resultado debe ser una lista")

    def test_roll_length(self):
        # Ejecutamos varias veces para cubrir dobles y no dobles
        found_double = False
        found_normal = False
        for _ in range(100):
            result = self.dice.roll()
            if len(result) == 2:
                found_normal = True
                self.assertNotEqual(result[0], result[1], "Si no es doble, los valores deben ser distintos")
            elif len(result) == 4:
                found_double = True
                self.assertTrue(all(x == result[0] for x in result), "Si es doble, todos los valores deben ser iguales")
            else:
                self.fail("La lista debe tener longitud 2 o 4")
        self.assertTrue(found_double, "Debe haber salido al menos un doble en 100 tiradas")
        self.assertTrue(found_normal, "Debe haber salido al menos una tirada normal en 100 tiradas")

    def test_values_between_1_and_6(self):
        for _ in range(50):
            result = self.dice.roll()
            for value in result:
                self.assertGreaterEqual(value, 1)
                self.assertLessEqual(value, 6)

    def test_get_last_roll(self):
        roll = self.dice.roll()
        self.assertEqual(roll, self.dice.get_last_roll(), "get_last_roll debe devolver el último resultado")

if __name__ == "__main__":
```

## Uso de la respuesta

Uso del código sin cambios 

## Prompt [3] 

**Fecha**: 03-09-2025 
**Modelo/Herramienta**: Claude Sonnet 4
**Contexto**: creación de código para test de Player en rojo

## Prompt enviado

crea varios tests unitarios para la clase player, siguiendo la metodología TDD (o sea que esten en rojo porque falta la clase)

### Respuesta recibida

```
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.player import Player
except ImportError:
    Player = None


class TestPlayer(unittest.TestCase):

    def setUp(self):
        if Player is None:
            self.skipTest("Clase Player no implementada aún")
        
        self.__player1__ = Player("Jugador1", "white")
        self.__player2__ = Player("Jugador2", "black")

    def test_player_creation_with_name_and_color(self):
        player = Player("TestPlayer", "white")
        self.assertEqual(player.get_name(), "TestPlayer")
        self.assertEqual(player.get_color(), "white")

    def test_player_name_getter(self):
        self.assertEqual(self.__player1__.get_name(), "Jugador1")

    def test_player_name_setter(self):
        self.__player1__.set_name("NuevoNombre")
        self.assertEqual(self.__player1__.get_name(), "NuevoNombre")

    def test_player_color_getter(self):
        self.assertEqual(self.__player1__.get_color(), "white")
        self.assertEqual(self.__player2__.get_color(), "black")

    def test_player_color_setter(self):
        self.__player1__.set_color("black")
        self.assertEqual(self.__player1__.get_color(), "black")

    def test_player_checkers_count_initial(self):
        self.assertEqual(self.__player1__.get_checkers_count(), 15)
        self.assertEqual(self.__player2__.get_checkers_count(), 15)

    def test_player_checkers_count_getter(self):
        count = self.__player1__.get_checkers_count()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_player_checkers_count_setter(self):
        self.__player1__.set_checkers_count(10)
        self.assertEqual(self.__player1__.get_checkers_count(), 10)

    def test_player_checkers_on_bar_initial(self):
        self.assertEqual(self.__player1__.get_checkers_on_bar(), 0)

    def test_player_checkers_on_bar_getter(self):
        count = self.__player1__.get_checkers_on_bar()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_player_checkers_on_bar_setter(self):
        self.__player1__.set_checkers_on_bar(3)
        self.assertEqual(self.__player1__.get_checkers_on_bar(), 3)

    def test_player_checkers_off_board_initial(self):
        self.assertEqual(self.__player1__.get_checkers_off_board(), 0)

    def test_player_checkers_off_board_getter(self):
        count = self.__player1__.get_checkers_off_board()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_player_checkers_off_board_setter(self):
        self.__player1__.set_checkers_off_board(5)
        self.assertEqual(self.__player1__.get_checkers_off_board(), 5)

    def test_player_is_winner_initial(self):
        self.assertFalse(self.__player1__.is_winner())

    def test_player_is_winner_setter(self):
        self.__player1__.set_winner(True)
        self.assertTrue(self.__player1__.is_winner())

    def test_player_can_move_initial(self):
        self.assertTrue(self.__player1__.can_move())

    def test_player_can_move_setter(self):
        self.__player1__.set_can_move(False)
        self.assertFalse(self.__player1__.can_move())

    def test_player_add_checker_to_bar(self):
        initial_count = self.__player1__.get_checkers_on_bar()
        self.__player1__.add_checker_to_bar()
        self.assertEqual(self.__player1__.get_checkers_on_bar(), initial_count + 1)

    def test_player_remove_checker_from_bar(self):
        self.__player1__.add_checker_to_bar()
        initial_count = self.__player1__.get_checkers_on_bar()
        self.__player1__.remove_checker_from_bar()
        self.assertEqual(self.__player1__.get_checkers_on_bar(), initial_count - 1)

    def test_player_remove_checker_from_bar_when_empty(self):
        with self.assertRaises(ValueError):
            self.__player1__.remove_checker_from_bar()

    def test_player_add_checker_off_board(self):
        initial_count = self.__player1__.get_checkers_off_board()
        self.__player1__.add_checker_off_board()
        self.assertEqual(self.__player1__.get_checkers_off_board(), initial_count + 1)

    def test_player_has_checkers_on_bar_true(self):
        self.__player1__.add_checker_to_bar()
        self.assertTrue(self.__player1__.has_checkers_on_bar())

    def test_player_has_checkers_on_bar_false(self):
        self.assertFalse(self.__player1__.has_checkers_on_bar())

    def test_player_can_bear_off_initial(self):
        self.assertFalse(self.__player1__.can_bear_off())

    def test_player_can_bear_off_setter(self):
        self.__player1__.set_can_bear_off(True)
        self.assertTrue(self.__player1__.can_bear_off())

    def test_player_get_home_board_start_white(self):
        white_player = Player("White", "white")
        self.assertEqual(white_player.get_home_board_start(), 19)

    def test_player_get_home_board_start_black(self):
        black_player = Player("Black", "black")
        self.assertEqual(black_player.get_home_board_start(), 1)

    def test_player_get_direction_white(self):
        white_player = Player("White", "white")
        self.assertEqual(white_player.get_direction(), -1)

    def test_player_get_direction_black(self):
        black_player = Player("Black", "black")
        self.assertEqual(black_player.get_direction(), 1)

    def test_player_invalid_color(self):
        with self.assertRaises(ValueError):
            Player("TestPlayer", "red")

    def test_player_empty_name(self):
        with self.assertRaises(ValueError):
            Player("", "white")

    def test_player_none_name(self):
        with self.assertRaises(ValueError):
            Player(None, "white")

    def test_player_negative_checkers_count(self):
        with self.assertRaises(ValueError):
            self.__player1__.set_checkers_count(-1)

    def test_player_excessive_checkers_count(self):
        with self.assertRaises(ValueError):
            self.__player1__.set_checkers_count(16)

    def test_player_negative_checkers_on_bar(self):
        with self.assertRaises(ValueError):
            self.__player1__.set_checkers_on_bar(-1)

    def test_player_negative_checkers_off_board(self):
        with self.assertRaises(ValueError):
            self.__player1__.set_checkers_off_board(-1)

    def test_player_string_representation(self):
        expected = "Player(name=Jugador1, color=white, checkers=15)"
        self.assertEqual(str(self.__player1__), expected)

    def test_player_equality_same_player(self):
        self.assertEqual(self.__player1__, self.__player1__)

    def test_player_equality_different_players(self):
        self.assertNotEqual(self.__player1__, self.__player2__)

    def test_player_equality_same_attributes(self):
        player3 = Player("Jugador1", "white")
        self.assertEqual(self.__player1__, player3)

    def test_player_hash_consistency(self):
        hash1 = hash(self.__player1__)
        hash2 = hash(self.__player1__)
        self.assertEqual(hash1, hash2)

    def test_player_reset_to_initial_state(self):
        self.__player1__.set_checkers_count(10)
        self.__player1__.add_checker_to_bar()
        self.__player1__.add_checker_off_board()
        self.__player1__.set_winner(True)
        
        self.__player1__.reset()
        
        self.assertEqual(self.__player1__.get_checkers_count(), 15)
        self.assertEqual(self.__player1__.get_checkers_on_bar(), 0)
        self.assertEqual(self.__player1__.get_checkers_off_board(), 0)
        self.assertFalse(self.__player1__.is_winner())
        self.assertTrue(self.__player1__.can_move())
        self.assertFalse(self.__player1__.can_bear_off())

    def test_player_checkers_conservation(self):
        self.__player1__.set_checkers_count(10)
        self.__player1__.set_checkers_on_bar(3)
        self.__player1__.set_checkers_off_board(2)
        
        total = (self.__player1__.get_checkers_count() + 
                self.__player1__.get_checkers_on_bar() + 
                self.__player1__.get_checkers_off_board())
        
        self.assertEqual(total, 15)


if __name__ == '__main__':
    unittest.main()
```

## Uso de la respuesta

Uso del código con modificaciones en las importaciones para que funcione.

## Prompt [4] 

**Fecha**: 08-09-2025  
**Modelo/Herramienta**: GitHub Copilot (GPT-4.1)  
**Contexto**: creación de la clase Player para pasar los tests definidos en test_player.py

## Prompt enviado

crea la clase para este test

### Respuesta recibida

```python
class Player:
    def __init__(self, name, color):
        if not name:
            raise ValueError("El nombre no puede estar vacío")
        if color not in ("white", "black"):
            raise ValueError("Color inválido")
        self.__name = name
        self.__color = color
        self.__checkers_count = 15
        self.__checkers_on_bar = 0
        self.__checkers_off_board = 0
        self.__winner = False
        self.__can_move = True
        self.__can_bear_off = False

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if not name:
            raise ValueError("El nombre no puede estar vacío")
        self.__name = name

    def get_color(self):
        return self.__color

    def set_color(self, color):
        if color not in ("white", "black"):
            raise ValueError("Color inválido")
        self.__color = color

    def get_checkers_count(self):
        return self.__checkers_count

    def set_checkers_count(self, count):
        if not (0 <= count <= 15):
            raise ValueError("Cantidad de fichas inválida")
        self.__checkers_count = count

    def get_checkers_on_bar(self):
        return self.__checkers_on_bar

    def set_checkers_on_bar(self, count):
        if count < 0:
            raise ValueError("Cantidad de fichas en la barra inválida")
        self.__checkers_on_bar = count

    def get_checkers_off_board(self):
        return self.__checkers_off_board

    def set_checkers_off_board(self, count):
        if count < 0:
            raise ValueError("Cantidad de fichas fuera del tablero inválida")
        self.__checkers_off_board = count

    def is_winner(self):
        return self.__winner

    def set_winner(self, winner):
        self.__winner = bool(winner)

    def can_move(self):
        return self.__can_move

    def set_can_move(self, can_move):
        self.__can_move = bool(can_move)

    def add_checker_to_bar(self):
        self.__checkers_on_bar += 1

    def remove_checker_from_bar(self):
        if self.__checkers_on_bar == 0:
            raise ValueError("No hay fichas en la barra para remover")
        self.__checkers_on_bar -= 1

    def add_checker_off_board(self):
        self.__checkers_off_board += 1

    def has_checkers_on_bar(self):
        return self.__checkers_on_bar > 0

    def can_bear_off(self):
        return self.__can_bear_off

    def set_can_bear_off(self, can_bear_off):
        self.__can_bear_off = bool(can_bear_off)

    def get_home_board_start(self):
        return 19 if self.__color == "white" else 1

    def get_direction(self):
        return -1 if self.__color == "white" else 1

    def __str__(self):
        return f"Player(name={self.__name}, color={self.__color}, checkers={self.__checkers_count})"

    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return (self.__name == other.__name and
                self.__color == other.__color and
                self.__checkers_count == other.__checkers_count and
                self.__checkers_on_bar == other.__checkers_on_bar and
                self.__checkers_off_board == other.__checkers_off_board)

    def __hash__(self):
        return hash((self.__name, self.__color, self.__checkers_count,
                     self.__checkers_on_bar, self.__checkers_off_board))

    def reset(self):
        self.__checkers_count = 15
        self.__checkers_on_bar = 0
        self.__checkers_off_board = 0
        self.__winner = False
        self.__can_move = True
        self.__can_bear_off = False
```

## Uso de la respuesta
Uso de código con modificaciones para que pasen todos los tests

