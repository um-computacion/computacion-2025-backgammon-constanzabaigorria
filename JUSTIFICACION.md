# Justificación del Diseño - Backgammon en Python

## 1. Resumen del Diseño General

El proyecto implementa un juego completo de Backgammon siguiendo una **arquitectura modular por capas**, separando claramente la lógica de negocio de las interfaces de usuario. El diseño se basa en **Programación Orientada a Objetos** con encapsulación estricta y principios **SOLID**.

### 1.1 Arquitectura General

El sistema está estructurado en tres capas principales:

```
┌─────────────────────────────────────────┐
│         Capa de Presentación            │
│  (CLI Interface / Pygame UI)            │
└─────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│         Capa de Lógica de Negocio       │
│  (BackgammonGame, Board, Player, etc.)  │
└─────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│         Capa de Datos                   │
│  (Estructuras de datos: Checker, Dice)  │
└─────────────────────────────────────────┘
```

**Justificación**: Esta separación permite:
- **Mantenibilidad**: Cambios en la UI no afectan la lógica de negocio
- **Testabilidad**: Cada capa puede probarse independientemente
- **Extensibilidad**: Fácil agregar nuevas interfaces (web, móvil) sin modificar lógica
- **Reutilización**: La lógica de juego puede usarse en diferentes contextos

### 1.2 Modelo de Dominio

El juego se modela mediante cinco clases principales:
- **`BackgammonGame`**: Orquestador principal del juego
- **`Board`**: Gestión del estado del tablero
- **`Player`**: Representación de jugadores
- **`Checker`**: Representación de fichas individuales
- **`Dice`**: Gestión de lanzamiento de dados

## 2. Justificación de las Clases Elegidas

### 2.1 Clase `Player`

**Responsabilidades**:
- Almacenar información del jugador (nombre, color)
- Gestionar contadores de fichas (en tablero, en barra, fuera)
- Determinar dirección de movimiento y zona de home board
- Manejar estado del jugador (puede mover, puede hacer bear off, es ganador)

**Por qué se eligió esta clase**:
- **Encapsulación de datos**: Centraliza toda la información relacionada con un jugador
- **Reutilización**: El mismo objeto `Player` puede usarse en diferentes contextos (CLI, GUI)
- **Validación centralizada**: Los setters validan la consistencia de los datos
- **Separación de responsabilidades**: El jugador no conoce las reglas del juego, solo su estado

**Principios aplicados**:
- **SRP (Single Responsibility)**: La clase solo gestiona información del jugador
- **Encapsulación**: Todos los atributos son privados (`__nombre_atributo`)

### 2.2 Clase `Checker`

**Responsabilidades**:
- Representar una ficha individual del juego
- Gestionar posición actual (en tablero, en barra, fuera)
- Determinar si está en home board según su propietario
- Calcular valores pip y distancias

**Por qué se eligió esta clase**:
- **Modelado del dominio**: En Backgammon, cada ficha es una entidad con estado propio
- **Flexibilidad**: Permite mover fichas individualmente sin afectar otras
- **Estado explícito**: Los tres estados posibles (tablero, barra, fuera) son mutuamente excluyentes y claros
- **Reutilización**: El mismo objeto puede estar en diferentes posiciones durante el juego

**Principios aplicados**:
- **SRP**: Solo gestiona el estado y propiedades de una ficha
- **Encapsulación**: Estado interno protegido

### 2.3 Clase `Board`

**Responsabilidades**:
- Mantener el estado de los 24 puntos del tablero
- Gestionar fichas en la barra y fuera del tablero
- Validar operaciones sobre puntos (agregar, remover, verificar propiedad)
- Calcular propiedades del tablero (pip count, posición más lejana)

**Por qué se eligió esta clase**:
- **Abstracción del tablero**: Representa el concepto central del juego de Backgammon
- **Centralización de operaciones**: Todas las operaciones sobre el tablero están en un solo lugar
- **Independencia de reglas**: El tablero solo gestiona estado, no reglas de juego
- **Facilita testing**: Estado del tablero puede verificarse fácilmente

