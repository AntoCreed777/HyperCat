# 🎮 HyperCat - Ultimate TicTacToe

## 📖 Descripción

**HyperCat** es una implementación del juego **Ultimate TicTacToe**, una variante avanzada del clásico TicTacToe (Tres en Raya / Gato). El juego consiste en un tablero de 3x3 donde cada casilla contiene otro tablero de 3x3.

### ¿Qué es Ultimate TicTacToe?

En lugar de jugar en un solo tablero, juegas en **9 tableros simultáneamente**.  Tu movimiento en un tablero determina en qué tablero debe jugar tu oponente a continuación, añadiendo una capa extra de estrategia.

## ✨ Características

- 🎯 **Dos modos de juego**:
  - TicTacToe clásico (3x3)
  - Ultimate TicTacToe (HyperCat) - 9x9
  
- 🎨 **Interfaz gráfica intuitiva**:
  - Colores diferenciados por cuadrante
  - Indicadores visuales claros para jugadores X y O
  - Feedback inmediato de movimientos

## 🔧 Requisitos

- **Python**:  3.12 o superior
- **Tkinter**:  Incluido en la mayoría de instalaciones de Python
- **PDM**: Para gestión de dependencias (opcional pero recomendado)

### Dependencias del proyecto

```toml
[project]
dependencies = [
    "black>=25.12.0",  # Formateador de código
    "isort>=7.0.0"      # Organizador de imports
]
```

## 📥 Instalación

### Opción 1: Con PDM (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/AntoCreed777/HyperCat.git
cd HyperCat

# Instalar dependencias con PDM
pdm install

# Ejecutar el juego
pdm run python src/main.py
```

### Opción 2: Con pip estándar

```bash
# Clonar el repositorio
git clone https://github.com/AntoCreed777/HyperCat.git
cd HyperCat

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias de desarrollo
pip install black isort

# Ejecutar el juego
python src/main.py
```

### Opción 3: Ejecución directa (sin dependencias de desarrollo)

```bash
# Clonar el repositorio
git clone https://github.com/AntoCreed777/HyperCat.git
cd HyperCat

# Ejecutar directamente
python src/main.py
```

## 🎮 Uso

### Iniciar el juego

```bash
python src/main.py
```

Al ejecutar, se mostrará un menú: 

```
¿Qué deseas jugar? 
1. HyperCat
2. TicTacToe (Gato clásico)

Ingresa el número del juego: 
```

### Controles

- **Click izquierdo**:  Seleccionar casilla para jugar
- El juego alterna automáticamente entre jugadores X y O
- Los mensajes emergentes te informarán de: 
  - Movimientos inválidos
  - Fin del juego
  - Ganador o empate

## 📜 Reglas del Juego

### TicTacToe Clásico

1.  Dos jugadores (X y O) se turnan para marcar casillas en un tablero de 3x3
2. El primer jugador en conseguir 3 marcas en línea (horizontal, vertical o diagonal) gana
3. Si se llenan todas las casillas sin ganador, el juego termina en empate

### Ultimate TicTacToe (HyperCat)

#### Configuración
- El tablero principal es de 3x3, donde cada casilla contiene un sub-tablero de 3x3
- Total:  9 sub-tableros con 9 casillas cada uno (81 casillas en total)

#### Reglas especiales

1. **Primer movimiento**: El jugador X puede elegir cualquier casilla en cualquier sub-tablero

2. **Movimientos subsecuentes**: 
   - La posición donde jugaste dentro del sub-tablero determina en qué **sub-tablero** debe jugar tu oponente
   - Ejemplo: Si juegas en la casilla superior derecha de un sub-tablero, tu oponente debe jugar en el sub-tablero superior derecho

3. **Sub-tablero terminado**:
   - Si tu movimiento envía al oponente a un sub-tablero ya ganado, puede elegir **cualquier sub-tablero disponible**

4. **Ganar un sub-tablero**:
   - Se gana igual que el TicTacToe clásico (3 en línea)
   - El sub-tablero completo se marca con el símbolo del ganador

5. **Empate en sub-tablero**:
   - Si un sub-tablero termina en empate, se **reinicia** y vuelve a estar disponible para jugar

6. **Victoria final**:
   - Gana quien consiga 3 sub-tableros en línea (horizontal, vertical o diagonal) en el tablero principal

7. **Empate final**:
   - Si todos los sub-tableros están terminados sin un ganador en el tablero principal

## 🗂️ Estructura del Proyecto

```
HyperCat/
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada del programa
│   │
│   ├── core/                      # Lógica del juego
│   │   ├── __init__.py
│   │   ├── base_gato.py           # Clase abstracta base
│   │   ├── gato. py               # TicTacToe clásico
│   │   ├── hyper_cat.py           # Ultimate TicTacToe
│   │   └── exceptions_custom.py   # Excepciones personalizadas
│   │
│   ├── enums/                     # Enumeraciones
│   │   ├── __init__.py
│   │   ├── estado_casilla.py      # Estados:  VACIA, X, O
│   │   ├── resultado. py          # Resultados del juego
│   │   └── colors.py              # Colores para UI
│   │
│   └── ui/                        # Interfaz gráfica
│       ├── __init__.py
│       ├── ventana_base.py        # Clase base para ventanas
│       ├── ventana_gato.py        # UI TicTacToe clásico
│       └── ventana_hyper_cat.py   # UI Ultimate TicTacToe
│
├── . gitignore
├── pdm.lock
├── pyproject.toml
├── LICENSE
└── README.md
```

### Descripción de módulos

#### `core/`
- **`base_gato.py`**: Clase abstracta con lógica común (validación de victoria, cambio de turno, etc.)
- **`gato.py`**: Implementación del TicTacToe tradicional
- **`hyper_cat.py`**: Implementación del Ultimate TicTacToe con reglas avanzadas
- **`exceptions_custom.py`**: Jerarquía de excepciones para manejo de errores

#### `enums/`
- **`estado_casilla.py`**: Estados posibles de una casilla (VACIA, X, O)
- **`resultado.py`**: Resultados posibles (VICTORIA_X, VICTORIA_O, EMPATE, EN_CURSO)
- **`colors.py`**: Paleta de colores para la interfaz

#### `ui/`
- **`ventana_base.py`**: Funcionalidad común de UI (creación de tablero, botones, etc.)
- **`ventana_gato.py`**:  Ventana específica para TicTacToe clásico
- **`ventana_hyper_cat.py`**: Ventana específica para Ultimate TicTacToe con lógica de sub-tableros
