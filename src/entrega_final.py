# Analizador de Impacto Ambiental - CABA
# Autores: Franco Gimenez, Fernando Gallego, Leandro Quintela

#----------------------------------------------IMPORTACIONES------------------------------------------------
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import re
import os



#-------------------------------------------------FUNCIONES------------------------------------------------------
#-----------------------------------------BEAUTIFUL SOUP & REQUESTS----------------------------------------------
def clima_caba(): #Función para obtener el clima de CABA en tiempo real

    url = "https://www.timeanddate.com/weather/@3433955" # URL del sitio de clima para Buenos Aires
    encabezados = {'User-Agent': 'Mozilla/5.0'} # Agente de usuario y cabecera para simular una solicitud desde un navegador web, 
                                            #lo que puede ayudar a evitar bloqueos por parte del sitio web

    try:
        response = requests.get(url, headers=encabezados, timeout=10) # Realiza la solicitud HTTP con un tiempo de espera de 10 segundos, pasado el tiempo de espera, se lanzará una excepción si no se recibe una respuesta del servidor
        
        if response.status_code == 200: # Verifica que la solicitud fue exitosa, el código de estado 200 indica que la página se cargó correctamente
            soup = BeautifulSoup(response.text, "html.parser") # Analiza el contenido HTML de la página 
            
            # En este sitio, la temperatura actual suele estar en un div con clase 'h2'
            # dentro de la sección de 'bk-focus'
            temp_div = soup.find('div', class_='h2') # Busca el div que contiene la temperatura actual
            # temp_div = <div class="h2">24 °C</div>
            
            if temp_div:
                # .strip() limpia espacios en blanco y saltos de línea extra y .text extrae solo el texto dentro del div, que es la temperatura actual
                return temp_div.text.strip() # Retorna la temperatura actual en CABA
            else:
                print("No se encontró el div de temperatura. Revisá el inspector.") # Si no se encuentra el div, se sugiere revisar el inspector del navegador para verificar la estructura HTML actual del sitio
        else:
            print(f"Error de conexión: {response.status_code}") # Si la solicitud no fue exitosa, se muestra el código de estado HTTP

    except Exception as e: # Captura cualquier excepción que ocurra durante la solicitud o el análisis
        print(f"Error de raíz: {e}") # Imprime el mensaje de error en caso de que ocurra una excepción, como problemas de conexión o cambios en la estructura del sitio web
#---------------------------------------------------------------------------------------------------------------

#-------------------------------------------------FUNCIONES SQL-------------------------------------------------
def crear_base_datos():
    # Buscamos la carpeta exacta donde está guardado este archivo .py
    carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
    
    # Creamos la ruta completa uniendo la carpeta con el nombre del archivo .db
    ruta_db = os.path.join(carpeta_del_script, "base_datos.db")
    
    # Ahora siempre se conectará/creará en el lugar correcto (dentro de src/)
    con = sqlite3.connect(ruta_db)
    return con

def crear_tabla(con): 
    cursor = con.cursor() #Crea un cursor para ejecutar comandos SQL en la base de datos
    sql = "CREATE TABLE IF NOT EXISTS empresa (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, descripcion TEXT, impacto INTEGER)" #Define la consulta SQL para crear una tabla llamada "empresa" con cuatro columnas: id, categoría, descripción e impacto  
    cursor.execute(sql) #Ejecuta la consulta SQL para crear la tabla en la base de datos
    con.commit() #Guarda los cambios realizados en la base de datos

def alta_de_registro(con, categoria, desc, impacto): 
    cursor = con.cursor()
    sql = "INSERT INTO empresa (categoria, descripcion, impacto) VALUES (?, ?, ?);" #Define la consulta SQL para insertar un registro en la tabla "empresa"
    data = (categoria, desc, impacto) #Crea una tupla llamada "data" que contiene los valores de categoría, descripción e impacto que se van a insertar en la tabla "empresa".
    cursor.execute(sql, data)
    con.commit()

def baja_de_registro(con, mi_id): 
    cursor = con.cursor()
    sql = "DELETE FROM empresa WHERE id = ?;" #Define la consulta SQL para eliminar un registro de la tabla "empresa"
    data = (mi_id,) #Crea una tupla con la id del registro a eliminar
    cursor.execute(sql, data)
    con.commit()