**Principios aplicados**:
- **SRP**: Solo gestiona el estado físico del tablero
- **OCP (Open/Closed)**: Extensible mediante métodos adicionales sin modificar existentes

### 2.4 Clase `Dice`

**Responsabilidades**:
- Generar lanzamientos aleatorios de dados
- Detectar si un lanzamiento es doble
- Calcular movimientos disponibles según el lanzamiento
- Almacenar el último lanzamiento

**Por qué se eligió esta clase**:
- **Abstracción del dado**: Separa la lógica de dados del resto del juego
- **Testabilidad**: Permite mockear lanzamientos para tests determinísticos
- **Reutilización**: Puede usarse independientemente del resto del juego
- **Configurabilidad**: Permite cambiar número de caras (extensibilidad)

**Principios aplicados**:
- **SRP**: Solo gestiona lanzamiento y análisis de dados
- **Encapsulación**: Estado interno protegido

### 2.5 Clase `BackgammonGame`

**Responsabilidades**:
- Orquestar el flujo completo del juego
- Coordinar entre `Player`, `Board`, `Dice`, y `Checker`
- Validar y ejecutar movimientos según reglas de Backgammon
- Gestionar turnos, estado del juego, y condición de victoria
- Mantener historial de movimientos

**Por qué se eligió esta clase**:
- **Facade Pattern**: Proporciona interfaz simplificada a toda la funcionalidad del juego
- **Coordinación central**: Centraliza la lógica de reglas y flujo del juego
- **Abstracción de alto nivel**: Las interfaces (CLI/GUI) solo interactúan con esta clase
- **Estado global**: Mantiene el estado completo del juego en un solo lugar

**Principios aplicados**:
- **Facade Pattern**: Simplifica interacciones entre múltiples clases
- **Dependency Injection**: Recibe objetos pero no los crea directamente (Player, Board, Dice)

### 2.6 Clases de Interfaz

#### `CLIInterface` (cli/cli.py)
**Responsabilidades**: Interacción por línea de comandos, visualización de tablero, entrada de comandos.

#### `TableroBackgammon` (pygame_ui/pygameUI.py)
**Responsabilidades**: Renderizado gráfico, detección de clics, visualización de estado.

**Por qué se separaron**:
- **SRP**: Cada interfaz tiene una única responsabilidad de presentación
- **OCP**: Nuevas interfaces pueden agregarse sin modificar lógica existente
- **DIP (Dependency Inversion)**: Ambas dependen de abstracciones (`BackgammonGame`)

## 3. Justificación de Atributos

### 3.1 Clase `Player`

| Atributo | Tipo | Justificación |
|----------|------|---------------|
| `__name` | `str` | Identifica al jugador. Es inmutable durante el juego. |
| `__color` | `str` | Determina dirección de movimiento y zona de home board. Solo "white" o "black". |
| `__checkers_count` | `int` | Contador de fichas en el tablero. Útil para verificación de estado. |
| `__checkers_on_bar` | `int` | Necesario para determinar si el jugador debe reingresar fichas. |
| `__checkers_off_board` | `int` | Permite verificar condición de victoria (15 fichas fuera = ganar). |
| `__winner` | `bool` | Estado explícito del ganador. Facilita consultas sobre resultado. |
| `__can_move` | `bool` | Permite deshabilitar movimientos en situaciones especiales. |
| `__can_bear_off` | `bool` | Indica si todas las fichas están en home board (condición para bear off). |

**Decisión de diseño**: Se usan contadores en lugar de referencias directas a fichas para simplificar la gestión de estado y mejorar performance.

### 3.2 Clase `Checker`

