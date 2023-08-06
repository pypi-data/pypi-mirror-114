"""
Modulo Experimental
"""
import re
from typing import Tuple
from prototools.config import RELLENOS, MARGENES, BORDES, TIPOS_BORDES

tipo = TIPOS_BORDES[1]

Relleno = type("Relleno", (), RELLENOS)
Margenes = type("Margenes", (), MARGENES)
Borde = type(
    "Borde", (), {atributo:valor[tipo] for atributo, valor in BORDES.items()}
    )

class Margen:
    def __init__(self) -> None:
        for atributo, valor in MARGENES.items():
            setattr(self, atributo, valor)


def partir(predicado, valores) -> Tuple[list, list]:
    """
    Separa los valores en dos conjuntos, basado en el retorno de la 
    función (True/False):

        >>> t = partir(lambda x: x < 4, range(9))
        ([4, 5, 6, 7, 8], [0, 1, 2, 3])
    """
    resultado = ([], [])
    for item in valores:
        resultado[predicado(item)].append(item)
    return resultado

def strip_ansi(s):
    t = re.compile(r"""
    \x1b     # literal ESC
    \[       # literal [
    [;\d]*   # zero or more digits or semicolons
    [A-Za-z] # a letter
    """, re.VERBOSE).sub
    return t("",s)
