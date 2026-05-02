from tkinter import Tk
from views.vista import Vista
from controllers.controlador import Controlador

if __name__ == "__main__":
    
    #Instanciacion del Tkinter (abrimos loop de la ventana))
    root = Tk() 
    
    #Instanciacion del controlador, que se encargará de manejar la lógica de la aplicación y de interactuar con la base de datos.
    controlador = Controlador()
    
    #Instanciacion de la vista, que se encargará de manejar la interfaz gráfica de la aplicación. 
    #Se le pasa el controlador para que pueda interactuar con él. (__init__)
    iniciar_app = Vista(root, controlador)
    
    #Se cierra el loop de la ventana.
    root.mainloop()