| Atributo | Tipo | Justificación |
|----------|------|---------------|
| `__owner` | `Player` | Establece propiedad de la ficha. Inmutable durante el juego. |
| `__position` | `Optional[int]` | Posición actual (0-23) o `None` si no está en tablero. |
| `__on_bar` | `bool` | Estado mutuamente excluyente con `__position` y `__off_board`. |
| `__off_board` | `bool` | Indica si la ficha fue retirada (bear off). |

**Decisión de diseño**: Los tres estados (`position`, `on_bar`, `off_board`) son mutuamente excluyentes para garantizar consistencia. Se usa `Optional[int]` para `position` porque puede no estar en el tablero.

### 3.3 Clase `Board`

| Atributo | Tipo | Justificación |
|----------|------|---------------|
| `points` | `List[List[Checker]]` | Array de 24 listas. Cada punto puede tener múltiples fichas. Permite acceso O(1) por índice. |
| `bar` | `Dict[str, List[Checker]]` | Diccionario por color ("white"/"black"). Separa fichas capturadas por jugador. |
| `bear_off` | `Dict[str, List[Checker]]` | Similar a `bar`. Permite verificar condición de victoria. |

**Decisión de diseño**: 
- `points` como lista permite acceso directo por índice (punto 0-23)
- `bar` y `bear_off` como diccionarios por color simplifican búsquedas y mantienen separación lógica
- Listas de `Checker` permiten múltiples fichas en un punto

### 3.4 Clase `Dice`

| Atributo | Tipo | Justificación |
|----------|------|---------------|
| `__sides` | `int` | Configurable (por defecto 6). Permite extensibilidad a otros juegos. |
| `__last_roll` | `Tuple[int, int]` | Almacena último lanzamiento para consultas. Tupla inmutable garantiza integridad. |

**Decisión de diseño**: Tupla inmutable evita modificación accidental del último lanzamiento.

### 3.5 Clase `BackgammonGame`

| Atributo | Tipo | Justificación |
|----------|------|---------------|
| `__player1`, `__player2` | `Player` | Referencias a jugadores. Permiten acceso a estado sin crear nuevos objetos. |
| `__board` | `Board` | Estado del tablero. Único objeto que gestiona todas las posiciones. |
| `__dice` | `Dice` | Gestor de lanzamientos. Permite control sobre aleatoriedad en tests. |
| `__current_player` | `Player` | Jugador activo. Facilita determinar de quién es el turno. |
| `__started`, `__finished` | `bool` | Estados del juego. Permiten validar operaciones solo en estados válidos. |
| `__winner` | `Optional[Player]` | Ganador del juego. `None` mientras el juego está en curso. |
| `__last_dice_roll` | `Optional[tuple]` | Último lanzamiento. `None` si aún no se han lanzado dados. |
| `__dice_rolled` | `bool` | Flag que indica si se lanzaron dados. Previene movimientos sin lanzar dados. |
| `__player1_checkers`, `__player2_checkers` | `List[Checker]` | Referencias a todas las fichas. Permiten actualizar estado de fichas individuales. |
| `__move_history` | `List[Any]` | Historial de movimientos. Facilita undo y análisis de juego. |
| `__match_score` | `Dict[Player, int]` | Puntaje en partidos. Extensibilidad para torneos. |
| `__double_offered`, `__doubling_cube_value`, `__doubling_cube_owner` | Varios | Funcionalidad avanzada de doblaje (implementada pero no usada en versión básica). |

**Decisión de diseño**: Atributos separados para `started`, `finished`, y `dice_rolled` permiten validaciones específicas y claras en cada método.

## 4. Decisiones de Diseño Relevantes

### 4.1 Encapsulación Estricta con Atributos Privados

**Decisión**: Todos los atributos de estado son privados (`__atributo`) y solo accesibles mediante getters/setters.

**Justificación**:
- **Protección de invariantes**: Los setters validan datos antes de asignar
- **Control de acceso**: Previene modificaciones accidentales del estado
- **Flexibilidad futura**: Permite cambiar implementación interna sin afectar código cliente
- **Documentación implícita**: Los métodos públicos definen la interfaz de la clase

