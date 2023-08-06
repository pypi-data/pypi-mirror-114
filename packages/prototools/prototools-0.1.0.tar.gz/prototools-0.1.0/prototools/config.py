# Archivo de configuracion
# 
# Este archivo contiene una seleccion de las opciones mas comunes: Para mayor
# detalle ver la documentacion:
# https://github.com/leugimkm/prototools
# -- General configuration ---------------------------------------------------

# -- Opciones para el modulo menu.py  ----------------------------------------

TIPOS_BORDES = {
    0: "ascii", 
    1: "delgado",
    2: "grueso",
    3: "doble",
}

BORDES = {
    "superior_izquierdo": {
        "ascii": "+", 
        "delgado": u"\u250C", "grueso": u"\u250F", "doble": u"\u2554",
    },
    "superior_derecho": {
        "ascii": "+",
        "delgado": u"\u2510", "grueso": u"\u2513", "doble": u"\u2557",
    },
    "inferior_izquierdo": {
        "ascii": "+",
        "delgado": u"\u2514", "grueso": u"\u2517", "doble": u"\u255A",
    },
    "inferior_derecho": {
        "ascii": "+",
        "delgado": u"\u2518", "grueso": u"\u251B", "doble": u"\u255D",
    },
    "vertical": {
        "ascii": "|",
        "delgado": u"\u2502", "grueso": u"\u2503", "doble": u"\u2551",
    },
    "vertical_izquierdo": {
        "ascii": "|",
        "delgado": u"\u251C", "grueso": u"\u2523", "doble": u"\u2560",
    },
    "vertical_derecho": {
        "ascii": "|",
        "delgado": u"\u2524", "grueso": u"\u252B", "doble": u"\u2563",
    },
    "horizontal": {
        "ascii": "-",
        "delgado": u"\u2500", "grueso": u"\u2501", "doble": u"\u2550",
    },
    "horizontal_superior": {
        "ascii": "-",
        "delgado": u"\u252C", "grueso": u"\u2533", "doble": u"\u2566",
    },
    "horizontal_inferior": {
        "ascii": "-",
        "delgado": u"\u2534", "grueso": u"\u253B", "doble": u"\u2569",
    },
    "interseccion": {
        "ascii": "+",
        "delgado": u"\u253C", "grueso": u"\u254B", "doble": u"\u256C",
    },
}

MARGENES = {
    "izquierdo": 2,
    "derecho": 2,
    "superior": 1,
    "inferior": 0,
}

RELLENOS = {
    "izquierdo": 2,
    "derecho": 2,
    "superior": 1,
    "inferior": 1,
}

# -- Opciones para el modulo color.py  ---------------------------------------

CSI = "\033["

ANSICOLOR = {
    "fore": {
        "negro": 30,
        "rojo": 31,
        "verde": 32,
        "amarillo": 33,
        "azul": 34,
        "magenta": 35,
        "cyan": 36,
        "blanco": 37,
        "reset": 39,
    },
    "back": {
        "negro": 40,
        "rojo": 41,
        "verde": 42,
        "amarillo": 43,
        "azul": 44,
        "magenta": 45,
        "cyan": 46,
        "blanco": 47,
        "reset": 49,
    },
}