# 1. Librerías de Interfaz (Tkinter)
from tkinter import *
from tkinter import ttk, messagebox

# 2. Módulos locales (Controlador y Modelo)
from controlador import (
    clima_caba, funcion_guardar, funcion_borrar, funcion_consultar, 
    funcion_modificar, funcion_total, funcion_promedio, copiar_fila, 
    al_cerrar, actualizar_tree, funcion_modificar_variables, 
    funcion_volver_menu_principal, ver_instrucciones, modo_claro, 
    modo_oscuro, busqueda
)
from modelo import con

#--------------------------------ESTILO-----------------------------------------
def aplicar_estilo_recursivo(root, color_botones, color_letra): #Esta funcion aplica colores de fondo y texto a todos los widgets de la interfaz de manera recursiva
    for w in root.winfo_children(): #winfo_children() devuelve una lista de todos los widgets hijos directos del widget root, 
                                    # es decir, los widgets que están contenidos dentro de root.
        try: w.configure(bg=color_botones, fg=color_letra) # Intenta pintar fondo y letra
        except: 
            try: w.configure(bg=color_botones)    # Si no tiene letra (como Frames), solo fondo
            except: pass
        aplicar_estilo_recursivo(w, color_botones, color_letra) # Sigue con los hijos

def modo_claro(root): #Funcion que define los colores del Modo Claro
    style = ttk.Style()
    style.theme_use('vista')
    root.config(bg="SystemButtonFace") #SystemButtonFace es el color de fondo predeterminado de los botones en Windows, 
                                        #al usarlo como fondo para la ventana principal, se logra un aspecto más claro y consistente con el tema clásico de Windows.
    aplicar_estilo_recursivo(root, "SystemButtonFace", "black") #Pinta fondo y letra de todos los widgets, 
                                                                #el fondo se pinta con el color predeterminado del sistema para botones (SystemButtonFace) 
                                                                # y la letra se pinta de negro
    barra_titulo.config(background="#46dab7", foreground="black")

def modo_oscuro(root): #Funcion que define los colores del Modo Oscuro
    style = ttk.Style()
    style.theme_use("clam")
    bg, fg = "#121212", "#ffffff" # Variables cortas
    
    # Configuración de los componentes TTK (Treeview/Combobox)
    style.configure("Treeview", background="#1e1e1e", foreground=fg, fieldbackground="#1e1e1e", borderwidth=0)
    style.configure("Treeview.Heading", background="#333333", foreground=fg, relief="flat")
    style.map("Treeview", background=[('selected', '#007acc')])
    style.configure("TCombobox", fieldbackground="#1e1e1e", background="#333333", foreground=fg)

    root.config(bg=bg)
    aplicar_estilo_recursivo(root, bg, fg)
    barra_titulo.config(background="#1f6857", foreground=fg)
#-----------------------------------------------------------------------------------------------------------


def funcion_modificar (frame_ab, frame_modificacion): 
    #Escondemos el frame de altas y bajas
    frame_ab.grid_forget()

    #Colocamos el frame de modificaciones
    frame_modificacion.grid(row=1, column=0)

    configurar_menu_modificar()

def funcion_consultar(frame_ab, frame_consulta):
    #Escondemos el frame de altas y bajas
    frame_ab.grid_forget()

    #Colocamos el frame de consultas
    frame_consulta.grid(row=1, column=0)

    configurar_menu_consulta()

def funcion_volver_menu_principal(frame_modificacion, frame_consulta, frame_ab, tree_consulta, tree):
    #Escondemos los frames de modificaciones y consultas 
    frame_modificacion.grid_forget()
    frame_consulta.grid_forget()

    #Escondemos el árbol de consultas
    tree_consulta.grid_forget()

    #Colocamos el frame de altas y bajas
    frame_ab.grid(row=1, column=0, sticky="nsew") 
    
    #Colocamos el árbol original
    tree.grid(row=6, column=0, columnspan=4, sticky="nsew")

    #Recorremos los elementos del árbol del 'menu consulta' y los eliminamos con el fin de dejarlo vacío
    for i in tree_consulta.get_children():
        tree_consulta.delete(i)