**Ejemplo**: En `Player`, `__checkers_count` solo puede modificarse mediante `set_checkers_count()`, que valida que esté entre 0 y 15.

### 4.2 Representación del Tablero como Array de Listas

**Decisión**: `points: List[List[Checker]]` donde cada índice (0-23) representa un punto del tablero.

**Justificación**:
- **Acceso directo**: O(1) para acceder a cualquier punto
- **Simplicidad**: Índice directo corresponde a punto del tablero
- **Flexibilidad**: Cada punto puede tener múltiples fichas (lista)
- **Compatibilidad**: Fácil mapear a representación visual

**Alternativas consideradas**:
- Diccionario: Más complejo sin beneficios claros
- Array unidimensional: No permite múltiples fichas por punto

### 4.3 Separación entre Estado de Player y Estado de Checker

**Decisión**: `Player` mantiene contadores, mientras que `Checker` mantiene posición individual.

**Justificación**:
- **Dualidad del modelo**: Player es agregado, Checker es entidad
- **Coherencia**: Player puede consultar estado sin recorrer todas las fichas
- **Flexibilidad**: Checkers pueden moverse independientemente
- **Performance**: Evita recorrer todas las fichas para consultas simples

### 4.4 Uso de Type Hints

**Decisión**: Todos los métodos y atributos tienen anotaciones de tipo.

**Justificación**:
- **Documentación**: Los tipos son documentación ejecutable
- **Validación temprana**: Herramientas (mypy) detectan errores antes de ejecución
- **IDE support**: Autocompletado y verificación en tiempo de desarrollo
- **Mantenibilidad**: Facilita entender el código para otros desarrolladores

### 4.5 Validación en Setters y Constructores

**Decisión**: Validación exhaustiva en constructores y setters, lanzando `ValueError` para datos inválidos.

**Justificación**:
- **Fail-fast**: Errores se detectan inmediatamente, no más tarde
- **Consistencia**: Garantiza que el objeto siempre está en estado válido
- **Claridad**: Mensajes de error específicos ayudan al debugging
- **Robustez**: Previene estados inválidos que causarían errores más tarde

## 5. Excepciones y Manejo de Errores

### 5.1 Excepciones Definidas

Se utiliza exclusivamente `ValueError` para errores de validación. Esta decisión se justifica porque:

- **Consistencia**: Todos los errores de validación son del mismo tipo
- **Estándar Python**: `ValueError` es la excepción apropiada para valores inválidos
- **Simplicidad**: No requiere jerarquía de excepciones personalizadas
- **Claridad**: El mensaje de error describe el problema específico

### 5.2 Excepciones por Clase

#### `Player`
```python
ValueError("El nombre no puede estar vacío")        # Constructor, set_name()
ValueError("Color inválido")                        # Constructor, set_color()
ValueError("Cantidad de fichas inválida")           # set_checkers_count()
ValueError("Cantidad de fichas en la barra inválida")  # set_checkers_on_bar()
ValueError("Cantidad de fichas fuera del tablero inválida")  # set_checkers_off_board()
ValueError("No hay fichas en la barra para remover")  # remove_checker_from_bar()
```

**Justificación**: Todas las excepciones en `Player` validan estado del jugador. Mensajes específicos facilitan debugging.

#### `Checker`
```python
ValueError("El propietario no puede ser None")      # Constructor, set_owner()
ValueError("Posición inválida")                     # set_position()
ValueError("La ficha no está en el tablero")        # hit_by_opponent(), is_moving_forward()
```

**Justificación**: Validaciones previenen estados inconsistentes (ficha sin propietario, posición fuera de rango, operaciones inválidas).

#### `Board`
```python
ValueError("Punto inválido")                        # get_checkers_count_on_point()
ValueError("No hay fichas para remover")            # remove_checker_from_point()
ValueError("No se puede golpear blot")              # hit_blot()
ValueError("No hay fichas en la barra")             # remove_checker_from_bar()
```