def actualizar(con, mi_id, categoria, desc, impacto): 
    cursor = con.cursor()
    sql = "UPDATE empresa SET categoria = ?, descripcion = ?, impacto = ? WHERE id = ?;" #Define la consulta SQL para actualizar un registro en la tabla "empresa"
    data = (categoria, desc, impacto, mi_id)
    cursor.execute(sql, data)
    con.commit()

def seleccionar(con, mi_id): #Selecciona un elemento de la base de datos
    cursor = con.cursor()
    sql = "SELECT * FROM empresa WHERE id = ?;" #Define la consulta SQL para seleccionar un registro de la tabla "empresa"
    data = (mi_id,)
    cursor.execute(sql, data)
    con.commit()

#--------------------------------ESTILO-----------------------------------------
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

#---------------------------FUNCIONES CONTROL DE DATOS--------------------------
#-GESTION DE DATOS
def actualizar_tree(con):
    tabla_tree = tree.get_children() #Obtiene una lista de los identificadores de los elementos que se encuentran en el nivel superior del árbol.
    for  fila in tabla_tree: #Recorre cada fila del Treeview.
        tree.delete(fila) #Elimina la fila del Treeview.
    
    cursor = con.cursor() #Crea un cursor para ejecutar comandos SQL en la base de datos
    sql = "SELECT * FROM empresa ORDER BY id DESC;" #Define la consulta SQL para seleccionar todos los registros ordenados por id en orden ascendente
    
    tabla = cursor.execute(sql) #Ejecuta la conuslta.
    tabla2 = tabla.fetchall() #Devuelve una lista con todas las filas resultantes de la consulta.

    for fila in tabla2: #Inserta los datos en el Treewiev.
        tree.insert("", "end", text=str(fila[0]), values=(fila[1], fila[2], fila[3]))

def busqueda():
    # 1. Limpiamos el árbol de resultados
    for i in tree_consulta.get_children():
        tree_consulta.delete(i)

    # 2. Obtenemos el texto a buscar
    termino = var_busqueda.get().lower()

    # 3. Filtramos desde el árbol original
    for item in tree.get_children():
        valores = tree.item(item).get("values")
        id_fila = tree.item(item).get("text")
        
        # Comparamos (Windows style: búsqueda parcial)
        if termino in str(id_fila) or termino in str(valores[0]).lower() or termino in str(valores[1]).lower() or termino in str(valores[2]).lower():
            # Insertamos en el árbol de consulta lo encontrado
            tree_consulta.insert("", "end", text=id_fila, values=valores) 

def funcion_guardar(con): 
    filtro = re.compile(r'\D') #Crea un patrón de expresión regular que se usará para buscar caracteres no numéricos en el texto.
    descripcion = str(var_descripcion.get()) #Obtiene el texto, se asegura que el valor sea una cadena y lo guarda en la variable local.
    if var_categoria.get() != "" and var_descripcion.get() != "" and var_impacto.get() != "": #Validación inicial de los campos.
        if (re.match(filtro, descripcion) == None): #Validación con la expresión regular.
            messagebox.showerror("Error", "Ingrese una descripción válida. No se permite iniciar con un caracter numérico.") #Mensaje de error si la descripcion inicia con un caracter numérico.
        else: #Guardar en el registro y actualizar el Treeview.
            alta_de_registro(con, var_categoria.get(), var_descripcion.get(), var_impacto.get())
            actualizar_tree(con)
            var_descripcion.set("")

    elif var_categoria.get().strip() == "" and var_descripcion.get().strip() == "": #Validación si los campos categoria y descripcion no estan vacios.
        messagebox.showerror("Error", "Debe ingresar una categoría y una descripción.") #Mensaje de error si los campos categoria y descripcion estan vacios.
        return

    elif var_categoria.get().strip() == "": #Validación si el campo categoria no esta vacio.
        messagebox.showerror("Error", "Debe ingresar una categoría.") #Mensaje de error si el campo categoria esta vacio.
        return
    
    elif var_descripcion.get().strip() == "": #Validación si el campo descripción no esta vacio.
        messagebox.showerror("Error", "Debe ingresar una descripción.") #Mensaje de error si el campo descripción esta vacio.
        return

