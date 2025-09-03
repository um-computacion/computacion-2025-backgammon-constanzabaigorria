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
    unittest.main()