**Justificación**: Validaciones garantizan que operaciones solo se ejecuten en estados válidos del tablero.

#### `BackgammonGame`
```python
ValueError("Los nombres de los jugadores no pueden estar vacíos")  # Constructor
ValueError("Los nombres de los jugadores deben ser distintos")      # Constructor
ValueError("Jugador inválido")                                     # set_current_player(), set_winner()
ValueError("El juego ha finalizado")                               # roll_dice(), make_move()
ValueError("El juego no ha comenzado")                             # make_move(), make_move_from_bar()
ValueError("Debes lanzar los dados primero")                       # make_move(), make_move_from_bar()
ValueError("El puntaje no puede ser negativo")                     # set_match_score()
ValueError("Ya se ha ofrecido el doble")                          # offer_double()
ValueError("No se ha ofrecido el doble")                           # accept_double(), decline_double()
ValueError("Estado inválido")                                      # load_game_state()
```

**Justificación**: Validaciones de estado previenen operaciones fuera de secuencia o en estados inválidos.

### 5.3 Estrategia de Manejo de Errores

**Principios aplicados**:
1. **Validación temprana**: Errores se detectan al ingresar datos inválidos
2. **Mensajes descriptivos**: Cada excepción tiene mensaje que explica el problema
3. **Sin recuperación automática**: Las excepciones se propagan para que la capa superior decida cómo manejarlas
4. **No silenciar errores**: No se capturan excepciones sin manejo explícito

**En la capa de presentación**:
- **CLI**: Captura `ValueError` y muestra mensaje al usuario, permite reintentar
- **Pygame UI**: Captura excepciones y muestra mensajes visuales o registra en consola
- **Errores críticos**: `SystemExit` para interrupciones del usuario (Ctrl+C, EOF)

**Ejemplo de manejo en CLI**:
```python
try:
    self._game_.make_move(from_point, to_point)
except ValueError as e:
    print(f"Error: {e}")
    # Permite al usuario intentar nuevamente
```

## 6. Estrategias de Testing y Cobertura

### 6.1 Metodología: Test-Driven Development (TDD)

**Enfoque**: Tests escritos antes de la implementación, siguiendo el ciclo Red-Green-Refactor.

**Evidencia**: 
- Tests iniciales en rojo (ver `prompts/prompts_testing.md`)
- Implementación mínima para pasar tests
- Refactorización manteniendo tests en verde

### 6.2 Estrategias de Testing Implementadas

#### 6.2.1 Tests Unitarios

**Objetivo**: Probar clases individuales en aislamiento.

**Ejemplos**:
- `test_player.py`: 40+ tests cubriendo todos los métodos de `Player`
- `test_dice.py`: Tests con mocks para controlar aleatoriedad
- `test_checker.py`: Tests de estado y transiciones
- `test_board.py`: Tests de operaciones sobre el tablero

**Cobertura alcanzada**: >90% en módulo `core/`

#### 6.2.2 Tests de Integración

**Objetivo**: Probar interacción entre múltiples clases.

**Ejemplos**:
- `test_backgammongame.py`: Tests de flujo completo del juego
  - Secuencias de movimientos
  - Interacción Player-Board-Checker
  - Validación de reglas de juego

#### 6.2.3 Tests de Casos Límite (Edge Cases)

**Objetivo**: Probar comportamientos en situaciones extremas.

**Ejemplos implementados**:
- Bear off con dado exacto vs. dado mayor
- Movimientos desde barra cuando puntos están bloqueados
- Validación de movimientos inválidos
- Estados del juego (no iniciado, finalizado)
- Dobles de dados (4 movimientos)

#### 6.2.4 Tests con Mocks

**Objetivo**: Controlar dependencias externas (aleatoriedad, entrada del usuario).

