"""
vista.py:
Este módulo define la clase Vista, que se encarga de manejar la interfaz gráfica de la aplicación.
"""

from tkinter import ttk, StringVar, IntVar, Frame, W
from views.interfaces import menu_principal, configurar_menu_consulta, configurar_menu_modificar
class Vista():
    def __init__(self, root, controlador):
        """
        Inicializa la interfaz gráfica de la aplicación de Gestión de Riesgos e Impacto Ambiental.

        Configura las variables de Tkinter, define los diferentes frames (menús) de la aplicación,
        los componentes Treeview (tanto el principal como el de consulta) y establece las reglas de
        responsividad de la ventana. Además, intercepta el evento de cierre de la ventana ("WM_DELETE_WINDOW")
        para asegurar que se ejecute la lógica de salida personalizada del controlador antes de destruir la interfaz.

        :param root: La ventana principal de la aplicación.
        :type root: tkinter.Tk
        :param controlador: La instancia del controlador que maneja la lógica de negocio y eventos.
        :type controlador: Controlador
        """
        self.controlador = controlador
        self.root = root
        
        self.root.title(f"Impacto Ambiental | CABA: {controlador.clima_caba()} | Gestión de Riesgos")

        #-DECLARACION DE VARIABLES
        self.var_categoria = StringVar()
        self.var_descripcion = StringVar()
        self.var_impacto = IntVar()
        self.var_busqueda = StringVar()

        #-DECLARACION DE VENTANAS
        self.frame_ab = Frame(self.root) #Frame para altas y bajas 
        self.frame_ab.title = "Menu Principal"

        self.frame_modificacion = Frame(self.root) #Frame para modificaciones
        self.frame_modificacion.title = "Menu Modificación"

        self.frame_consulta = Frame(self.root) #Frame para consultas
        self.frame_consulta.title = "Menu Consulta"

        # Al iniciar, solo mostramos el de AB
        self.frame_ab.grid(row=0, column=0, sticky="nsew") 
        self.frame_ab.rowconfigure(2, minsize=10)


        #-EVENTO AL TOCAR "X"
        # Esta línea conecta el evento de la "X" con tu función
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.controlador.al_cerrar(self.root))

        """
        El método protocol() se utiliza para interceptar eventos específicos de la ventana. 
        En este caso, "WM_DELETE_WINDOW" es el evento que se genera cuando el usuario intenta cerrar la ventana (haciendo clic en la "X"). 
        Al asociar este evento con la función al_cerrar, 
        se garantiza que se ejecute la lógica personalizada definida en esa función antes de cerrar la ventana.
        """


        #-DISPOSICION DE TREEVIEW
        #Creamos el árbol original
        self.tree = ttk.Treeview(self.root, height=20)

        #Creamos las columnas que tendrá nuestro árbol original sin contar la columna de id
        self.tree["columns"] = ("col1", "col2", "col3")

        #Creamos las columnas estableciendo su tamaño y las nomenclamos 
        self.tree.column("#0", width=50, minwidth=50, anchor=W)
        self.tree.heading("#0", text="ID", anchor=W)
        self.tree.column("col1", width=150, minwidth=150, anchor=W)
        self.tree.heading("col1", text="Categoria", anchor=W)
        self.tree.column("col2", width=150, minwidth=150, anchor=W)
        self.tree.heading("col2", text="Descripción", anchor=W)
        self.tree.column("col3", width=150, minwidth=150, anchor=W)
        self.tree.heading("col3", text="Impacto", anchor=W)

        #Colocamos el árbol original
        self.tree.grid(column=0, row=4, columnspan=4, sticky="nsew")

        #Creamos el árbol de consulta, pero lo dejamos oculto
        self.tree_consulta = ttk.Treeview(self.root, height=20) 

        #Creamos las columnas que tendrá nuestro árbol de consulta, sin contar la columna de id
        self.tree_consulta["columns"] = ("col1", "col2", "col3")

        #Creamos las columnas estableciendo su tamaño y las nomenclamos 
        self.tree_consulta.column("#0", width=50, minwidth=50, anchor=W)
        self.tree_consulta.heading("#0", text="ID", anchor=W)
        self.tree_consulta.column("col1", width=150, minwidth=150, anchor=W)
        self.tree_consulta.heading("col1", text="Categoria", anchor=W)
        self.tree_consulta.column("col2", width=150, minwidth=150, anchor=W)
        self.tree_consulta.heading("col2", text="Descripción", anchor=W)
        self.tree_consulta.column("col3", width=150, minwidth=150, anchor=W)
        self.tree_consulta.heading("col3", text="Impacto", anchor=W)


        #-CONFIGURACIÓN DE RESPONSIVIDAD
        #Hacemos que los botones y el árbol se ajusten al tamaño de la ventana
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(4, weight=1)

        # Hacemos que los botones del menú se repartan el ancho y alto igualitariamente
        for i in range(4): # Recorremos las columnas del frame de botones (0 a 3)   
            self.frame_ab.columnconfigure(i, weight=1) 
            self.frame_ab.rowconfigure(i, weight=1)

        menu_principal(self)
        self.controlador.actualizar_tree(self.tree) #Llenamos el árbol original con los datos de la base de datos


    def aplicar_estilo_recursivo(self, root, color_botones, color_letra): #Esta funcion aplica colores de fondo y texto a todos los widgets de la interfaz de manera recursiva
        """
        Aplica colores de fondo y texto a todos los widgets de la interfaz de manera recursiva.

        Utiliza el método ``winfo_children()`` para obtener los elementos hijos directos del contenedor
        actual. Intenta aplicar las propiedades de fondo (`bg`) y texto (`fg`) mediante bloques try-except
        para evitar fallos en componentes que no soportan texto (como los objetos Frame). Al finalizar con
        los elementos directos, se invoca a sí mismo para continuar la propagación en los niveles inferiores.

        :param root: El widget contenedor o ventana desde el cual iniciar la propagación del estilo.
        :type root: tkinter.Widget o tkinter.Tk
        :param color_botones: El color en formato hexadecimal o nombre para el fondo (background).
        :type color_botones: str
        :param color_letra: El color en formato hexadecimal o nombre para el texto (foreground).
        :type color_letra: str
        """
        for w in root.winfo_children(): #winfo_children() devuelve una lista de todos los widgets hijos directos del widget root, 
                                        # es decir, los widgets que están contenidos dentro de root.
            try: w.configure(bg=color_botones, fg=color_letra) # Intenta pintar fondo y letra
            except: 
                try: w.configure(bg=color_botones)    # Si no tiene letra (como Frames), solo fondo
                except: pass
            self.aplicar_estilo_recursivo(w, color_botones, color_letra) # Sigue con los hijos

    def modo_claro(self, root): #Funcion que define los colores del Modo Claro
        """
        Define y aplica la paleta de colores correspondiente al Modo Claro en la interfaz gráfica.

        Configura el tema de los componentes ``ttk`` utilizando el estilo 'vista' y establece el color de 
        la ventana principal al valor predeterminado de Windows (``SystemButtonFace``) para mantener la 
        consistencia visual del sistema operativo. Posteriormente, invoca de manera interna la propagación 
        recursiva de estilos para modificar el fondo y color de texto (negro) de todos los widgets hijos, 
        finalizando con la personalización de la barra de títulos.

        :param root: La ventana o contenedor principal al que se le aplicará el cambio de tema.
        :type root: tkinter.Tk o tkinter.Widget
        """
        style = ttk.Style()
        style.theme_use('vista')
        self.root.config(bg="SystemButtonFace") #SystemButtonFace es el color de fondo predeterminado de los botones en Windows, 
                                            #al usarlo como fondo para la ventana principal, se logra un aspecto más claro y consistente con el tema clásico de Windows.
        self.aplicar_estilo_recursivo(self.root, "SystemButtonFace", "black") #Pinta fondo y letra de todos los widgets, 
                                                                    #el fondo se pinta con el color predeterminado del sistema para botones (SystemButtonFace) 
                                                                    # y la letra se pinta de negro
        self.barra_titulo.config(background="#46dab7", foreground="black")

    def modo_oscuro(self, root): #Funcion que define los colores del Modo Oscuro
        """
        Define y aplica la paleta de colores correspondiente al Modo Oscuro en la interfaz gráfica.

        Cambia el tema activo de los componentes ``ttk`` al estilo 'clam' y reconfigura los elementos
        visuales avanzados (como el Treeview y el Combobox) para que utilicen fondos oscuros (``#1e1e1e``)
        y textos claros, incluyendo el comportamiento de selección (resaltado en azul ``#007acc``). 
        Finalmente, establece el fondo general de la aplicación en gris oscuro (``#121212``), propaga 
        los colores de manera recursiva a todos los widgets hijos y actualiza la barra de títulos.

        :param root: La ventana o contenedor principal al que se le aplicará el cambio de tema.
        :type root: tkinter.Tk o tkinter.Widget
        """
        style = ttk.Style()
        style.theme_use("clam") 
        bg, fg = "#121212", "#ffffff" # Variables cortas
        
        # Configuración de los componentes TTK (Treeview/Combobox)
        style.configure("Treeview", background="#1e1e1e", foreground=fg, fieldbackground="#1e1e1e", borderwidth=0)
        style.configure("Treeview.Heading", background="#333333", foreground=fg, relief="flat")
        style.map("Treeview", background=[('selected', '#007acc')])
        style.configure("TCombobox", fieldbackground="#1e1e1e", background="#333333", foreground=fg)

        self.root.config(bg=bg)
        self.aplicar_estilo_recursivo(self.root, bg, fg)
        self.barra_titulo.config(background="#1f6857", foreground=fg)

    def funcion_volver_menu_principal(self):
        """
        Restablece la interfaz gráfica al estado del menú principal de altas y bajas (AB).

        Oculta los contenedores secundarios utilizando el método ``grid_forget()`` (tanto el frame de 
        modificaciones como el de consultas) y remueve de la vista el árbol secundario. Posteriormente, 
        vuelve a posicionar el frame principal y el Treeview original en la grilla. Como paso final de 
        limpieza, vacía por completo el árbol de consultas recorriendo y eliminando de forma explícita 
        todos sus nodos hijos.
        """
        #Escondemos los frames de modificaciones y consultas 
        self.frame_modificacion.grid_forget()
        self.frame_consulta.grid_forget()

        #Escondemos el árbol de consultas
        self.tree_consulta.grid_forget()

        #Colocamos el frame de altas y bajas
        self.frame_ab.grid(row=1, column=0, sticky="nsew") 
        
        #Colocamos el árbol original
        self.tree.grid(row=6, column=0, columnspan=4, sticky="nsew")

        #Recorremos los elementos del árbol del 'menu consulta' y los eliminamos con el fin de dejarlo vacío
        for i in self.tree_consulta.get_children():
            self.tree_consulta.delete(i)

    def correr_modificar(self):
        """
        Cambia el estado de la interfaz gráfica para mostrar el menú de modificaciones.

        Oculta el frame principal de altas y bajas (AB) utilizando ``grid_forget()`` y 
        posiciona el contenedor de modificaciones en la grilla. Finalmente, invoca a la 
        función externa ``configurar_menu_modificar`` para inicializar los componentes y 
        botones específicos de esta vista.
        """
        self.frame_ab.grid_forget()
        self.frame_modificacion.grid(row=1, column=0)
        configurar_menu_modificar(self)

    def correr_consultar(self):
        """
        Cambia el estado de la interfaz gráfica para mostrar el menú de consultas.

        Oculta el frame principal de altas y bajas (AB) utilizando ``grid_forget()`` y 
        posiciona el contenedor de consultas en la grilla. Finalmente, invoca a la 
        función externa ``configurar_menu_consulta`` para inicializar los componentes y 
        criterios de búsqueda específicos de esta vista.
        """
        self.frame_ab.grid_forget()
        self.frame_consulta.grid(row=1, column=0)
        configurar_menu_consulta(self)