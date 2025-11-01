# Changelog
Formato basado en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] – 2025-11-01

### Added
- Se implementó bear off (retirar fichas) en la lógica del juego
- Se agregó visualización de fichas retiradas y conteo en la zona lateral
- Se ajustó el mapeo de puntos a columnas en la UI para alinear fichas correctamente
- Se actualizó la UI para saltar el turno solo si el jugador tiene fichas en barra y no existen reingresos válidos con los dados
- Se resolvió TabError por mezcla de tabs/espacios en `pygame_ui/pygameUI.py`
- Se corrigió la lógica de dobles: cuando sale un doble (ej: 2,2), ahora se guarda como (2,2,2,2) permitiendo 4 movimientos del mismo valor según las reglas del Backgammon
- Se actualizó la visualización de dados en la UI para mostrar correctamente los 4 movimientos disponibles en dobles
- Se corrigió el consumo de movimientos en dobles para que cada movimiento reste un valor de la tupla hasta agotar los 4 movimientos
- Se implementó condición de victoria: el jugador gana cuando completa el bear off de todas sus fichas (15 fichas)
- Se agregó mensaje de victoria en la UI que se muestra cuando un jugador gana el juego
- Se implementó límite visual de 6 fichas apiladas con indicador numérico cuando hay más fichas
- Se mejoró la visualización del conteo de bear off con fondos y bordes para mejor legibilidad
- Se ajustó el botón "Tirar Dado" para que tenga mejor tamaño y legibilidad
- Se agregaron nuevos tests para aumentar la cobertura del código al 90%+ en el módulo `core/`
- Se implementaron tests adicionales para cubrir casos edge de bear off, reingreso desde barra y validaciones de movimientos

### Fixed
- Se corrigió la lógica de bear off para fichas blancas: ahora incluye correctamente el punto 24 en el home board
- Se corrigió el rango del home board de blancas de `range(18, 23)` a `range(18, 24)` en múltiples archivos
- Se corrigió la validación de movimientos desde punto 24 para bear off de fichas blancas
- Se corrigió el uso de claves de diccionario en métodos de `Board` para usar `player.get_color()` en lugar de objetos `Player`
- Se eliminaron variables no usadas (`boton_y_bottom`) en la UI
- Se corrigieron todas las excepciones genéricas `Exception` en `cli/cli.py` para usar excepciones más específicas
- Se corrigió el nombre de variable `bar` a `bar_checkers` en `cli/cli.py` para cumplir con convenciones de nombres
- Se corrigieron variables con caracteres no ASCII (`tamaño_fuente` → `tamano_fuente`, `fuente_pequeña` → `fuente_pequena`)
- Se dividieron líneas largas (más de 100 caracteres) en múltiples archivos para cumplir con PEP 8
- Se eliminó todo el trailing whitespace en todos los archivos del proyecto
- Se corrigieron argumentos no usados agregando `# pylint: disable=unused-argument` donde es apropiado
- Se agregaron comentarios de pylint para deshabilitar warnings apropiados (`disallowed-name`, `import-outside-toplevel`)
- Se corrigieron imports condicionales en `main.py` con comentarios apropiados de pylint

### Changed
- Se mejoró la organización visual de la UI para evitar superposiciones entre elementos
- Se ajustó el posicionamiento del mensaje de victoria para no tapar otros elementos de la UI
- Se estandarizó el estilo visual de contadores y botones para mantener consistencia

## [Sprint 5] – 2025-10-30

### Added
- Se implementó cambio automático de jugadores después de completar movimientos
- Se agregó seguimiento de movimientos restantes en el CLI
- Se implementa estructura de pygame con errores
- Se implementó sistema completo de captura de fichas en Backgammon
- Se agregó visualización de fichas en la barra central
- Se implementó reingreso obligatorio desde la barra
- Se agregó validación de movimientos válidos desde la barra
- Se implementó indicación visual de fichas seleccionadas (círculo dorado)
- Se agregó visualización de movimientos válidos con círculos verdes
- Se corrigió posicionamiento de fichas cerca de la barra central
- Se implementó lógica de captura según reglas del Backgammon
- Se agregó sistema de selección en dos pasos para fichas en la barra
- Se corrigieron errores de indentación en pygameUI.py
- Se solucionó problema de posicionamiento de círculos verdes en movimientos válidos
- Se corrigió lógica de reingreso desde la barra para fichas blancas y negras
- Se arregló validación de movimientos desde la barra según reglas del Backgammon