def funcion_borrar(con):

    cursor = con.cursor() #Crear cursos de base de datos.
    item_seleccionado = tree.selection() #Obtener items seleccionados del Treeview
    if not item_seleccionado:
        messagebox.showerror("Error", "Debe seleccionar un registro para borrar.") #Mensaje de error si el item no esta seleccionado al intentar borrar.
        return
    if item_seleccionado:
        for i in item_seleccionado: #Reccorrer cada item seleccionado.
            mi_id = tree.item(i).get("text") #Obtener el id asociado al item.
            tree.delete(i) #Elimina la fila del Treeview.
            baja_de_registro(con, mi_id) #Elimina el registro d ela base de datos.

def funcion_modificar_variables(con):
    filtro = re.compile(r'\D') #Crea un patrón de expresión regular que se usará para buscar caracteres no numéricos en el texto.
    descripcion = str(var_descripcion.get()) #Obtiene el texto, se asegura que el valor sea una cadena y lo guarda en la variable local.
    item_seleccionado = tree.focus() #Obtiene el ítem enfocado en el Treeview.
    if not item_seleccionado:
        messagebox.showerror("Error", "Debe seleccionar un registro para modificar.") #Mensaje de error si no hay lista seleccionada.
    else:
        if var_categoria.get().strip() == "" and var_descripcion.get().strip() == "":
            messagebox.showerror("Error", "Debe ingresar una categoría y una descripción.") #Mensaje de error si los campos categoria y descripcion estan vacios.
            return
        if var_categoria.get().strip() == "":
            messagebox.showerror("Error", "Debe ingresar una categoría.") #Mensaje de error si el campo categoria esta vacio.
            return
        if var_descripcion.get().strip() == "":
            messagebox.showerror("Error", "Debe ingresar una descripción.") #Mensaje de error si el campo descripción esta vacio.
            return
        if re.match(filtro, descripcion): #Validación con la expresión regular.
            tree.item(item_seleccionado, values=(var_categoria.get(), var_descripcion.get(), var_impacto.get())) #Validación inicial de los campos.
            mi_id = tree.item(item_seleccionado).get("text") #Obtener el id del registro.
            actualizar(con, mi_id, var_categoria.get(), var_descripcion.get(), var_impacto.get()) #Actualiza el registro en la base de datos.
        else:
            messagebox.showerror("Error", "No se permite iniciar la descripción con caracteres numéricos.") #Mensaje de error si la descripcion inicia con un caracter numérico.
            return

#-CALCULOS E INFORMACION
def ver_instrucciones():
    mensaje = ( #Contiene la informacion de la ventana de ayuda
        "Instrucciones para realizar el analisis de impacto ambiental de su proyecto:\n"
        "\n"
        "1. Complete los campos de 'Categoría', 'Descripción' e 'Impacto'.\n"
        "\n"
            "-Categoría: Se dividen en Físico, Biológico y Socioeconómico.\n"
            "\n"
            "-Descripción: Detalle del parámetro ambiental especifico afectado por la actividad. \n"
            " No se permiten caracteres numéricos al inicio de la descripción.\n"
            "\n"
            "-Impacto: Valor del impacto ambiental; cuyos valores de referencia son:\n"
                      "Para impactos negativos: -1\n"
                      "Para impactos positivos: 1\n"
                      "Para impactos neutros: 0\n"
            "Solo puede ingresar valores dentro de ese rango\n"
            "\n"
        "2. Use el boton 'Guardar' para agregar la entrada a la base de datos.\n"
        "\n"
        "3. De ser necesario puede Borrar, Modificar o Consultar una entrada en particular pulsando los respectivos botones.\n"
        "\n"
        "4. Use el boton 'Total' para obtener el valor total del impacto ambiental de su proyecto.\n"
        "\n"
        "5. Use el boton 'Promedio' para obtener un promedio del impacto ambiental de su proyecto.\n"
        "\n"
        "Menores valores indican un mayor impacto negativo sobre el ambiente, mientras que valores mayores indican un impacto positivo."
    )
    messagebox.showinfo("Instrucciones del programa", mensaje)

