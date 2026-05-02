import sqlite3
import os

class Modelo:
    def __init__(self):
        self.con = self.crear_base_datos()
        self.crear_tabla()
    
    def crear_base_datos(self):
        # Buscamos la carpeta exacta donde está guardado este archivo .py
        carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
        
        # Creamos la ruta completa uniendo la carpeta con el nombre del archivo .db
        ruta_db = os.path.join(carpeta_del_script, "base_datos.db")
        
        # Ahora siempre se conectará/creará en el lugar correcto (dentro de src/)
        con = sqlite3.connect(ruta_db)
        return con

    def crear_tabla(self): 
        cursor = self.con.cursor() #Crea un cursor para ejecutar comandos SQL en la base de datos
        sql = "CREATE TABLE IF NOT EXISTS empresa (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, descripcion TEXT, impacto INTEGER)" #Define la consulta SQL para crear una tabla llamada "empresa" con cuatro columnas: id, categoría, descripción e impacto  
        cursor.execute(sql) #Ejecuta la consulta SQL para crear la tabla en la base de datos
        self.con.commit() #Guarda los cambios realizados en la base de datos

    def alta_de_registro(self, categoria, desc, impacto): 
        cursor = self.con.cursor()
        sql = "INSERT INTO empresa (categoria, descripcion, impacto) VALUES (?, ?, ?);" #Define la consulta SQL para insertar un registro en la tabla "empresa"
        data = (categoria, desc, impacto) #Crea una tupla llamada "data" que contiene los valores de categoría, descripción e impacto que se van a insertar en la tabla "empresa".
        cursor.execute(sql, data)
        self.con.commit()

    def baja_de_registro(self, mi_id): 
        cursor = self.con.cursor()
        sql = "DELETE FROM empresa WHERE id = ?;" #Define la consulta SQL para eliminar un registro de la tabla "empresa"
        data = (mi_id,) #Crea una tupla con la id del registro a eliminar
        cursor.execute(sql, data)
        self.con.commit()

    def actualizar(self, categoria, desc, impacto, mi_id): 
        cursor = self.con.cursor()
        sql = "UPDATE empresa SET categoria = ?, descripcion = ?, impacto = ? WHERE id = ?;" #Define la consulta SQL para actualizar un registro en la tabla "empresa"
        data = (categoria, desc, impacto, mi_id)
        cursor.execute(sql, data)
        self.con.commit()

    def consultar_todos(self):
        cursor = self.con.cursor() #Crea un cursor para ejecutar comandos SQL en la base de datos
        sql = "SELECT * FROM empresa ORDER BY id DESC;" #Define la consulta SQL para seleccionar todos los registros ordenados por id en orden ascendente
        
        tabla = cursor.execute(sql) #Ejecuta la conuslta.
        tabla2 = tabla.fetchall() #Devuelve una lista con todas las filas resultantes de la consulta.
        return tabla2
    
    def cerrar_base(self):
        self.con.close()