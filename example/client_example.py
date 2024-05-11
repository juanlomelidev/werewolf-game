import socket

# Creamos un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectamos el socket al servidor
server_address = ('localhost', 12345)
print('Conectando a %s puerto %s' % server_address)
client_socket.connect(server_address)

try:
    while True:
        # Pedimos al usuario que ingrese un mensaje
        message = input("Ingrese un mensaje para enviar al servidor (o 'exit' para salir): ")
        
        if message.lower() == 'exit':
            break  # Salir del bucle si el usuario ingresa 'exit'

        # Enviamos el mensaje al servidor
        print('Enviando:', message)
        client_socket.sendall(message.encode())

        # Recibimos la respuesta del servidor
        data = client_socket.recv(1024)
        print('Recibido del servidor:', data.decode())

finally:
    # Cerramos la conexión
    client_socket.close()
