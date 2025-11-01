## Prompt [1] 

**Fecha**: 27/08/2025
**Modelo/Herramienta**: ChatGPT (GPT-5) 
**Contexto**: creación de readme

## Prompt enviado

armame un readme que cumpla con los requisitos del archivo cargado en el que explique lo que se ha implementado. 

### Respuesta recibida
```
# Backgammon en Python – Computación 2025 🎲

---

## 👤 Alumno
- **Nombre:** Constanza Agustina Baigorria Montes  
- **Carrera:** Ingeniería (Universidad de Mendoza)  
- **Materia:** Computación 2025  

---

## 📖 Descripción

Este proyecto implementa el juego **Backgammon** en **Python**, siguiendo las consignas de la materia *Computación 2025*.  
El desarrollo contempla tanto una **interfaz de línea de comandos (CLI)** como una **interfaz gráfica basada en Pygame**, manteniendo la lógica de juego desacoplada de la presentación.  

---

## 📌 Estado actual del proyecto

### ✔️ Estructura de carpetas creada
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
- Clases base esqueleto: `Dice`, `Player`, `Board`, `Checker`, `BackgammonGame`.
- Estructura de tests inicial (`tests/`).
- Prompts en curso (`prompts-desarrollo.md`, `prompts-testing.md`, `prompts-documentacion.md`).
- Configuración de entorno virtual.
- Configuración de coverage.
- Test de ejemplo para validar setup.

---

## 🐍 Entorno virtual

Para crear y activar el entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
```

---

## Prompt [2] 

**Fecha**: 27-08-2025 
**Modelo/Herramienta**: Claude Sonnet 4  
**Contexto**: creación de estructura para prompts

## Prompt enviado

crea una estructura modelo para el archivo de prompts

### Respuesta recibida
```
## Prompt [NÚMERO] - [TÍTULO]

**Fecha**: YYYY-MM-DD  
**Modelo/Herramienta**: [Nombre y versión]  
**Contexto**: [Descripción del contexto de documentación]

### Prompt
```

## Prompt [3]

**Fecha**: 15-01-2025  
**Modelo/Herramienta**: Claude Sonnet 4  
**Contexto**: documentación de implementación de sistema de captura

## Prompt enviado

realiza la documentación de todos los prompts enviados y todos los cambios en cada archivo respetando el formato@CHANGELOG.md @prompts_desarrollo.md @prompts_documentacion.md

### Respuesta recibida

Se actualizó la documentación completa del proyecto:
- Se agregaron nuevos prompts al archivo `prompts_desarrollo.md`
- Se actualizó `CHANGELOG.md` con las funcionalidades implementadas
- Se documentaron todos los cambios realizados en el sistema de captura
- Se mantuvo el formato consistente en todos los archivos de documentación

### Uso de la respuesta

Se completó la documentación de todos los prompts y cambios realizados en el proyecto Backgammon.

## Prompt [4]

**Fecha**: 01-11-2025  
**Modelo/Herramienta**: Claude Sonnet 4  
**Contexto**: completar archivo JUSTIFICACION.md con todos los requisitos académicos

## Prompt enviado

comleta el archivo de @JUSTIFICACION.md con esto: 
Contenido mínimo:
Resumen del diseño general.
Justificación de las clases elegidas (por qué, responsabilidades).
Justificación de atributos (por qué se eligieron).
Decisiones de diseño relevantes
Excepciones y manejo de errores (qué excepciones definidas y por qué).
Estrategias de testing y cobertura (qué se probó y por qué).
Referencias a requisitos SOLID y cómo se cumplen.
Anexos: diagramas UML(ej: diagrama de clases).


### Respuesta recibida

Se completó el archivo `JUSTIFICACION.md` con todos los requisitos académicos especificados:
- **Resumen del diseño general**: Arquitectura modular por capas con diagrama y justificación
- **Justificación de las clases elegidas**: Análisis detallado de cada clase (Player, Checker, Board, Dice, BackgammonGame) incluyendo responsabilidades y razones de elección
- **Justificación de atributos**: Tablas completas con atributos, tipos y justificación de cada decisión de diseño
- **Decisiones de diseño relevantes**: Explicación de 5 decisiones clave (encapsulación, representación del tablero, separación de estado, type hints, validación)
- **Excepciones y manejo de errores**: Lista completa de todas las excepciones `ValueError` definidas en cada clase, con justificación y estrategias de manejo
- **Estrategias de testing y cobertura**: Metodología TDD, tipos de tests implementados, cobertura alcanzada (>90%), y tabla de funcionalidades probadas
- **Referencias a requisitos SOLID**: Análisis detallado de cada principio (SRP, OCP, LSP, ISP, DIP) con ejemplos de código y tabla de cumplimiento
- **Anexos con diagramas UML**: 
  - Diagrama de clases completo con todos los atributos y métodos
  - Relaciones entre clases (agregación, composición, dependencia)

El documento tiene más de 700 líneas y cumple completamente con los requisitos académicos para justificación de diseño.

### Uso de la respuesta

El archivo `JUSTIFICACION.md` ahora está completo y listo para presentación académica, documentando exhaustivamente el diseño del proyecto Backgammon siguiendo todos los estándares requeridos.

