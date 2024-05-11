import socket

# Creamos un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asociamos el socket al puerto y dirección local
server_address = ('localhost', 12345)
print('Iniciando servidor en %s puerto %s' % server_address)
server_socket.bind(server_address)

# Escuchamos conexiones entrantes
server_socket.listen(1)

while True:
    print('Esperando conexión...')
    connection, client_address = server_socket.accept()
    try:
        print('Conexión desde', client_address)
        
        while True:
            # Recibimos datos del cliente
            data = connection.recv(1024)
            if not data:
                break  # Salir del bucle si no hay datos

            print('Recibido:', data.decode())

            # Enviamos datos de vuelta al cliente
            message = input("Ingrese un mensaje para enviar al cliente (o 'exit' para salir): ")
            connection.sendall(message.encode())

            if message.lower() == 'exit':
                break  # Salir del bucle si el servidor envía 'exit'
    finally:
        # Cerramos la conexión
        connection.close()
