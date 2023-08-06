import time
import warnings
from functools import wraps, update_wrapper
from typing import Any, Callable, Optional, TypeVar

from prototools.componentes import Borde

PLUGINS = dict()

FuncType = Callable[..., Any]
F = TypeVar('F', bound=FuncType)


class Contador:
    """Cuenta el número de llamadas que realiza la funcion decorada.

    Examples:
        Scripts::

            @Contador
            def actualizar():
                print("Actualizando!")

            actualizar()
            actualizar()
            actualizar()
        
        Output::

            Llamada N°1 de 'actualizar'
            Actualizando!
            Llamada N°2 de 'actualizar'
            Actualizando!
            Llamada N°3 de 'actualizar'
            Actualizando!
    """
    def __init__(self, funcion) -> None:
        update_wrapper(self, funcion)
        self.funcion = funcion
        self.llamadas = 0

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.llamadas += 1
        print(f"Llamada N°{self.llamadas} de {self.funcion.__name__!r}")
        return self.funcion(*args, **kwargs)


def debug(funcion):
    """Muestra el signature de la función a decorar y retorna su valor.

    Example:
        Script::
        
            @debug
            def saludar(nombre):
                return f"Hola {nombre}"

            saludar("ProtoTools")

        Output::

            Llamando: saludar('ProtoTools')
            'saludar' retornó 'Hola ProtoTools'
    """
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Llamando: {funcion.__name__}({signature})")
        valor = funcion(*args, **kwargs)
        print(f"{funcion.__name__!r} retornó {valor!r}")
        return valor
    return wrapper

def obsoleto(mensaje):
    """Decora una funcion obsoleta y manda un mensaje de aviso.

    Example:
        Script::

            @obsoleto("se recomendia usar 'obtener_version()'")
            def obtener():
                return "version 1.0"

            print(obtener())

        Output::

            DeprecationWarning: 
            Función 'obtener' esta obsoleta!, se recomendia usar 
            'obtener_version()'
    
    """
    def inner(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"\nFunción '{funcion.__name__}' esta obsoleta!, {mensaje}",
                category=DeprecationWarning, 
                stacklevel=2,
                )
            return funcion(*args, **kwargs)
        return wrapper
    return inner

def registrar(funcion):
    """Registra una funcion como un plug-in.
    
    Example:
        Script::

            from prototools.decoradores import PLUGINS, registrar

            @registrar
            def f():
                pass

            print(PLUGINS)

        OUTPUT::

            {'f': <function f at 0x00000258176C64C8>}
    """
    PLUGINS[funcion.__name__] = funcion
    return funcion

def ralentizar(_funcion=None, *, radio: int = 1):
    """Ralentiza unos segundos antes de llamar a la función decorada.

    Example:
        Script::

            @ralentizar(radio=2)
            def temporizador(n):
                if n < 1:
                    print("Fin!")
                else:
                    print(n)
                    temporizador(n - 1)

            temporizador(3)

        Output::

            3
            2
            1
            Fin!
    """
    def inner(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            time.sleep(radio)
            return funcion(*args, **kwargs)
        return wrapper
    
    if _funcion is None:
        return inner
    else:
        return inner(_funcion)

def timer(funcion):
    """Imprime el tiempo de ejecución de la función a decorar.

    Example:
        Script::

            @timer
            def f(n):
                for _ in range(n):
                    sum([x**2 for x in range(10_000)])

            f(10)

        Output::

            f terminó en 0.0289 segundos
    """
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        fin = time.time()
        print(f"{funcion.__name__} terminó en {fin - inicio:.4f} segundos")
        return resultado
    return wrapper

def repetir(_funcion=None, *, n: int = 2):
    """Repite un número determinado de veces la función a decorar.

    Args:
        n (int): Cantidad de veces a repetir.

    Example:
        Script::

            @repetir(4)
            def saludar(nombre):
                print(f"Hola {nombre}!")

            saludar("ProtoTools")

        Output::
            
            Hola ProtoTools!
            Hola ProtoTools!
            Hola ProtoTools!
            Hola ProtoTools!
    """
    def inner(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                resultado = funcion(*args, **kwargs)
            return resultado
        return wrapper
    if _funcion is None:
        return inner
    else:
        return inner(_funcion)

def singleton(cls):
    """Convierte una clase en Singleton Class (una sola instancia).

    Example:
        Script::

            @singleton
            class T:
                pass

        >>> a = T()
        >>> b = T()
        >>> id(a)
        2031647265608
        >>> id(b)
        2031647265608
        >>> a is b
        True
    """
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper

def caja(_funcion=None, *, estilo="delgado"):
    """Caja que rodea al retorno de la función decorada.

    Args:
        estilo (str, optional): Estilo del borde.

    Example:
        Script::

            @caja(estilo="doble")
            def mensaje(msj):
                return msj

            mensaje("ProtoTools")

        Output::

            ╔════════════╗
            ║ ProtoTools ║
            ╚════════════╝ 
    """
    def inner(funcion):
        borde = Borde(estilo)
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            resultado = funcion(*args, **kwargs)
            print(u"{superior_izquierdo}{h}{superior_derecho}".format(
                superior_izquierdo=borde.superior_izquierdo,
                h=borde.horizontal * (len(resultado) + 2),
                superior_derecho=borde.superior_derecho,
            ))
            print(u"{lado_izquierdo}{contenido}{lado_derecho}".format(
                lado_izquierdo=borde.vertical,
                contenido=" "+resultado+" ",
                lado_derecho=borde.vertical,
            ))
            print(u"{inferior_izquierdo}{h}{inferior_derecho}".format(
                inferior_izquierdo=borde.inferior_izquierdo,
                h=borde.horizontal * (len(resultado) + 2),
                inferior_derecho=borde.inferior_derecho,
            ))
            return resultado
        return wrapper
    if _funcion is None:
        return inner
    else:
        return inner(_funcion)

def banner(contenido, ancho, estilo=None):
    """Banner.

    Example:
        Script::

            @banner("ProtoTools", 12)
            def mensaje():
                return None

            mensaje()

        Output::

            ════════════
             ProtoTools   
            ════════════
    """
    if estilo is not None:
        borde = Borde(estilo)
    borde = Borde("doble")
    def inner(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            print(borde.horizontal*ancho)
            resultado = funcion(*args, **kwargs)
            print(contenido.center(ancho))
            print(borde.horizontal*ancho)
            return resultado
        return wrapper
    return inner