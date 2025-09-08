# Changelog
Formato basado en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Implementación de la clase `Player` en `core/player.py` con atributos privados, getters y setters.
- Tests unitarios completos para la clase `Player`.
- Documentación de prompts y respuestas en `prompts/prompts_testing.md`.
- Tests uniarios completos para la clase `Board` (en rojo).
- Implementación de la clase `Board` con errores por la falta de clase Checker.


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