def funcion_total():
    total = 0 #Inicia la variable total en 0.
    for item in tree.get_children(): #Devuelve una lista de los identificadores de los elementos hijos del widget Treeview.
        valores = tree.item(item, "values") #Se utiliza para obtener los valores de un elemento específico del widget Treeview.
        total += int(valores[2]) #Toma el valor de la tercera columna, que corresponde al impacto, lo convierte a entero y lo suma al acumulador.

    messagebox.showinfo("Total del Impacto", f"El valor total del impacto ambiental es: {total}") #Mostrar venetana emergente con el resultado total.

def funcion_promedio():
    total = 0 #Inicia la variable total en 0.
    promedio = 0 #Inicia la variable promedio en 0.
    contador = 0 #Inicia la variable contador en 0.
    for item in tree.get_children(): #Devuelve una lista de los identificadores de los elementos hijos del widget Treeview.     
        valores = tree.item(item, "values") #Se utiliza para obtener los valores de un elemento específico del widget Treeview.
        total += int(valores[2]) #Toma el valor de la tercera columna, que corresponde al impacto, lo convierte a entero y lo suma al acumulador.
        if int(valores[2]) != 0: #Para que los valores neutros no afecten al promedio (no se suman al contador).
            contador += 1
    if total != 0:
        promedio = round(total / contador, 2) #Aplica la fórmula para obtener el promedio de impacto de nuestra Base de Datos.   
    messagebox.showinfo("Promedio de impacto", f"El valor promedio del impacto ambiental es: {promedio}") #Mostrar venetana emergente con el valor promedio.

def copiar_fila(): #Permite copiar la/las filas seleccionadas
    seleccion = tree.selection()

    if not seleccion: #Verifica si hay al menos una fila seleccionada
        messagebox.showerror("Error", "Debe seleccionar una o más filas para copiar.")
        return
    texto = "" #Inicia una variable donde se irá acumulando el texto que se copiará al portapapeles.
    for item in seleccion:
        valores = tree.item(item, "values")
        texto += f"{valores[0]}\t{valores[1]}\t{valores[2]}\n" #Construye una línea de texto con los valores de la fila.

    root.clipboard_clear() #Limpia el portapapeles del sistema operativo.
    root.clipboard_append(texto) #Copia el texto generado al portapapeles.

def al_cerrar():
    # 1. Acción personalizada (ej: preguntar si está seguro)
    if messagebox.askokcancel("Salir", "¿Deseas cerrar el programa?"):  #askokcancel muestra un cuadro de diálogo con opciones "OK" y "Cancelar". 
                                                                        #Devuelve True si el usuario hace clic en "OK" y False si hace clic en "Cancelar".
        # 2. Cerrar recursos (Base de datos)
        con.close() 
        print("Conexión cerrada. Saliendo...")
        # 3. Destruir la ventana manualmente
        root.destroy()

#--------------------------------INTERFAZ Y NAVEGACIÓN---------------------------
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

def configurar_menu_modificar():
   
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
    boton_save = Button(frame_modificacion, text="Volver", width=15, command = lambda: funcion_volver_menu_principal())
    boton_save.grid(row=1, column=6, sticky=E)

def configurar_menu_consulta():
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

def funcion_modificar (): 
    #Escondemos el frame de altas y bajas
    frame_ab.grid_forget()

    #Colocamos el frame de modificaciones
    frame_modificacion.grid(row=1, column=0)

    configurar_menu_modificar()

def funcion_consultar():
    #Escondemos el frame de altas y bajas
    frame_ab.grid_forget()

    #Colocamos el frame de consultas
    frame_consulta.grid(row=1, column=0)

    configurar_menu_consulta()

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

#---------------------------------INICIO BASE DE DATOS-------------------------------
con = crear_base_datos()
crear_tabla(con)

#------------------------------------INICIO TKINTER---------------------------------------
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


actualizar_tree(con)
menu_principal()
root.mainloop()