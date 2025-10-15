# Changelog
Formato basado en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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