#--------------------------------INTERFAZ Y NAVEGACIÓN---------------------------
def menu_principal(frame_ab, frame_consulta, frame_modificacion, tree, tree_consulta, root, var_categoria, var_descripcion, var_impacto, con):
    
    global barra_titulo

    #Creamos la barra de título del menú principal y la colocamos dentro de nuestro frame de altas y bajas.
    barra_titulo = Label(frame_ab, text="Analizador de Impacto Ambiental", background="#46dab7", foreground="black", font=("Arial", 14, "bold"))
    barra_titulo.grid(row=0, column=0,columnspan=10, sticky="we") 

    #Creamos las etiquetas para la categoría, descripción e impacto y los colocamos dentro de nuestro frame de altas y bajas.
    etiqueta_categoria = Label(frame_ab, text="Categoría:") 
    etiqueta_categoria.grid(row=1, column=0, sticky = E) 
    etiqueta_descripcion = Label(frame_ab, text="Descripción:") 
    etiqueta_descripcion.grid(row=1, column=2, sticky = E) 
    etiqueta_impacto = Label(frame_ab, text="Impacto:") 
    etiqueta_impacto.grid(row=1, column=4, sticky = E)

    #Creamos el campo de entrada con opciones prefijadas para categoría y lo colocamos en el frame de altas y bajas.
    entry_valor = ttk.Combobox(frame_ab, textvariable=var_categoria, width=15, state="readonly")
    entry_valor['values'] = ("Físico", "Biológico", "Socioeconómico")
    entry_valor.grid(row=1, column=1, sticky = W)

    #Creamos el campo de entrada de descipción y lo colocamos en el frame.
    entry_descripcion = Entry(frame_ab, textvariable=var_descripcion, width=25)
    entry_descripcion.grid(row=1, column=3, sticky = W) 
    
    #Creamos el campo de entrada con opciones prefijadas para valor de impacto y lo colocamos en el frame de altas y bajas.
    entry_valor = ttk.Combobox(frame_ab, textvariable=var_impacto, width=3, state="readonly")
    entry_valor['values'] = (-1, 0, 1)
    entry_valor.grid(row=1, column=5, sticky = W)

    #Creamos y colocamos los cuatro botones del CRUD y dos botones mas para calcular el total y el promedio
    boton_g = Button(frame_ab, text="Guardar", command = lambda: funcion_guardar()) 
    boton_g.grid(row=1, column=7, sticky="ew", padx=2)
    boton_d = Button(frame_ab, text="Borrar", command = lambda: funcion_borrar())
    boton_d.grid(row=2, column=7, sticky="ew", padx=2)
    boton_m = Button(frame_ab, text="Modificar", command = lambda: funcion_modificar())
    boton_m.grid(row=1, column=8, sticky="ew", padx=2)
    boton_c = Button(frame_ab, text="Consultar", command = lambda: funcion_consultar())
    boton_c.grid(row=2, column=8, sticky="ew", padx=2)
    boton_t = Button(frame_ab, text="Total", command = lambda: funcion_total())
    boton_t.grid(row=1, column=9, sticky="ew", padx=2)
    boton_p = Button(frame_ab, text="Promedio", command = lambda: funcion_promedio())
    boton_p.grid(row=2, column=9, sticky="ew", padx=2)
    
    #Creamos el objeto 'menu desplegable' (barra horizontal) en la ventana principal (root), donde colocaremos nuestros botones.
    menu_desplegable = Menu(root) 
    #config se utiliza para configurar opciones de la ventana principal, en este caso se establece el menú principal de la aplicación con el menú que hemos creado
    root.config(menu=menu_desplegable) 
    
    #Creamos el menu de 'Archivo', hacemos que al clickear en él se desplieguen el botón 'Copiar' y el botón 'Salir'
    menu_archivo = Menu(menu_desplegable, tearoff=0) 
    menu_archivo.add_command(label="Copiar", command=copiar_fila)
    menu_archivo.add_separator() #Añadimos un separador entre el botón 'Copiar' y el botón 'Salir'
    menu_archivo.add_command(label="Salir", command=al_cerrar)
    menu_desplegable.add_cascade(label="Archivo", menu=menu_archivo) #Hacemos que se añada esta cascada al menu 'menu desplegable'

    #Creamos el menu de 'Ayuda', hacemos que al clickear en él se despliegue el botón 'Instrucciones'
    menu_ayuda = Menu(menu_desplegable, tearoff=0)
    menu_ayuda.add_command(label="Instrucciones", command=ver_instrucciones)
    menu_ayuda.add_separator() #Añadimos un separador por si en un futuro deseamos colocar mas botones
    menu_desplegable.add_cascade(label="Ayuda", menu=menu_ayuda) #Hacemos que se añada esta cascada al menu 'menu desplegable'

    #Creamos el submenu que irá dentro del menú 'menu ajustes', hacemos que al clickear en él se desplieguen el botón 'Oscuro' y el botón 'Claro'
    submenu_claro_oscuro = Menu(menu_desplegable, tearoff=0) 
    submenu_claro_oscuro.add_command(label="Oscuro", command=modo_oscuro) 
    submenu_claro_oscuro.add_separator() #Añadimos un separador entre el botón 'Oscuro' y el botón 'Claro'
    submenu_claro_oscuro.add_command(label="Claro", command=modo_claro) 

    #Creamos el menú 'menu ajustes', hacemos que al clickear en él se despliegue el botón 'Modo' y que eso nos dirija al 'submenu claro oscuro'
    menu_ajustes = Menu(menu_desplegable, tearoff=0) 
    menu_ajustes.add_cascade(label="Modo", menu=submenu_claro_oscuro)
    menu_ajustes.add_separator() #Añadimos un separador por si en un futuro deseamos colocar mas botones
    menu_desplegable.add_cascade(label="⚙", menu=menu_ajustes) #Hacemos que se añada esta cascada al menu 'menu desplegable'

