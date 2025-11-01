# Backgammon en Python – Computación 2025

---

## Alumno

- **Nombre:** Constanza Baigorria - 64237
- **Carrera:** Ingeniería en Informática  
- **Universidad:** Universidad de Mendoza
- **Materia:** Computación 

---

## Descripción

Este proyecto implementa el juego **Backgammon** completo en **Python**, siguiendo las consignas de la materia *Computación 2025*. El desarrollo contempla tanto una **interfaz de línea de comandos (CLI)** como una **interfaz gráfica basada en Pygame**, manteniendo la lógica de juego completamente desacoplada de la presentación.

### Características Principales

- Implementación completa de las reglas oficiales de Backgammon
- Sistema de captura de fichas
- Bear off (retiro de fichas)
- Condición de victoria automática
- Manejo de dobles en dados
- Reingreso desde la barra
- Dos interfaces de usuario (CLI y Pygame)
- Suite completa de tests unitarios (>90% cobertura)
- Código siguiendo principios SOLID

---

## Requisitos

### Requisitos del Sistema

- **Python 3.10 o superior**
- **pip** 
- **Git** 

### Dependencias del Proyecto

Las siguientes dependencias se instalan automáticamente (ver sección de instalación):

- `pygame==2.6.1` - Para la interfaz gráfica
- `coverage==7.10.5` - Para medir cobertura de código en tests
- `pylint>=3.0.0` - Para análisis estático de código

---

## Instalación y Configuración

### Paso 1: Clonar o Descargar el Repositorio

**Opción A: Clonar con Git** (si tienes acceso al repositorio)
```bash
git clone <url-del-repositorio>
cd computacion-2025-backgammon-constanzabaigorria
```

### Paso 2: Crear y Activar el Entorno Virtual

Se recomienda **fuertemente** usar un entorno virtual para aislar las dependencias del proyecto:

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Mac/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

Con el entorno virtual activado, instala todas las dependencias:

```bash
pip install -r requirements.txt
```

Esto instalará automáticamente:
- `pygame==2.6.1` - Librería para interfaz gráfica
- `coverage==7.10.5` - Herramienta para medir cobertura de tests
- `pylint>=3.0.0` - Analizador estático de código Python

**Verificación**: Para verificar que todo se instaló correctamente:
```bash
pip list
```

---

## Ejecutar tests
```bash
python -m unittest discover tests/ -v
```

## Medir Cobertura de Código
```bash
coverage run -m unittest discover 
coverage report -m
```

**Cobertura esperada**: El módulo `core/` debe tener **más del 90% de cobertura**.

### Ejecutar Análisis de Calidad con Pylint
```bash
pylint core/ cli/ pygame_ui/ main.py
```

---

## Modo Juego - Puesta en Funcionamiento

El juego puede ejecutarse en dos modos: **CLI (Línea de Comandos)** o **Pygame UI (Interfaz Gráfica)**.

### Método Recomendado: Usar main.py

El archivo `main.py` es el punto de entrada principal y presenta un menú interactivo:

```bash
python main.py
```

Esto mostrará un menú como el siguiente:

```
============================================================

 BACKGAMMON

Elige una interfaz:
  1. CLI (Línea de comandos)
  2. Pygame UI (Interfaz gráfica)

Ingresa tu elección (1 o 2):
```

**Opciones**:
- Ingresa `1` para iniciar el modo **CLI (Línea de Comandos)**
- Ingresa `2` para iniciar el modo **Pygame UI (Interfaz Gráfica)**

---

## Cómo jugar 

### Modo CLI (Línea de Comandos)

Una vez iniciado el juego en modo CLI, podrás interactuar mediante comandos de texto:

#### Comandos Disponibles

1. **Lanzar dados**
   ```
   roll
   ```
   o simplemente:
   ```
   r
   ```
   Lanza los dados y muestra el resultado.

2. **Hacer un movimiento**
   ```
   move <desde> <hasta>
   ```
   Donde:
   - `<desde>`: Punto de origen (número del 0 al 23) o `bar` si la ficha está en la barra
   - `<hasta>`: Punto destino (número del 0 al 23) o `bear` para hacer bear off
   
   **Ejemplos**:
   ```
   move 0 5        # Mueve una ficha del punto 0 al punto 5
   move bar 5      # Reingresa una ficha desde la barra al punto 5
   move 23 bear    # Retira una ficha del punto 23 (bear off)
   ```