**Ejemplos**:
- `test_dice.py`: Mock de `random.randint` para resultados determinísticos
- `test_cli.py`: Mock de `input()` y `print()` para probar interacción

### 6.3 Cobertura de Código

**Herramienta**: `coverage.py`

**Métricas alcanzadas**:
- **Módulo `core/`**: >90% de cobertura
- **Líneas cubiertas**: Todas las rutas críticas de ejecución
- **Ramas**: Decisiones condicionales probadas

**Estrategia para aumentar cobertura**:
1. Identificación de líneas no cubiertas con `coverage report`
2. Adición de tests específicos para casos faltantes
3. Verificación de cobertura después de cada iteración

**Casos específicos agregados para cobertura**:
- Setters de `Dice` y `Player` con validaciones
- Casos de bear off (exacto, mayor, ficha más atrasada)
- Reingreso desde barra (captura, bloqueado, inválido)
- Validaciones internas de movimientos
- Métodos de consulta (`get_player2_checkers`, `get_pip_count`)

### 6.4 Tipos de Tests por Funcionalidad

| Funcionalidad | Tests Implementados | Justificación |
|---------------|---------------------|---------------|
| Creación de objetos | Tests de constructores con validación | Garantiza objetos en estado válido |
| Setters con validación | Tests de límites y valores inválidos | Asegura protección de invariantes |
| Operaciones de Board | Tests de agregar/remover fichas | Verifica integridad del tablero |
| Movimientos | Tests de validación y ejecución | Asegura cumplimiento de reglas |
| Bear off | Tests de múltiples escenarios | Funcionalidad compleja requiere cobertura exhaustiva |
| Captura de fichas | Tests de hit blot | Regla crítica del juego |
| Condición de victoria | Tests de finalización | Funcionalidad central |
| Estado del juego | Tests de transiciones de estado | Previene operaciones inválidas |

## 7. Referencias a Requisitos SOLID y Cómo se Cumplen

### 7.1 Single Responsibility Principle (SRP)

**Principio**: Una clase debe tener una sola razón para cambiar.

**Cumplimiento**:

- **`Player`**: Solo gestiona información y estado de un jugador
  - **Razón de cambio única**: Cambios en representación de jugadores
  
- **`Checker`**: Solo gestiona estado de una ficha individual
  - **Razón de cambio única**: Cambios en representación de fichas
  
- **`Board`**: Solo gestiona estado físico del tablero
  - **Razón de cambio única**: Cambios en estructura del tablero
  
- **`Dice`**: Solo gestiona lanzamiento y análisis de dados
  - **Razón de cambio única**: Cambios en lógica de dados
  
- **`BackgammonGame`**: Coordina el juego (múltiples responsabilidades, pero cohesivas)
  - **Nota**: Esta clase tiene más responsabilidades, pero todas relacionadas con orquestación del juego

**Violaciones evitadas**:
- `Player` no conoce reglas del juego
- `Checker` no gestiona el tablero
- `Board` no ejecuta movimientos (solo gestiona estado)

### 7.2 Open/Closed Principle (OCP)

**Principio**: Las clases deben estar abiertas para extensión pero cerradas para modificación.

**Cumplimiento**:

- **Extensibilidad sin modificación**:
  - Nuevos tipos de validación pueden agregarse a `Board` mediante nuevos métodos sin modificar existentes
  - `Dice` puede extenderse con nuevos tipos de lanzamiento sin modificar `roll()`
  - `BackgammonGame` puede agregar nuevas reglas mediante métodos adicionales

- **Ejemplo concreto**:
  ```python
  # Se pueden agregar métodos nuevos sin modificar existentes
  class Board:
      def can_place_checker(self, ...):  # Método existente
          ...
      
      def get_moves_to_bear_off(self, ...):  # Nuevo método, no modifica existentes
          ...
  ```

**Limitaciones**:
- Algunos métodos internos requieren modificación para nuevas funcionalidades
- Compromiso aceptable entre OCP y simplicidad

