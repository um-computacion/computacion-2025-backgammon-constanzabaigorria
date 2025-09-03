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

## Prompt [1] 

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