3. **Salir del juego**
   ```
   quit
   ```
   o:
   ```
   q
   ```

#### Flujo de Juego Típico

1. Lanza los dados con `roll`
2. Haz tus movimientos con `move <desde> <hasta>`
3. Si tienes fichas en la barra, primero debes reingresarlas con `move bar <punto>`
4. Cuando todas tus fichas estén en home board, puedes hacer bear off con `move <punto> bear`
5. El juego termina automáticamente cuando un jugador retira 15 fichas

### Modo Pygame UI (Interfaz Gráfica)

Una vez iniciada la interfaz gráfica, verás el tablero de Backgammon y podrás interactuar con clics del mouse.

#### Controles

1. **Lanzar dados**
   - Haz clic en el botón **"Tirar Dado"** (ubicado en el panel lateral)
   - Los dados aparecerán mostrando los valores obtenidos

2. **Mover una ficha**
   - **Paso 1**: Haz clic en una ficha propia (del color de tu turno)
   - **Paso 2**: Los puntos válidos aparecerán marcados con círculos verdes
   - **Paso 3**: Haz clic en el punto destino deseado
   - La ficha se moverá automáticamente

3. **Reingresar desde la barra**
   - **Paso 1**: Haz clic en la barra central donde están tus fichas capturadas (se mostrará un indicador)
   - **Paso 2**: Aparecerán círculos verdes en los puntos válidos de reingreso
   - **Paso 3**: Haz clic en el punto donde quieres reingresar

4. **Bear off (retirar fichas)**
   - Asegúrate de que todas tus fichas estén en tu home board
   - Selecciona una ficha y haz clic en la zona de bear off (extremo del tablero del lado opuesto)
   - La ficha será retirada y se actualizará el contador

#### Información Visual

- **Panel superior**: Muestra el turno actual (BLANCAS o NEGRAS)
- **Panel lateral derecho**: 
  - Contador de fichas retiradas por cada jugador
  - Botón "Tirar Dado"
- **Barra central**: Muestra fichas capturadas (si las hay)
- **Círculos verdes**: Indican movimientos válidos disponibles

#### Fin del Juego

El juego termina automáticamente cuando un jugador retira 15 fichas. Aparecerá un mensaje de victoria indicando el ganador.

---

## Estructura del Proyecto

```
computacion-2025-backgammon-constanzabaigorria/
├── core/                          # Lógica de negocio del juego
│   ├── __init__.py
│   ├── backgammongame.py          # Clase principal que orquesta el juego
│   ├── board.py                   # Gestión del estado del tablero
│   ├── checker.py                 # Representación de fichas individuales
│   ├── dice.py                    # Gestión de lanzamiento de dados
│   └── player.py                  # Representación de jugadores
│
├── cli/                           # Interfaz de línea de comandos
│   ├── __init__.py
│   └── cli.py                     # CLIInterface - manejo de comandos
│
├── pygame_ui/                     # Interfaz gráfica
│   ├── __pycache__/
│   └── pygameUI.py                # TableroBackgammon - renderizado gráfico
│
├── tests/                         # Pruebas unitarias
│   ├── __init__.py
│   ├── test_backgammongame.py     # Tests de BackgammonGame
│   ├── test_board.py              # Tests de Board
│   ├── test_checker.py            # Tests de Checker
│   ├── test_cli.py                # Tests de CLI
│   ├── test_dice.py               # Tests de Dice
│   └── test_player.py             # Tests de Player
│
├── prompts/                       # Documentación de prompts utilizados
│   ├── prompts_desarrollo.md      # Prompts de desarrollo de código
│   ├── prompts_testing.md         # Prompts de creación de tests
│   └── prompts_documentacion.md   # Prompts de documentación
│
├── assets/                        # Recursos (imágenes, sonidos)
│
├── main.py                        # Punto de entrada principal
├── requirements.txt               # Dependencias del proyecto
├── README.md                      # Este archivo
├── CHANGELOG.md                   # Historial de cambios y funcionalidades
└── JUSTIFICACION.md               # Justificación del diseño (SOLID, UML, etc.)
```