### 7.3 Liskov Substitution Principle (LSP)

**Principio**: Los objetos de una superclase deben ser reemplazables por instancias de sus subclases.

**Cumplimiento**:

- **Aunque no hay herencia explícita**, el principio se aplica mediante:
  - Uso de `Player` como tipo en múltiples contextos (ambos jugadores son intercambiables)
  - `Checker` objects son intercambiables independientemente de su `owner`
  - Métodos que reciben `Player` funcionan con cualquier instancia

**Ejemplo**:
```python
def can_bear_off(self, player: Player) -> bool:
    # Funciona igual para player1 o player2
    # No requiere conocimiento de qué jugador específico es
```

### 7.4 Interface Segregation Principle (ISP)

**Principio**: Los clientes no deben depender de interfaces que no usan.

**Cumplimiento**:

- **Interfaces pequeñas y específicas**:
  - `Player` expone solo métodos necesarios para cada contexto
  - `Checker` tiene métodos específicos para cada operación
  - No hay interfaces "gordas" con muchos métodos no utilizados

- **Separación de interfaces de presentación**:
  - `CLIInterface` solo usa métodos públicos de `BackgammonGame`
  - `TableroBackgammon` solo usa métodos públicos de `BackgammonGame`
  - Ninguna interfaz depende de métodos internos que no necesita

**Ejemplo**:
```python
# CLI solo usa métodos públicos necesarios
class CLIInterface:
    def _display_board_(self):
        board = self._game_.get_board()  # Solo getter, no setter directo
        current = self._game_.get_current_player()  # Solo consulta
```

### 7.5 Dependency Inversion Principle (DIP)

**Principio**: Depender de abstracciones, no de concreciones.

**Cumplimiento**:

- **`BackgammonGame` depende de abstracciones**:
  ```python
  def __init__(self, player1_name: str, player2_name: str):
      # Crea instancias, pero depende de interfaces (métodos públicos)
      self.__player1 = Player(...)  # Depende de interfaz Player
      self.__board = Board()        # Depende de interfaz Board
      self.__dice = Dice()          # Depende de interfaz Dice
  ```

- **Interfaces dependen de abstracción `BackgammonGame`**:
  - `CLIInterface` recibe `BackgammonGame` (no implementación concreta)
  - `TableroBackgammon` usa métodos públicos de `BackgammonGame`
  - Pueden intercambiarse implementaciones de `BackgammonGame` sin afectar interfaces

**Limitaciones**:
- Algunas dependencias son concretas (no hay interfaces explícitas)
- En Python, esto es aceptable debido a duck typing
- La estructura permite fácil extracción de interfaces si es necesario

### 7.6 Resumen de Cumplimiento SOLID

| Principio | Cumplimiento | Ejemplo |
|-----------|--------------|---------|
| **SRP** | ✅ Alto | Cada clase tiene responsabilidad única y bien definida |
| **OCP** | ✅ Medio | Extensible mediante nuevos métodos, pero requiere modificación para algunas funcionalidades |
| **LSP** | ✅ Alto | Objetos del mismo tipo son intercambiables |
| **ISP** | ✅ Alto | Interfaces pequeñas y específicas |
| **DIP** | ✅ Medio | Dependencias de abstracciones implícitas (duck typing de Python) |

**Conclusión**: El diseño cumple sólidamente con los principios SOLID, con algunas limitaciones menores aceptables en el contexto de Python y la complejidad del proyecto.

## 8. Anexos: Diagramas UML

### 8.1 Diagrama de Clases

