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

#---------------------------------INICIO BASE DE DATOS-------------------------------
try:
    con = crear_base_datos()
except Exception as e:
    print("Error al crear la base de datos:", e)

def crear_tabla(con): 
    cursor = con.cursor() #Crea un cursor para ejecutar comandos SQL en la base de datos
    sql = "CREATE TABLE IF NOT EXISTS empresa (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, descripcion TEXT, impacto INTEGER)" #Define la consulta SQL para crear una tabla llamada "empresa" con cuatro columnas: id, categoría, descripción e impacto  
    cursor.execute(sql) #Ejecuta la consulta SQL para crear la tabla en la base de datos
    con.commit() #Guarda los cambios realizados en la base de datos

try:
    crear_tabla(con)
except Exception as e:
    print("Error al crear la tabla:", e)

def alta_de_registro(categoria, desc, impacto): 
    con = crear_base_datos()
    cursor = con.cursor()
    sql = "INSERT INTO empresa (categoria, descripcion, impacto) VALUES (?, ?, ?);" #Define la consulta SQL para insertar un registro en la tabla "empresa"
    data = (categoria, desc, impacto) #Crea una tupla llamada "data" que contiene los valores de categoría, descripción e impacto que se van a insertar en la tabla "empresa".
    cursor.execute(sql, data)
    con.commit()
    con.close()

def baja_de_registro(mi_id):
    con = crear_base_datos() 
    cursor = con.cursor()
    sql = "DELETE FROM empresa WHERE id = ?;" #Define la consulta SQL para eliminar un registro de la tabla "empresa"
    data = (mi_id,) #Crea una tupla con la id del registro a eliminar
    cursor.execute(sql, data)
    con.commit()
    con.close()

def actualizar(mi_id, categoria, desc, impacto): 
    con = crear_base_datos()
    cursor = con.cursor()
    sql = "UPDATE empresa SET categoria = ?, descripcion = ?, impacto = ? WHERE id = ?;" #Define la consulta SQL para actualizar un registro en la tabla "empresa"
    data = (categoria, desc, impacto, mi_id)
    cursor.execute(sql, data)
    con.commit()
    con.close()

def seleccionar(mi_id): #Selecciona un elemento de la base de datos
    con = crear_base_datos()
    cursor = con.cursor()
    sql = "SELECT * FROM empresa WHERE id = ?;" #Define la consulta SQL para seleccionar un registro de la tabla "empresa"
    data = (mi_id,)
    cursor.execute(sql, data)
    con.commit()
    con.close()

def consultar_todos():
    cursor = con.cursor() #Crea un cursor para ejecutar comandos SQL en la base de datos
    sql = "SELECT * FROM empresa ORDER BY id DESC;" #Define la consulta SQL para seleccionar todos los registros ordenados por id en orden ascendente
    
    tabla = cursor.execute(sql) #Ejecuta la conuslta.
    tabla2 = tabla.fetchall() #Devuelve una lista con todas las filas resultantes de la consulta.
    con.close()
    return tabla2