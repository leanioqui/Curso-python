import os
import sqlite3


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

try:
    crear_tabla()
except Exception as e:
    print("Error al crear la tabla:", e)

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

#---------------------------------INICIO BASE DE DATOS-------------------------------
con = crear_base_datos()
crear_tabla(con)