```
┌─────────────────────────────────────────────────────────────┐
│                      BackgammonGame                         │
├─────────────────────────────────────────────────────────────┤
│ - __player1: Player                                         │
│ - __player2: Player                                         │
│ - __board: Board                                            │
│ - __dice: Dice                                              │
│ - __current_player: Player                                  │
│ - __started: bool                                           │
│ - __finished: bool                                          │
│ - __winner: Optional[Player]                                │
│ - __last_dice_roll: Optional[tuple]                        │
│ - __dice_rolled: bool                                       │
│ - __player1_checkers: List[Checker]                        │
│ - __player2_checkers: List[Checker]                         │
│ - __move_history: List[Any]                                 │
├─────────────────────────────────────────────────────────────┤
│ + get_player1() → Player                                    │
│ + get_player2() → Player                                    │
│ + get_board() → Board                                       │
│ + get_dice() → Dice                                         │
│ + start_game() → None                                       │
│ + roll_dice() → tuple                                       │
│ + is_valid_move(from: int, to: int) → bool                 │
│ + make_move(from: int, to: int) → None                     │
│ + make_move_from_bar(to: int) → None                       │
│ + is_finished() → bool                                      │
│ + get_winner() → Optional[Player]                           │
│ + get_available_moves() → List[Any]                        │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         │                    │                    │
         │                    │                    │
    ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
    │ Player  │          │  Board  │          │  Dice   │
    ├─────────┤          ├─────────┤          ├─────────┤
    │ -__name │          │ points │          │ -__sides│
    │ -__color│          │ bar    │          │ -__last │
    │ -__check│          │ bear_  │          │   _roll │
    │   ers_  │          │   off   │          │         │
    │   count │          │         │          │         │
    ├─────────┤          ├─────────┤          ├─────────┤
    │ +get_   │          │ +setup │          │ +roll() │
    │  name() │          │   _init│          │ +is_    │
    │ +get_   │          │   ial_ │          │  double │
    │  color()│          │   _pos │          │  ()     │
    │ +get_   │          │  ition│          │ +get_   │
    │  check  │          │ ()    │          │  moves()│
    │  ers_   │          │ +add_  │          │         │
    │  count()│          │  check │          │         │
    │ +set_   │          │  er_to │          │         │
    │  check  │          │  _point│          │         │
    │  ers_   │          │ ()    │          │         │
    │  count()│          │ +remove│          │         │
    └─────────┘          │   _    │          └─────────┘
                         │  check │
                         │  er_   │
                         │  from_ │
                         │  point │
                         │ ()    │
                         │ +can_  │
                         │  bear_ │
                         │  off() │
                         │ +has_  │
                         │  check │
                         │  ers_  │
                         │  on_   │
                         │  bar() │
                         └────────┘
                               │
                               │
                         ┌─────▼─────┐
                         │  Checker  │
                         ├───────────┤
                         │ -__owner  │
                         │ -__       │
                         │  position │
                         │ -__on_bar │
                         │ -__off_   │
                         │  board    │
                         ├───────────┤
                         │ +get_     │
                         │  owner()  │
                         │ +get_     │
                         │  color()  │
                         │ +get_     │
                         │  position │
                         │ ()        │
                         │ +set_     │
                         │  position │
                         │ ()        │
                         │ +move_to_ │
                         │  bar()    │
                         │ +move_    │
                         │  off_     │
                         │  board()  │
                         │ +is_in_   │
                         │  home_    │
                         │  board()  │
                         └───────────┘
```

### 8.2 Relaciones entre Clases

**Agregación**:
- `BackgammonGame` **tiene** `Player`, `Board`, `Dice` (agregación)
- `BackgammonGame` **tiene** múltiples `Checker` (agregación)
- `Board` **contiene** múltiples `Checker` en puntos (agregación)

**Composición**:
- `Checker` **tiene** referencia a `Player` (composición débil)
- `Board` **tiene** `points`, `bar`, `bear_off` (composición)

**Dependencia**:
- `CLIInterface` **depende** de `BackgammonGame`
- `TableroBackgammon` **depende** de `BackgammonGame`
- `BackgammonGame` **usa** métodos de `Player`, `Board`, `Dice`, `Checker`

---

**Fecha de elaboración**: Noviembre 2025  
**Versión**: 1.0  
**Estado**: Completo y funcional
