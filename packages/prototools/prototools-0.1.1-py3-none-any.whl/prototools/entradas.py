import time
from builtins import input
from typing import Any, Callable, Optional, Union

import prototools.validaciones as v


class _EntradaExcepcion(Exception):
    """Clase base para excepciones. 

    Las excepciones son lanzadas cuando las funciones que la usan
    encuentran un problema.
    """
    pass


class _ValidacionExcepcion(_EntradaExcepcion):
    """Excepción lanzada cuando falla la validación de la entrada. Esta 
    excepción se levanta en vez de la excepción de validaciones.
    """
    pass


class _TiempoExcepcion(Exception):
    """Excepción lanzada cuando el usuario ha fallado en ingresar una
    entrada válida (periodo de tiempo agotado).
    """
    pass


class _LimiteExcepcion(Exception):
    """Excepción lanzada cuando el usuario ha fallado en ingresar una
    entrada (número de intentos agotados).
    """
    pass

def parametros() -> None:
	"""Parámetros comunes para todas las funciones de entrada:
    
    * ``indicacion`` (str): Texto a mostrar en cada entrada de usuario.
    * ``defecto`` (Any, None): Valor por defecto si se usa un timer.
    * ``vacio`` (bool): Si es verdadero, se aceptan valores en blanco.
    * ``tiempo`` (int, float): Número de segundos disponibles para 
        ingresar una entrada.
    * ``limite`` (int): Número de intentos permitidos.
    * ``aplicar`` (Callable, None): Función opcional.
    * ``validar`` (Callable, None): Función de validación opcional.
    """

def _verificar_tiempo_limite(
    inicio: float, 
    tiempo: float, 
    intentos: int, 
    limite: int,
) -> Union[_TiempoExcepcion, _LimiteExcepcion, None]:
    """Verifica el tiempo limite

    Args:
        inicio: Tiempo (Unix epoch) cuando la función fue llamada.
        tiempo: Número de segundos que el usuario tiene para ingresar
            una entrada válida.
        intentos: Número de intentos que el usuario realizó para 
            ingresar una entrada válida.
        limite: Número de intentos que el usuario tiene para ingresar
            una entrada válida.

    Returns:
        ``TiempoExcepcion`` o ``LimiteExcepcion`` si el usuario excedió
            esos limites, de lo contrario ``None``.
    """
    if (tiempo is not None) and (inicio + tiempo < time.time()):
        return _TiempoExcepcion()
    if limite is not None and intentos > limite:
        return _LimiteExcepcion()
    return None

def _entrada_generica(
    indicacion: str = "",
    defecto: Optional[Any] = None,
    tiempo: Optional[float] = None,
    limite: Optional[int] = None,
    aplicar: Optional[Callable] = None,
    validacion: Optional[Callable] = None,
    validar: Optional[Callable] = None,
    password: Optional[str] = None,
) -> Any:
    """Función base usada por otras funciones de entrada para manejar
    las operaciones comunes de cada función de entrada.

    Args:
        indicacion: Texto a mostrar.
        defecto: Valor por defecto que se muestra si se usa un el
            parámetro 'tiempo'.
        tiempo: Número de segundos disponibles para ingresar un valor
        limite: Número de intentos permitidos.
        aplicar: Función opcional que usa la entrada del usuario y 
            retorna un nuevo valor.
        validacion: Función de validación opcional.
        validar: Post validación.
        password: Máscara para contraseñas.
    """
    if not isinstance(indicacion, str):
        raise _EntradaExcepcion(
            "El argumento 'indicacion' debe ser de tipo str"
            )
    if not isinstance(limite, (int, type(None))):
        raise _EntradaExcepcion(
            "El argumento 'limite' debe ser de tipo int"
            )
    if not callable(validacion):
        raise _EntradaExcepcion(
            "El argumento 'validacion' debe ser una función"
            )
    if not (callable(aplicar) or aplicar is None):
        raise _EntradaExcepcion(
            "El argumento 'aplicar' debe ser una función o None"
            )
    if not (callable(validar) or validar is None):
        raise _EntradaExcepcion(
            "El argumento 'validar' deber ser una función o None"
            )
    
    tiempo_inicial = time.time()
    _intentos = 0
    
    while True:
        print(indicacion, end="")

        if password is None:
            entrada_usuario = input()
        else:
            entrada_usuario = input()
        
        _intentos += 1
        
        if aplicar is not None:
            entrada_usuario = aplicar(entrada_usuario)
        
        try:
            posible_nueva_entrada = validacion(entrada_usuario)
            if posible_nueva_entrada is not None:
                entrada_usuario = posible_nueva_entrada
        except Exception as exc:
            exc_limite_o_tiempo = _verificar_tiempo_limite(
                inicio=tiempo_inicial, 
                tiempo=tiempo, 
                intentos=_intentos, 
                limite=limite,
            )
            print(exc)
            if isinstance(exc_limite_o_tiempo, Exception):
                if defecto is not None:
                    return defecto
                else:
                    raise exc_limite_o_tiempo
            else:
                continue
        
        if tiempo is not None and tiempo_inicial + tiempo < time.time():
            if defecto is not None:
                return defecto
            else:
                raise _TiempoExcepcion()
        
        if validar is not None:
            return validar(entrada_usuario)
        else:
            return entrada_usuario

