


def menu_principal():
    
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
    boton_g = Button(frame_ab, text="Guardar", command = lambda: funcion_guardar(con)) 
    boton_g.grid(row=1, column=7, sticky="ew", padx=2)
    boton_d = Button(frame_ab, text="Borrar", command = lambda: funcion_borrar(con))
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
