"""
controlador.py:
Este módulo define la clase Controlador, que se encarga de manejar la lógica de la aplicación y de interactuar con la base de datos a través del modelo, así como de manejar las acciones de la interfaz gráfica a través de la vista.
Además, incluye funciones para realizar cálculos relacionados con el impacto ambiental y para obtener información en tiempo real, como el clima de CABA.
"""

from .mis_regex import MisRegex
import requests
from tkinter import messagebox
from bs4 import BeautifulSoup
from models.modelo import Modelo
import re

class Error(Exception): 
    pass

class CarNumError(Error):
    def __init__(self):
        super().__init__("Error: Ingrese una descripción válida. No se permite iniciar con un caracter numérico.")

class CatDescError(Error):
    def __init__(self):
        super().__init__("Error: Debe ingresar una categoría y una descripción.")

class CatError(Error):
    def __init__(self):
        super().__init__("Error: Debe ingresar una categoría.")    
class DescError(Error):
    def __init__(self):
        super().__init__("Error: Debe ingresar una descripción.")

class Controlador():
    def __init__(self):
        """
        Constructor de la clase Controlador. Inicializa la conexión con el componente 
        del modelo para la persistencia y gestión de los datos del sistema.
        
        :return: No devuelve ningún valor.
        :rtype: None
        """
        self.modelo = Modelo()
        

    def actualizar_tree(self, tree):
        """
        Limpia todas las filas actuales del widget Treeview e inserta los datos
        actualizados obtenidos desde la base de datos a través del modelo.

        :param tree: El widget de la interfaz gráfica que muestra los datos en formato de tabla.
        :type tree: ttk.Treeview
        :return: No devuelve ningún valor.
        :rtype: None
        """
        tabla_tree = tree.get_children() #Obtiene una lista de los identificadores de los elementos que se encuentran en el nivel superior del árbol.
        for  fila in tabla_tree: #Recorre cada fila del Treeview.
            tree.delete(fila) #Elimina la fila del Treeview.
        
        tabla = self.modelo.consultar_todos()

        for fila in tabla: #Inserta los datos en el Treewiev.
            tree.insert("", "end", text=str(fila[0]), values=(fila[1], fila[2], fila[3]))

    def funcion_busqueda(self, vista):
        """
        Busca un término de texto en las columnas del Treeview principal y filtra
        los resultados coincidentes, insertándolos en el Treeview de consultas.

        :param vista: La instancia de la interfaz gráfica que contiene los widgets y variables de búsqueda.
        :type vista: tk.Toplevel o tk.Tk
        :return: No devuelve ningún valor.
        :rtype: None
        """
        # 1. Limpiamos el árbol de resultados
        for i in vista.tree_consulta.get_children():
            vista.tree_consulta.delete(i)

        # 2. Obtenemos el texto a buscar
        termino = vista.var_busqueda.get().lower()

        # 3. Filtramos desde el árbol original
        for item in vista.tree.get_children():
            valores = vista.tree.item(item).get("values")
            id_fila = vista.tree.item(item).get("text")
            
            # Comparamos (Windows style: búsqueda parcial)
            if termino in str(id_fila) or termino in str(valores[0]).lower() or termino in str(valores[1]).lower() or termino in str(valores[2]).lower():
                # Insertamos en el árbol de consulta lo encontrado
                vista.tree_consulta.insert("", "end", text=id_fila, values=valores) 
        
    def funcion_guardar(self, vista): 
        """
        Valida las entradas de la interfaz de usuario mediante expresiones regulares 
        y excepciones personalizadas, y da de alta el registro en la base de datos.

        :param vista: La instancia de la interfaz gráfica que contiene las variables y el Treeview.
        :type vista: tk.Toplevel o tk.Tk
        :return: No devuelve ningún valor.
        :rtype: None
        """
        filtro = MisRegex()
        cat = vista.var_categoria.get().strip()
        desc = vista.var_descripcion.get().strip()
        imp = vista.var_impacto.get()
        try:
            # 1. Validaciones (Lanzamos el error apenas detectamos el fallo)
            if not cat and not desc: 
                raise CatDescError()
            
            if not cat: 
                raise CatError()
            
            if not desc: 
                raise DescError()
            
            if re.match(filtro.solo_letras(), desc) is None: 
                raise CarNumError()

            # 2. Si todo está bien, guardamos
            self.modelo.alta_de_registro(cat, desc, imp)
            self.actualizar_tree(vista.tree)
            vista.var_descripcion.set("")

        except Error as e: 
            # Capturamos cualquiera de TUS errores aquí
            messagebox.showerror("Error", str(e))
            print(e) # Usamos el objeto que ya existe

    def funcion_borrar(self, tree):
        """
        Obtiene los elementos seleccionados en el Treeview, valida que exista al menos 
        una selección y elimina los registros tanto de la interfaz gráfica como de la base de datos.

        :param tree: El widget de la interfaz gráfica desde donde se realiza la selección.
        :type tree: ttk.Treeview
        :return: No devuelve ningún valor.
        :rtype: None
        """
        item_seleccionado = tree.selection() #Obtener items seleccionados del Treeview
        if not item_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un registro para borrar.") #Mensaje de error si el item no esta seleccionado al intentar borrar.
            return
        if item_seleccionado:
            for i in item_seleccionado: #Reccorrer cada item seleccionado.
                mi_id = tree.item(i).get("text") #Obtener el id asociado al item.
                tree.delete(i) #Elimina la fila del Treeview.
                self.modelo.baja_de_registro(mi_id) #Elimina el registro d ela base de datos.

    def funcion_modificar_variables(self, vista):
        """
        Valida los campos de entrada mediante expresiones regulares y lógica condicional,
        y actualiza los datos del registro seleccionado tanto en el Treeview como en la base de datos.

        :param vista: La instancia de la interfaz gráfica que contiene los widgets, variables y el Treeview.
        :type vista: tk.Toplevel o tk.Tk
        :return: No devuelve ningún valor.
        :rtype: None
        """
        filtro = re.compile(r'\D') #Crea un patrón de expresión regular que se usará para buscar caracteres no numéricos en el texto.
        descripcion = str(vista.var_descripcion.get()) #Obtiene el texto, se asegura que el valor sea una cadena y lo guarda en la variable local.
        item_seleccionado = vista.tree.focus() #Obtiene el ítem enfocado en el Treeview.
        if not item_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un registro para modificar.") #Mensaje de error si no hay lista seleccionada.
        else:
            if vista.var_categoria.get().strip() == "" and vista.var_descripcion.get().strip() == "":
                messagebox.showerror("Error", "Debe ingresar una categoría y una descripción.") #Mensaje de error si los campos categoria y descripcion estan vacios.
                return
            if vista.var_categoria.get().strip() == "":
                messagebox.showerror("Error", "Debe ingresar una categoría.") #Mensaje de error si el campo categoria esta vacio.
                return
            if vista.var_descripcion.get().strip() == "":
                messagebox.showerror("Error", "Debe ingresar una descripción.") #Mensaje de error si el campo descripción esta vacio.
                return
            if re.match(filtro, descripcion): #Validación con la expresión regular.
                vista.tree.item(item_seleccionado, values=(vista.var_categoria.get(), vista.var_descripcion.get(), vista.var_impacto.get())) #Validación inicial de los campos.
                mi_id = vista.tree.item(item_seleccionado).get("text") #Obtener el id del registro.
                self.modelo.actualizar(mi_id, vista.var_categoria.get(), vista.var_descripcion.get(), vista.var_impacto.get()) #Actualiza el registro en la base de datos.
            else:
                messagebox.showerror("Error", "No se permite iniciar la descripción con caracteres numéricos.") #Mensaje de error si la descripcion inicia con un caracter numérico.
                return

    #-CALCULOS E INFORMACION
    def ver_instrucciones(self, vista):
        """
        Genera y despliega una ventana emergente de información con el manual de usuario,
        los rangos de referencia de impacto y las pautas operativas del sistema.

        :param vista: La instancia de la interfaz gráfica desde la cual se invoca la ventana de ayuda.
        :type vista: tk.Toplevel o tk.Tk
        :return: No devuelve ningún valor.
        :rtype: None
        """
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

    def funcion_total(self, tree):
        """
        Recorre todos los elementos activos en el Treeview, extrae los valores numéricos
        de la columna de impactos y despliega un cuadro de diálogo con el valor acumulado total.

        :param tree: El widget de la interfaz gráfica que contiene las filas con los valores de impacto.
        :type tree: ttk.Treeview
        :return: No devuelve ningún valor.
        :rtype: None
        """
        total = 0 #Inicia la variable total en 0.
        for item in tree.get_children(): #Devuelve una lista de los identificadores de los elementos hijos del widget Treeview.
            valores = tree.item(item, "values") #Se utiliza para obtener los valores de un elemento específico del widget Treeview.
            total += int(valores[2]) #Toma el valor de la tercera columna, que corresponde al impacto, lo convierte a entero y lo suma al acumulador.

        messagebox.showinfo("Total del Impacto", f"El valor total del impacto ambiental es: {total}") #Mostrar venetana emergente con el resultado total.

    def funcion_promedio(self, tree):
        """
        Calcula el promedio de los impactos ambientales activos en el Treeview,
        excluyendo de la muestra estadística aquellos valores considerados neutros (0),
        y despliega un cuadro de diálogo con el resultado redondeado a dos decimales.

        :param tree: El widget de la interfaz gráfica que contiene las filas con los datos de impacto.
        :type tree: ttk.Treeview
        :return: No devuelve ningún valor.
        :rtype: None
        """
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

    def copiar_fila(self, tree, root): #Permite copiar la/las filas seleccionadas
        """
        Obtiene los elementos seleccionados en el Treeview, concatena sus valores 
        en formato de texto separado por tabulaciones y los transfiere al portapapeles del sistema.

        :param tree: El widget de la interfaz gráfica desde donde se extrae la selección de filas.
        :type tree: ttk.Treeview
        :param root: La ventana o instancia raíz de Tkinter requerida para interactuar con el portapapeles.
        :type root: tk.Tk o tk.Toplevel
        :return: No devuelve ningún valor.
        :rtype: None
        """
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
   
    def al_cerrar(self, root):
        """
        Gestiona el evento de cierre de la aplicación, solicitando confirmación al usuario
        y asegurando la correcta desconexión de la base de datos antes de destruir la ventana principal.

        :param root: La ventana o instancia raíz de Tkinter que se va a destruir para finalizar el programa.
        :type root: tk.Tk o tk.Toplevel
        :return: No devuelve ningún valor.
        :rtype: None
        """
        # 1. Acción personalizada (ej: preguntar si está seguro)
        if messagebox.askokcancel("Salir", "¿Deseas cerrar el programa?"):  #askokcancel muestra un cuadro de diálogo con opciones "OK" y "Cancelar". 
                                                                            #Devuelve True si el usuario hace clic en "OK" y False si hace clic en "Cancelar".
            # 2. Cerrar recursos (Base de datos)
            self.modelo.cerrar_base()
            print("Conexión cerrada. Saliendo...")
            # 3. Destruir la ventana manualmente
            root.destroy()

    def clima_caba(self): #Función para obtener el clima de CABA en tiempo real
        """
        Realiza una petición HTTP GET con cabeceras personalizadas a un proveedor externo
        de clima y parsea el árbol HTML para extraer la temperatura actual de CABA.

        :return: La cadena de texto con la temperatura actual (ej: "24 °C") si la extracción es exitosa, o None en caso de error.
        :rtype: str o None
        """
        url = "https://www.timeanddate.com/weather/@3433955" # URL del sitio de clima para Buenos Aires
        encabezados = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Referer': 'https://www.google.com/'
        } # Agente de usuario y cabecera para simular una solicitud desde un navegador web, lo que puede ayudar a evitar bloqueos por parte del sitio web

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
                print(f"Error de conexión con la Web del Clima: {response.status_code}") # Si la solicitud no fue exitosa, se muestra el código de estado HTTP

        except Exception as e: # Captura cualquier excepción que ocurra durante la solicitud o el análisis
            print(f"Error de raíz: {e}") # Imprime el mensaje de error en caso de que ocurra una excepción, como problemas de conexión o cambios en la estructura del sitio web