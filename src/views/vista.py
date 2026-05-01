

def aplicar_estilo_recursivo(root, color_botones, color_letra): #Esta funcion aplica colores de fondo y texto a todos los widgets de la interfaz de manera recursiva
    for w in root.winfo_children(): #winfo_children() devuelve una lista de todos los widgets hijos directos del widget root, 
                                    # es decir, los widgets que están contenidos dentro de root.
        try: w.configure(bg=color_botones, fg=color_letra) # Intenta pintar fondo y letra
        except: 
            try: w.configure(bg=color_botones)    # Si no tiene letra (como Frames), solo fondo
            except: pass
        aplicar_estilo_recursivo(w, color_botones, color_letra) # Sigue con los hijos

def modo_claro(): #Funcion que define los colores del Modo Claro
    style = ttk.Style()
    style.theme_use('vista')
    root.config(bg="SystemButtonFace") #SystemButtonFace es el color de fondo predeterminado de los botones en Windows, 
                                        #al usarlo como fondo para la ventana principal, se logra un aspecto más claro y consistente con el tema clásico de Windows.
    aplicar_estilo_recursivo(root, "SystemButtonFace", "black") #Pinta fondo y letra de todos los widgets, 
                                                                #el fondo se pinta con el color predeterminado del sistema para botones (SystemButtonFace) 
                                                                # y la letra se pinta de negro
    barra_titulo.config(background="#46dab7", foreground="black")

def modo_oscuro(): #Funcion que define los colores del Modo Oscuro
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

def funcion_volver_menu_principal():
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