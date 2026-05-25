"""
main.py:
Punto de entrada de la aplicación. Aquí se inicializa la interfaz gráfica
y se establece la conexión entre la vista y el controlador.
"""

from tkinter import Tk
from views.vista import Vista
from controllers.controlador import Controlador

__author__ = "Leandro Quintela, Franco Gimenez, Fernando Gallego"
__maintainer__ = "Leandro Quintela, Franco Gimenez, Fernando Gallego"
__email__ = (
    "quintela.leandro@gmail.com, francogimenez100@gmail.com, ferdinandgmaster@gmail.com"
)
__copyright__ = "Copyright (c) 2026 Leandro Quintela, Franco Gimenez, Fernando Gallego"
__license__ = "MIT"
__version__ = "0.0.1"


def iniciar_aplicacion():
    """
    Punto de entrada principal de la aplicación. Inicializa el ciclo de vida
    de Tkinter, el componente controlador y la interfaz gráfica de la vista.
    """
    # Instanciacion del Tkinter (abrimos loop de la ventana)
    root = Tk()

    # Instanciacion del controlador, que se encargará de manejar la lógica de la aplicación y de interactuar con la base de datos.
    controlador = Controlador()

    # Instanciacion de la vista, que se encargará de manejar la interfaz gráfica de la aplicación.
    # Se le pasa el controlador para que pueda interactuar con él. (__init__)
    Vista(root, controlador)

    # Se cierra el loop de la ventana.
    root.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
