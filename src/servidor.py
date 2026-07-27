"""
servidor.py:
Este módulo implementa el servidor de logs independiente que escucha
peticiones UDP provenientes de la aplicación principal y las registra
en un archivo de texto utilizando el módulo nativo ``logging``.
"""

import socketserver
import os
import logging

# Configuración del módulo logging nativo de Python
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_log = os.path.join(carpeta_actual, "app.log")

logging.basicConfig(
    filename=ruta_log,
    level=logging.INFO,
    format="%(levelname)s:%(name)s:[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)


class ManejadorLogsUDP(socketserver.BaseRequestHandler):
    """
    Clase manejadora que procesa los datagramas UDP entrantes enviados
    por la aplicación.

    Hereda de :class:`socketserver.BaseRequestHandler`.
    """

    def handle(self):
        """
        Método invocado automáticamente cada vez que se recibe un paquete UDP.

        Extrae el mensaje enviado, la dirección IP/puerto de origen,
        lo imprime en consola y lo guarda mediante el logger en ``app.log``.
        """
        # Obtenemos los bytes enviados por el cliente y la IP/Puerto
        datos_bytes = self.request[0]
        mensaje = datos_bytes.decode("utf-8").strip()
        ip_cliente, puerto_cliente = self.client_address

        # Preparamos el mensaje del log
        registro = f"[{ip_cliente}:{puerto_cliente}] -> {mensaje}"

        # Muestra en pantalla el log recibido
        print(f"[LOG RECIBIDO]: {registro}")

        # Guarda el log usando el módulo logging nativo
        logging.info(registro)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    print("=" * 60)
    print(" SERVIDOR DE LOGS UDP EN EJECUCIÓN INICIADO")
    print(f" Escuchando peticiones en {HOST}:{PORT}")
    print(" Presiona Ctrl+C para detener el servidor")
    print("=" * 60)
    logging.info(f"Servidor iniciado en {HOST}:{PORT}")

    # Instanciamos el servidor UDP en localhost:9999
    with socketserver.UDPServer((HOST, PORT), ManejadorLogsUDP) as servidor:
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            logging.warning("El servidor fue detenido manualmente por el usuario.")
            print("\nServidor detenido correctamente.")