def configurar_menu_modificar(frame_modificacion, var_categoria, var_descripcion, var_impacto, con):
   
    #Creamos las etiquetas para la categoría, descripción e impacto y los colocamos dentro de nuestro frame de modificaciones.
    etiqueta_categoria = Label(frame_modificacion, text="Categoría") 
    etiqueta_categoria.grid(row=0, column=0, sticky = W) 
    etiqueta_descripcion = Label(frame_modificacion, text="Descripción") 
    etiqueta_descripcion.grid(row=0, column=2, sticky = W) 
    etiqueta_impacto = Label(frame_modificacion, text="Impacto") 
    etiqueta_impacto.grid(row=0, column=4, sticky = W)

    #Creamos el campo de entrada con opciones prefijadas para categoría y lo colocamos en el frame de modificaciones.
    entry_valor = ttk.Combobox(frame_modificacion, textvariable=var_categoria, width=15, state="readonly")
    entry_valor['values'] = ("Físico", "Biológico", "Socioeconómico")
    entry_valor.grid(row=0, column=1, sticky = W)

    #Creamos el campo de entrada de descipción y lo colocamos en el frame de modificaciones.
    entry_descripcion = Entry(frame_modificacion, textvariable=var_descripcion, width=25)
    entry_descripcion.grid(row=0, column=3, sticky = W) 
    
    #Creamos el campo de entrada con opciones prefijadas para valor de impacto y lo colocamos en el frame de modificaciones.
    entry_valor = ttk.Combobox(frame_modificacion, textvariable=var_impacto, width=3, state="readonly")
    entry_valor['values'] = (-1, 0, 1)
    entry_valor.grid(row=0, column=5, sticky = W)

    #Creamos y colocamos los botones 'Actualizar' y 'Volver' 
    boton_refresh = Button(frame_modificacion, text="Actualizar", width=15, command = lambda: funcion_modificar_variables(con))
    boton_refresh.grid(row=0, column=6, sticky=E)
    boton_save = Button(frame_modificacion, text="Volver", width=15, command = lambda: funcion_volver_menu_principal)
    boton_save.grid(row=1, column=6, sticky=E)


def configurar_menu_consulta(tree, tree_consulta, frame_consulta, var_busqueda, busqueda):

    #Escondemos el árbol orginal
    tree.grid_forget()

    #Colocamos el árbol del 'menu consulta'
    tree_consulta.grid(row=5, column=0, columnspan=4, sticky="nsew")

    #Creamos la etiqueta para la búsqueda y la colocamos dentro de nuestro frame de consulta.
    etiqueta_nombre_search1 = Label(frame_consulta, text="Busque por Id, Categoría, Descripción o Impacto") 
    etiqueta_nombre_search1.grid(row=0, column=0, columnspan=2, sticky=W+E)  

    #Creamos el campo de entrada para la búsqueda y lo colocamos en el frame de consulta.
    entry_id_search = Entry(frame_consulta, textvariable=var_busqueda, width=20)
    entry_id_search.grid(row=1, column=0, columnspan=2)

    #Creamos y colocamos los botones 'Buscar' y 'Volver' 
    boton_busqueda = Button(frame_consulta, text="Buscar", width=25, command = busqueda)
    boton_busqueda.grid(row=0, column=2, columnspan=2, sticky=W+E)
    boton_menu_principal = Button(frame_consulta, text="Volver", width=25, command = funcion_volver_menu_principal)
    boton_menu_principal.grid(row=1, column=2, columnspan=2, sticky=W+E)

    #------------------------------------INICIO TKINTER---------------------------------------
def iniciar_app():

    root = Tk()
    root.title(f"Impacto Ambiental | CABA: {clima_caba()} | Gestión de Riesgos")

    #-DECLARACION DE VARIABLES
    var_categoria = StringVar()
    var_descripcion = StringVar()
    var_impacto = IntVar()
    var_busqueda = StringVar()

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
    root.protocol("WM_DELETE_WINDOW", al_cerrar)

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



    menu_principal(frame_ab, frame_consulta, frame_modificacion, tree, tree_consulta, root, var_categoria, var_descripcion, var_impacto, con)
    actualizar_tree(tree)
    root.mainloop()