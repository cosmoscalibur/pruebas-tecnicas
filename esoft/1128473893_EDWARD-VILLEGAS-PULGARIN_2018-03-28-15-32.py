# -*- coding: utf-8 -*-

"""
Módulo de la prueba técnica.

Este módulo contiene las funciones requeridas para el desarrollo de la prueba
técnica suministrada por el grupo ESOFT.

.. caution::
   Dado que los guiones medios no puedes ser usados en los nombres de los
   archivos de código debe cambiar el nombre por uno que cumpla las condiciones
   de ejecución.

Suponga que ha renombrado el archivo a :code:`esoft.py`. Ubicando la consola en
el directorio donde está el archivo puede ejecutar como sigue:

>>> import esoft
>>> esoft.prueba(3, 3)

El resultado difiere tras cada ejecución por la condición de números
aleatorios para la formación de la matriz.

.. note::
   Al desconocer el entorno de prueba, se desarrolla el código solo dependiendo
   de la biblioteca estándar de python y es funcional con python2.7 y python3.

Si desea probar las otras funciones, asegurese de realizar el :code:`import`
de la forma adecuada.
"""

from __future__ import division
import random

# 1128473893_EDWARD-VILLEGAS-PULGARIN_2018-03-28-HH-MM.py
# Código en github
# https://docs.google.com/forms/d/e/1FAIpQLSebqSwjqWj1t0lsUkKvIASfdR5nWv1KKQyg1cDebUBgbhM6AA/viewform?usp=sf_link


def generar_matriz(N, M):
    """
    Generación de matriz solicitada.

    Función que genera una matriz :math:`N\\times M` de elementos aleatorios
    desde 1 hasta :math:`NM`.

    :param int N: Número mayor o igual que 2 que determina las filas de la
                  matriz.
    :param int M: Número mayor o igual que 2 que determina las columnas de la
                  matriz.
    :return: Matriz generada.
    :rtype: list(list[int])
    :raises ValueError: Si uno de los argumentos es menor que 2.
    """
    if (N < 2) or (M < 2):
        raise ValueError("Ambos argumentos deben ser mayores o iguales que 2.")
    else:
        total_elementos = N * M
        elementos_unicos = range(1, total_elementos + 1)
        elementos_aleatorizados = random.sample(elementos_unicos,
                                                total_elementos)
        matriz = [elementos_aleatorizados[M * i:M * (i + 1)] for i in range(N)]
    return matriz


def sumas(matriz):
    """
    Desarrollo de sumas de columnas.

    Función que genera el promedio de las sumas de las columnas pares de la
    matriz ingresada y las sumas de las columnas individuales.

    .. attention::
       La numeración de las columnas corresponde a la numeración tradicional de
       python donde el primer indice es 0.

    :param matriz: Matriz sobre la cual se desarrollan la sumas.
    :param type: list(list[int])
    :return: Tuple cuyo primer valor es el promedio de las sumas de las
             columnas pares y el segundo elemento es la lista de sumas de las
             columnas.
    :rtyoe: tuple(int, list[int])

    >>> a = [[5, 3, 8], [1, 2, 4], [9, 7, 6]]
    >>> sumas(a)
    (16.5, [15, 12, 18])
    """
    filas = len(matriz)
    columnas = len(matriz[0])
    sumas_columnas = [sum([matriz[i][j] for i in range(filas)]) for j in
                      range(columnas)]
    suma_par = sum([sumas_columnas[i] for i in range(0, columnas, 2)])
    promedio_par = suma_par / (int(columnas / 2) + 1)
    return promedio_par, sumas_columnas


def cumple(matriz):
    """
    Validación de condición solicitada.

    Función que determina la cantidad de columnas cuya suma de elementos es
    superior al promedio de la suma de las columnas pares.

    .. attention::
       La numeración de las columnas corresponde a la numeración tradicional de
       python donde el primer indice es 0.

    :param matriz: Matriz a la cual se verificara la condición de sus columnas.
    :type matriz: list(list[int])
    :return: Cantidad de columnas cuya suma supera el promedio de la suma de
             las columnas pares.
    :rtype: int

    >>> a = [[5, 3, 8], [1, 2, 4], [9, 7, 6]]
    >>> cumple(a)
    1
    """
    promedio, sumas_columnas = sumas(matriz)
    mayores = [promedio < suma for suma in sumas_columnas]
    return sum(mayores)


def prueba(N, M):
    """
    Función principal de la prueba técnica del Grupo ESOFT.

    :param int N: Número entero mayor o igual que 2. Determina las filas.
    :param int M: Número entero mayor o igual que 2. Determina las columnas.
    :return: Retorno el número de columnas cuya suma es mayor al promedio de
             las sumas de las columnas pares.
    :rtype: int

    >>> prueba(3, 3)
    """
    matriz = generar_matriz(N, M)
    return cumple(matriz)
