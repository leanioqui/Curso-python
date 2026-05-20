"""
mis_regex.py:
Este módulo define la clase MisRegex, que se encarga de manejar las expresiones regulares utilizadas en la aplicación para validar los datos ingresados por el usuario.
Actualmente, incluye un método para validar que solo se ingresen letras en ciertos campos.
"""

import re
class MisRegex:
    def __init__(self):

        self.filtro = re.compile(r'\D') #Crea un patrón de expresión regular que se usará para buscar caracteres no numéricos en el texto.

    def solo_letras(self):
        """
        Este método devuelve un patrón de expresión regular que se utiliza para validar 
        que solo se ingresen letras en ciertos campos de la aplicación.

        :param self: La instancia de la clase MisRegex.
        :type self: MisRegex
        :return: Un patrón de expresión regular que busca caracteres no numéricos.
        :rtype: re.Pattern
        """
        return re.compile(r'\D') #Crea un patrón de expresión regular que se usará para buscar caracteres no numéricos en el texto.