def entrada_str(
    indicacion: str = "",
    defecto: Optional[Any] = None,
    vacio: bool = None,
    tiempo: Optional[float] = None,
    limite: Optional[int] = None,
    aplicar: Optional[Callable] = None,
    validar: Optional[Callable] = None,
) -> str:
    """Pide al usuario una cadena de texto a ingresar.

    Args:
        indicacion: Texto a mostrar.
        defecto: Valor por defecto que se muestra si se usa un el
            parámetro 'tiempo'.
        vacio: Si es verdadero, acepta valores vacios.
        tiempo: Número de segundos disponibles para ingresar un valor
        limite: Número de intentos permitidos.
        aplicar: Función opcional que usa la entrada del usuario y 
            retorna un nuevo valor.
        validar: Post validación.
    """
    v._validar_parametros_genericos(vacio)
    validacion = lambda valor: v._pre_validacion(valor, vacio=vacio)[1]

    return _entrada_generica(
        indicacion=indicacion,
        defecto=defecto,
        tiempo=tiempo,
        limite=limite,
        aplicar=aplicar,
        validacion=validacion,
    )

def entrada_num(
    indicacion="",
    defecto=None,
    vacio=False,
    tiempo=None,
    limite=None,
    aplicar=None,
    validar=None,
    min=None,
    max=None,
    menor=None,
    mayor=None,
):
    """
    """
    v._validar_parametros_numeros(min=min, max=max, menor=menor, mayor=mayor)

    validacion = lambda valor: v.validar_numero(
        valor,
        vacio=vacio,
        min=min,
        max=max,
        menor=menor, 
        mayor=mayor,
        _tipo="num",
    )

    return _entrada_generica(
        indicacion=indicacion,
        defecto=defecto,
        tiempo=tiempo,
        limite=limite,
        aplicar=aplicar,
        validar=validar,
        validacion=validacion,
    )

def entrada_int(
    indicacion: str = "",
    defecto: Optional[Any] = None,
    vacio: bool = False,
    tiempo: Optional[float] = None,
    limite: Optional[int] = None,
    aplicar: Optional[Callable] = None,
    validar: Optional[Callable] = None,
    min: Optional[int] = None,
    max: Optional[int] = None,
    menor: Optional[int] = None,
    mayor: Optional[int] = None,
):
    """Pide al usuario ingresar un valor numerico entero.

    Args:
        
        indicacion: Texto a mostrar.
        defecto: Valor por defecto que se muestra si se usa un el
            parámetro 'tiempo'.
        vacio: Si es verdadero, acepta valores vacios.
        tiempo: Número de segundos disponibles para ingresar un valor
        limite: Número de intentos permitidos.
        aplicar: Función opcional que usa la entrada del usuario y 
            retorna un nuevo valor.
        validar: Función de validación opcional.
        min: Valor mínimo (inclusivo).
        max: Valor máximo (inclusivo).
        menor: Valor mínimo (excluyente).
        mayor: Valor máximo (excluyente).
	"""
    v._validar_parametros_numeros(min=min, max=max, menor=menor, mayor=mayor)

    validacion = lambda valor: v.validar_numero(
        valor,
        vacio=vacio,
        min=min,
        max=max,
        menor=menor, 
        mayor=mayor,
        _tipo="num",
    )

    resultado = _entrada_generica(
        indicacion=indicacion,
        defecto=defecto,
        tiempo=tiempo,
        limite=limite,
        aplicar=aplicar,
        validacion=validacion,
    )

    try: 
        resultado = int(float(resultado))
    except ValueError:
        pass

    if validar is None:
        return resultado
    else:
        return validar(resultado)

def entrada_sino(
    indicacion="",
    si="si",
    no="no",
    sensible=False,
    defecto=None,
    vacio=False,
    tiempo=None,
    limite=None,
    aplicar=None,
    validar=None,
):
    """Ingresar respuestas de tipo si/no
    """
    validacion = lambda valor: v.validar_si_no(
        valor,
        si=si,
        no=no,
        sensible=sensible,
        vacio=vacio,
    )

    resultado = _entrada_generica(
        indicacion=indicacion,
        defecto=defecto,
        tiempo=tiempo,
        limite=limite,
        aplicar=aplicar,
        validacion=validacion,
    )

    resultado = v.validar_si_no(
        resultado,
        si=si,
        no=no,
        sensible=sensible,
        vacio=vacio,
    )

    if validar is None:
        return resultado
    else:
        return validar(resultado)


for functionname in (
    "validar_numero",
    "validar_int",
    "valida_sino",
):
    exec(
        f"""def {functionname}(valor, *args, **kwargs):
    try:
        return v.{functionname}(valor, *args, **kwargs)
    except v.ValidacionExcepcion as e:
        raise ValidacionExcepcion(str(e))"""
    )