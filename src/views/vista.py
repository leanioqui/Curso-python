from tkinter import *
from tkinter import ttk, messagebox

from views.interfaces import menu_principal, configurar_menu_consulta, configurar_menu_modificar
class Vista():
    def __init__(self, root, controlador):
        self.controlador = controlador
        self.root = root
        
        root.title(f"Impacto Ambiental | CABA: {controlador.clima_caba()} | Gestión de Riesgos")

        #-DECLARACION DE VARIABLES
        self.var_categoria = StringVar()
        self.var_descripcion = StringVar()
        self.var_impacto = IntVar()
        self.var_busqueda = StringVar()

        #-DECLARACION DE VENTANAS
        frame_ab = Frame(root) #Frame para altas y bajas 
        frame_ab.title = "Menu Principal"

        frame_modificacion = Frame(root) #Frame para modificaciones
        frame_modificacion.title = "Menu Modificación"

        frame_consulta = Frame(root) #Frame para consultas
        frame_consulta.title = "Menu Consulta"

        # Al iniciar, solo mostramos el de AB
        frame_ab.grid(row=0, column=0, sticky="nsew") 
        frame_ab.rowconfigure(2, minsize=10)


        #-EVENTO AL TOCAR "X"
        # Esta línea conecta el evento de la "X" con tu función
        root.protocol("WM_DELETE_WINDOW", controlador.al_cerrar)

        """
        El método protocol() se utiliza para interceptar eventos específicos de la ventana. 
        En este caso, "WM_DELETE_WINDOW" es el evento que se genera cuando el usuario intenta cerrar la ventana (haciendo clic en la "X"). 
        Al asociar este evento con la función al_cerrar, 
        se garantiza que se ejecute la lógica personalizada definida en esa función antes de cerrar la ventana.
        """


        #-DISPOSICION DE TREEVIEW
        #Creamos el árbol original
        tree = ttk.Treeview(root, height=20)

        #Creamos las columnas que tendrá nuestro árbol original sin contar la columna de id
        tree["columns"] = ("col1", "col2", "col3")

        #Creamos las columnas estableciendo su tamaño y las nomenclamos 
        tree.column("#0", width=50, minwidth=50, anchor=W)
        tree.heading("#0", text="ID", anchor=W)
        tree.column("col1", width=150, minwidth=150, anchor=W)
        tree.heading("col1", text="Categoria", anchor=W)
        tree.column("col2", width=150, minwidth=150, anchor=W)
        tree.heading("col2", text="Descripción", anchor=W)
        tree.column("col3", width=150, minwidth=150, anchor=W)
        tree.heading("col3", text="Impacto", anchor=W)

        #Colocamos el árbol original
        tree.grid(column=0, row=4, columnspan=4, sticky="nsew")

        #Creamos el árbol de consulta, pero lo dejamos oculto
        tree_consulta = ttk.Treeview(root, height=20) 

        #Creamos las columnas que tendrá nuestro árbol de consulta, sin contar la columna de id
        tree_consulta["columns"] = ("col1", "col2", "col3")

        #Creamos las columnas estableciendo su tamaño y las nomenclamos 
        tree_consulta.column("#0", width=50, minwidth=50, anchor=W)
        tree_consulta.heading("#0", text="ID", anchor=W)
        tree_consulta.column("col1", width=150, minwidth=150, anchor=W)
        tree_consulta.heading("col1", text="Categoria", anchor=W)
        tree_consulta.column("col2", width=150, minwidth=150, anchor=W)
        tree_consulta.heading("col2", text="Descripción", anchor=W)
        tree_consulta.column("col3", width=150, minwidth=150, anchor=W)
        tree_consulta.heading("col3", text="Impacto", anchor=W)


        #-CONFIGURACIÓN DE RESPONSIVIDAD
        #Hacemos que los botones y el árbol se ajusten al tamaño de la ventana
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(4, weight=1)

        # Hacemos que los botones del menú se repartan el ancho y alto igualitariamente
        for i in range(4): # Recorremos las columnas del frame de botones (0 a 3)   
            frame_ab.columnconfigure(i, weight=1) 
            frame_ab.rowconfigure(i, weight=1)


        controlador.actualizar_tree()
        menu_principal()
        root.mainloop()





    
    def aplicar_estilo_recursivo(self, root, color_botones, color_letra): #Esta funcion aplica colores de fondo y texto a todos los widgets de la interfaz de manera recursiva
        for w in root.winfo_children(): #winfo_children() devuelve una lista de todos los widgets hijos directos del widget root, 
                                        # es decir, los widgets que están contenidos dentro de root.
            try: w.configure(bg=color_botones, fg=color_letra) # Intenta pintar fondo y letra
            except: 
                try: w.configure(bg=color_botones)    # Si no tiene letra (como Frames), solo fondo
                except: pass
            self.aplicar_estilo_recursivo(w, color_botones, color_letra) # Sigue con los hijos

    def modo_claro(self, root): #Funcion que define los colores del Modo Claro
        style = ttk.Style()
        style.theme_use('vista')
        root.config(bg="SystemButtonFace") #SystemButtonFace es el color de fondo predeterminado de los botones en Windows, 
                                            #al usarlo como fondo para la ventana principal, se logra un aspecto más claro y consistente con el tema clásico de Windows.
        self.aplicar_estilo_recursivo(root, "SystemButtonFace", "black") #Pinta fondo y letra de todos los widgets, 
                                                                    #el fondo se pinta con el color predeterminado del sistema para botones (SystemButtonFace) 
                                                                    # y la letra se pinta de negro
        self.barra_titulo.config(background="#46dab7", foreground="black")

    def modo_oscuro(self, root): #Funcion que define los colores del Modo Oscuro
        style = ttk.Style()
        style.theme_use("clam")
        bg, fg = "#121212", "#ffffff" # Variables cortas
        
        # Configuración de los componentes TTK (Treeview/Combobox)
        style.configure("Treeview", background="#1e1e1e", foreground=fg, fieldbackground="#1e1e1e", borderwidth=0)
        style.configure("Treeview.Heading", background="#333333", foreground=fg, relief="flat")
        style.map("Treeview", background=[('selected', '#007acc')])
        style.configure("TCombobox", fieldbackground="#1e1e1e", background="#333333", foreground=fg)

        root.config(bg=bg)
        self.aplicar_estilo_recursivo(root, bg, fg)
        self.barra_titulo.config(background="#1f6857", foreground=fg)

    def funcion_volver_menu_principal(self):
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
