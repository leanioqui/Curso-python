"""
modelo.py:
Este módulo define la clase Modelo, que se encarga de manejar la lógica de la aplicación y de interactuar con la base de datos.
"""

import sqlite3
import os
import socket


# ==============================================================================
# PATRÓN OBSERVADOR: Clase que observa al Modelo y envía Logs por UDP
# ==============================================================================
class LoggerObserver:
    """
    Observador que recibe notificaciones del decorador y las envía por socket UDP
    al servidor de logs.
    """

    def __init__(self, host="localhost", port=9999):
        """
        Inicializa la instancia del observador con la dirección y puerto del servidor UDP.

        :param host: Dirección IP o nombre de host del servidor de logs.
        :type host: str
        :param port: Puerto en el que el servidor de logs escucha las conexiones.
        :type port: int
        """
        self.host = host
        self.port = port

    def actualizar(self, mensaje):
        """
        Envía un mensaje de registro formateado al servidor de logs mediante un socket UDP.

        :param mensaje: El contenido del log que se enviará al servidor.
        :type mensaje: str
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(mensaje.encode("utf-8"), (self.host, self.port))
            sock.close()
        except Exception as e:
            print(f"[LoggerObserver Error]: No se pudo enviar el log via UDP: {e}")


class Observable:
    """
    Clase base que implementa el Patrón Observador.
    Permite que los observadores se registren y reciban notificaciones de cambios.
    :type self: Observable
    """

    def __init__(self):
        """
        Inicializa la lista de observadores y suscribe automáticamente
        el observador de logs por UDP.
        """
        # Lista de observadores para el Patrón Observador
        self._observadores = []

        # Suscribimos automáticamente el observador de Logs UDP
        self.agregar_observador(LoggerObserver())

    # --- Métodos del Patrón Observador ---
    def agregar_observador(self, observador):
        """
        Agrega un nuevo observador a la lista de suscritos.

        :param observador:
        :type observador: object
        """
        self._observadores.append(observador)

    def notificar_observadores(self, mensaje):
        """
        Itera sobre todos los observadores registrados e invoca su método ``actualizar``
        pasándoles el mensaje especificado.

        :param mensaje: Mensaje o evento que se transmitirá a cada observador.
        :type mensaje: str
        """
        for obs in self._observadores:
            obs.actualizar(mensaje)


def notificar_observador(funcion):
    """
    Este decorador envuelve las funciones del Modelo que realizan cambios en la base de datos.
    Después de ejecutar la función original, construye un mensaje de log y notifica a los observadores registrados.

    - ``alta``: Registra el ID y la categoría a partir del resultado.
    - ``baja``: Registra el ID pasado como argumento.
    - ``otras acciones``: Registra la categoría, descripción, impacto e ID.

    :param funcion: La función del Modelo que se va a envolver.
    :type funcion: function
    :return: La función envuelta que notifica a los observadores después de su ejecución.
    :rtype: function
    """

    def envoltura(self, *args, **kwargs):
        resultado = funcion(self, *args, **kwargs)
        # Construimos el mensaje del log según la función ejecutada
        nombre_accion = funcion.__name__.replace("_", " ").upper()
        if "alta" in funcion.__name__:
            mensaje = f"ACCION: {nombre_accion} | ID: {resultado['id']} | Categoria: {resultado['categoria']}"
        elif "baja" in funcion.__name__:
            mensaje = f"ACCION: {nombre_accion} | ID: {args[0]}"
        else:
            mensaje = f"ACCION: {nombre_accion} | ID: {args[3]} | Categoria: {args[0]} | Descripcion: {args[1]} | Impacto: {args[2]} "

        self.notificar_observadores(mensaje)

        return resultado

    return envoltura


class Modelo(Observable):
    def __init__(self):
        super().__init__()
        self.con = self.crear_base_datos()
        self.crear_tabla()

    def crear_base_datos(self):
        """
        Este método crea o establece una conexión con la base de datos SQLite
        ubicada en la misma carpeta donde se encuentra el archivo actual.

        La función obtiene automáticamente la ruta absoluta del script en ejecución,
        genera la ruta completa del archivo ``base_datos.db`` y luego crea la conexión
        con la base de datos.

        :param self: La instancia de la clase Modelo.
        :type self: Modelo
        :return: Un objeto de conexión a la base de datos SQLite.
        :rtype: sqlite3.Connection
        """
        # Buscamos la carpeta exacta donde está guardado este archivo .py
        carpeta_del_script = os.path.dirname(os.path.abspath(__file__))

        # Creamos la ruta completa uniendo la carpeta con el nombre del archivo .db
        ruta_db = os.path.join(carpeta_del_script, "base_datos.db")

        # Ahora siempre se conectará/creará en el lugar correcto (dentro de src/)
        con = sqlite3.connect(ruta_db)
        return con

    def crear_tabla(self):
        """
        Este método crea la tabla ``empresa`` en la base de datos si todavía no existe.

        La tabla contiene cuatro columnas:

        - ``id``: identificador único autoincremental.
        - ``categoria``: categoría del registro.
        - ``descripcion``: descripción del registro.
        - ``impacto``: valor numérico asociado al impacto.

        Además, ejecuta la consulta SQL y guarda los cambios realizados
        en la base de datos.

        :param self: La instancia de la clase Modelo.
        :type self: Modelo
        """
        cursor = (
            self.con.cursor()
        )  # Crea un cursor para ejecutar comandos SQL en la base de datos
        sql = "CREATE TABLE IF NOT EXISTS empresa (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, descripcion TEXT, impacto INTEGER)"  # Define la consulta SQL para crear una tabla llamada "empresa" con cuatro columnas: id, categoría, descripción e impacto
        cursor.execute(
            sql
        )  # Ejecuta la consulta SQL para crear la tabla en la base de datos
        self.con.commit()  # Guarda los cambios realizados en la base de datos

    @notificar_observador
    def alta_de_registro(self, categoria, desc, impacto):
        """
        Este método inserta un nuevo registro en la tabla ``empresa``
        de la base de datos.

        El registro almacenará una categoría, una descripción y un valor
        de impacto asociados al nuevo elemento ingresado.

        :param self: La instancia de la clase Modelo.
        :type self: Modelo
        :param categoria: La categoría del registro a insertar.
        :type categoria: str
        :param desc: La descripción del registro.
        :type desc: str
        :param impacto: El valor numérico de impacto asociado al registro.
        :type impacto: int
        """
        cursor = self.con.cursor()
        sql = "INSERT INTO empresa (categoria, descripcion, impacto) VALUES (?, ?, ?);"  # Define la consulta SQL para insertar un registro en la tabla "empresa"
        data = (
            categoria,
            desc,
            impacto,
        )  # Crea una tupla llamada "data" que contiene los valores de categoría, descripción e impacto que se van a insertar en la tabla "empresa".
        cursor.execute(sql, data)
        self.con.commit()
        # cursor.lastrowid nos da el ID exacto que acaba de asignar SQLite automáticamente
        nuevo_id = cursor.lastrowid

        # Retornamos los datos completos (incluido el ID) para que el decorador los capture
        return {
            "id": nuevo_id,
            "categoria": categoria,
            "descripcion": desc,
            "impacto": impacto,
        }

    @notificar_observador
    def baja_de_registro(self, mi_id):
        """
        Este método elimina un registro de la tabla ``empresa``
        utilizando su identificador único.

        La eliminación se realiza mediante una consulta SQL que busca
        el registro correspondiente al ``id`` proporcionado.

        :param self: La instancia de la clase Modelo.
        :type self: Modelo
        :param mi_id: El identificador único del registro a eliminar.
        :type mi_id: int
        """
        cursor = self.con.cursor()
        sql = "DELETE FROM empresa WHERE id = ?;"  # Define la consulta SQL para eliminar un registro de la tabla "empresa"
        data = (mi_id,)  # Crea una tupla con la id del registro a eliminar
        cursor.execute(sql, data)
        self.con.commit()

    @notificar_observador
    def actualizar(self, categoria, desc, impacto, mi_id):
        """
        Este método actualiza los datos de un registro existente
        en la tabla ``empresa``.

        La actualización se realiza utilizando el identificador único
        del registro y reemplazando los valores de categoría,
        descripción e impacto por los nuevos datos proporcionados.

        :param self: La instancia de la clase Modelo.
        :type self: Modelo
        :param categoria: La nueva categoría del registro.
        :type categoria: str
        :param desc: La nueva descripción del registro.
        :type desc: str
        :param impacto: El nuevo valor de impacto del registro.
        :type impacto: int
        :param mi_id: El identificador único del registro a actualizar.
        :type mi_id: int
        """
        cursor = self.con.cursor()
        sql = "UPDATE empresa SET categoria = ?, descripcion = ?, impacto = ? WHERE id = ?;"  # Define la consulta SQL para actualizar un registro en la tabla "empresa"
        data = (categoria, desc, impacto, mi_id)
        cursor.execute(sql, data)
        self.con.commit()

    def consultar_todos(self):
        """
        Este método consulta y devuelve todos los registros almacenados
        en la tabla ``empresa``.

        Los registros se obtienen ordenados de forma descendente según
        el identificador ``id``, mostrando primero los registros más recientes.

        :param self: La instancia de la clase Modelo.
        :type self: Modelo
        :return: Una lista con todas las filas obtenidas de la consulta SQL.
        :rtype: list
        """
        cursor = (
            self.con.cursor()
        )  # Crea un cursor para ejecutar comandos SQL en la base de datos
        sql = "SELECT * FROM empresa ORDER BY id DESC;"  # Define la consulta SQL para seleccionar todos los registros ordenados por id en orden ascendente

        tabla = cursor.execute(sql)  # Ejecuta la conuslta.
        tabla2 = (
            tabla.fetchall()
        )  # Devuelve una lista con todas las filas resultantes de la consulta.
        return tabla2

    def cerrar_base(self):
        """
        Este método cierra la conexión activa con la base de datos SQLite.

        Se utiliza para liberar recursos y finalizar correctamente
        la comunicación con la base de datos una vez que ya no se necesita.

        :param self: La instancia de la clase Modelo.
        :type self: Modelo
        """
        self.con.close()
