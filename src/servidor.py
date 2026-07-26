"""
servidor.py:
Servidor de Logs UDP utilizando la infraestructura de socketserver.
Escucha en el puerto 9999 y guarda cada registro en un archivo de texto.
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
    encoding="utf-8"
)


class ManejadorLogsUDP(socketserver.BaseRequestHandler):
    """
    Clase manejadora que procesa los paquetes UDP entrantes enviados
    por el LoggerObserver de la aplicación principal.
    """
    def handle(self):
        # 1. Obtenemos los bytes enviados por el cliente y la IP/Puerto
        datos_bytes = self.request[0]
        mensaje = datos_bytes.decode('utf-8').strip()
        ip_cliente, puerto_cliente = self.client_address

        # 2. Preparamos el mensaje del log
        registro = f"[{ip_cliente}:{puerto_cliente}] -> {mensaje}"

        # 3. Muestra en pantalla el log recibido
        print(f"📥 [LOG RECIBIDO]: {registro}")

        # 4. Guarda el log usando el módulo logging nativo
        logging.info(registro)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    print("=" * 60)
    print(f" SERVIDOR DE LOGS UDP EN EJECUCIÓN INICIADO")
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