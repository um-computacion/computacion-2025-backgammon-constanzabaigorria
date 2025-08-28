# Backgammon en Python – Computación 2025 

---

## Alumno
- **Nombre:** Constanza Baigorria 
- **Carrera:** Ingeniería en Informática 
- **Materia:** Computación 2025  

---

## Descripción

Este proyecto implementa el juego **Backgammon** en **Python**, siguiendo las consignas de la materia *Computación 2025*.  
El desarrollo contempla tanto una **interfaz de línea de comandos (CLI)** como una **interfaz gráfica basada en Pygame**, manteniendo la lógica de juego desacoplada de la presentación.  

---

## Estado actual del proyecto

### Estructura de carpetas creada
- `core/` → lógica del juego.
- `cli/` → interfaz de consola.
- `pygame_ui/` → interfaz gráfica.
- `assets/` → imágenes y sonidos.
- `tests/` → pruebas unitarias.
- `prompts/` → almacenamiento de prompts usados.

Archivos base ya presentes:
- `.gitignore`
- `README.md`
- `CHANGELOG.md`
- `JUSTIFICACION.md`
- `requirements.txt`

### ✔️ Avances realizados
- Estructura de tests inicial (`tests/`).
- Prompts en curso (`prompts-desarrollo.md`, `prompts-testing.md`, `prompts-documentacion.md`).
- Configuración de entorno virtual.
- Configuración de coverage.
- Test de ejemplo para validar setup.

---

## 🐍 Entorno virtual

Para crear y activar el entorno virtual:

```bash
python3 -m venv venv  #según versión puede ser solo python sin el 3
source venv/bin/activate   # mac/linux