## [Sprint 4] – 2025-10-15

### Added
- Se crearon los tests completos para el CLI en `tests/test_cli.py`, siguiendo SOLID, TDD, PEP 8, PEP 257 y PEP 484.
- Se implementó una visualización completa del tablero de Backgammon en formato ASCII
- Se agregó manejo automático de inicialización del juego en el CLI
- Se mejoró el manejo de entrada de datos del usuario con validaciones robustas
- Se solucionó el error "El juego no ha comenzado" agregando inicialización automática
- Se corrigió el error "No hay fichas en el punto de origen" mejorando el manejo de entrada
- Se mejoró la visualización del tablero para mostrar correctamente las fichas en la barra
- Se optimizó el método `start_game()` para no resetear el tablero innecesariamente
- Se mejoró la interfaz CLI con mensajes informativos más claros
- Se actualizó la visualización del tablero para mostrar fichas en la barra y fuera del tablero
- Se mejoró el manejo de errores en los comandos del CLI

## [Sprint 3] – 2025-10-01

### Added
- Se agregó la importación de la clase `Checker` en `core/backgammongame.py`.
- Se crearon listas de fichas para cada jugador y método para inicializar la posición de las fichas usando objetos `Checker`.
- Se corrigió el archivo `core/backgammongame.py` para cumplir con PEP8, PEP257, PEP484 y obtener lo más cercano a 10/10 en pylint.
- Se corrigió el archivo `core/board.py` para cumplir con PEP8, PEP257, PEP484 y obtener lo más cercano a 10/10 en pylint.
- Se corrigió el archivo `core/checker.py` para cumplir con PEP8, PEP257, PEP484 y obtener lo más cercano a 10/10 en pylint.
- Se corrigió el archivo `core/dice.py` para cumplir con PEP8, PEP257, PEP484 y obtener lo más cercano a 10/10 en pylint.
- Se corrigió el archivo `core/player.py` para cumplir con PEP8, PEP257, PEP484 y obtener lo más cercano a 10/10 en pylint.
- Se creó un esqueleto de CLI en `cli/cli.py` para Backgammon, con renderizado básico de tablero y preparado para futuras extensiones.


## [Sprint 2] – 2025-09-17

### Added
- Implementación de la clase `Player` en `core/player.py` con atributos privados, getters y setters.
- Tests unitarios completos para la clase `Player`.
- Documentación de prompts y respuestas en `prompts/prompts_testing.md`.
- Tests uniarios completos para la clase `Board` (en rojo).
- Implementación de la clase `Board` con errores por la falta de clase Checker.
- Implementación de tests unitarios para clase checker y backgammongame (en rojo).
- Implementación de clase checker.
- Implementación de clase Backgammongame.
- Se agregó mock en tests de Dice.


## [Sprint 1] – 2025-09-03

### Added
- Estructura inicial de carpetas (`core/`, `cli/`, `pygame_ui/`, `assets/`, `tests/`, `prompts/`).
- Archivos base: `.gitignore`, `README.md`, `CHANGELOG.md`, `JUSTIFICACION.md`, `requirements.txt`.
- Archivos de prompts (`prompts-desarrollo.md`, `prompts-testing.md`, `prompts-documentacion.md`).
- Configuración de entorno virtual (`venv/`) y agregado al `.gitignore`.
- Configuración inicial de **coverage** con `.coveragerc`.
- Dependencias iniciales: `pytest`, `coverage`, `pytest-cov`.
- Test de ejemplo (`tests/test_sample.py`) para validar setup. 
- Documentación en `README.md` con pasos de entorno, testing y coverage.
- Implementación inicial de clase `Dice` según TDD.
- Tests iniciales para `Dice`.

