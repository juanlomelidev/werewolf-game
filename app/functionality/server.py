import socket
import threading
import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject

class ServerSignals(QObject):
    update_users = pyqtSignal()
    update_messages = pyqtSignal(str)
    update_roles = pyqtSignal(str)

class ServerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.client_names = {}
        self.messages = []
        self.player_counter = 1
        self.roles = {}
        self.signals = ServerSignals()
        self.signals.update_users.connect(self.update_users_box)
        self.signals.update_messages.connect(self.update_messages_box)
        self.signals.update_roles.connect(self.update_roles_box)

    def initUI(self):
        self.setWindowTitle('Servidor de Chat')
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.layout = QVBoxLayout(self.main_widget)
        
        self.users_label = QLabel("Usuarios conectados:")
        self.layout.addWidget(self.users_label)
        
        self.users_box = QTextEdit()
        self.users_box.setReadOnly(True)
        self.layout.addWidget(self.users_box)
        
        self.messages_box = QTextEdit()
        self.messages_box.setReadOnly(True)
        self.layout.addWidget(self.messages_box)
        
        self.input_box = QLineEdit()
        self.layout.addWidget(self.input_box)
        
        self.send_button = QPushButton("Enviar")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)
        
        self.assign_roles_button = QPushButton("Asignar roles")
        self.assign_roles_button.clicked.connect(self.assign_roles)
        self.layout.addWidget(self.assign_roles_button)
        
        self.roles_box = QTextEdit()
        self.roles_box.setReadOnly(True)
        self.layout.addWidget(self.roles_box)
        
        self.show()
    
    def start_server(self, address, port):
        self.server_socket.bind((address, port))
        self.server_socket.listen(8)  # Permite hasta 8 conexiones entrantes
        
        self.accept_thread = threading.Thread(target=self.accept_connections)
        self.accept_thread.start()
        
        self.signals.update_users.emit()

    def accept_connections(self):
        while True:
            connection, client_address = self.server_socket.accept()
            player_name = f"Jugador {self.player_counter}"
            self.player_counter += 1
            self.client_names[connection] = player_name
            self.clients.append(connection)
            
            self.broadcast(f"{player_name} se ha unido al chat.")
            self.signals.update_users.emit()

            client_thread = threading.Thread(target=self.handle_client, args=(connection, player_name))
            client_thread.start()

    def handle_client(self, connection, player_name):
        try:
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                decoded_message = data.decode()
                if decoded_message == "SOLICITAR_LISTA_JUGADORES":
                    self.send_player_list(connection)
                else:
                    message = f"{player_name}: {decoded_message}"
                    self.messages.append(message)
                    self.signals.update_messages.emit(message)
                    self.broadcast(message)
        finally:
            connection.close()
            self.clients.remove(connection)
            del self.client_names[connection]
            self.broadcast(f"{player_name} ha salido del chat.")
            self.signals.update_users.emit()

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.sendall(message.encode())
            except:
                self.clients.remove(client)
        self.signals.update_messages.emit(message)

    def send_player_list(self, connection):
        player_list = "Jugadores conectados:\n" + "\n".join(self.client_names.values())
        try:
            connection.sendall(player_list.encode())
        except:
            self.clients.remove(connection)

    def send_message(self):
        message = self.input_box.text()
        if message:
            full_message = f"Servidor: {message}"
            self.messages.append(full_message)
            self.signals.update_messages.emit(full_message)
            self.broadcast(full_message)
            self.input_box.clear()

    def assign_roles(self):
        # Define los roles según el algoritmo proporcionado
        special_roles = ["witch", "sorcerer", "seer", "hunter", "mayor"]
        villager_roles = ["villager"]
        wolf_roles = []

        players = len(self.clients)
        if 8 <= players <= 10:
            wolf_roles = ["wolf"]
        elif 11 <= players <= 13:
            wolf_roles = ["wolf", "wolf"]
        elif 14 <= players <= 16:
            wolf_roles = ["wolf", "wolf", "wolf"]
        else:
            print("Número de jugadores fuera del rango permitido (8-16).")
            return

        roles = special_roles + wolf_roles
        roles_villager_count = players - len(roles)
        roles += villager_roles * roles_villager_count
        random.shuffle(roles)

        self.roles = {self.client_names[client]: role for client, role in zip(self.clients, roles)}

        self.signals.update_roles.emit("\n".join([f"{player}: {role}" for player, role in self.roles.items()]))
        self.broadcast_roles()

    def broadcast_roles(self):
        for client in self.clients:
            try:
                role_message = f"Tu rol es: {self.roles[self.client_names[client]]}"
                client.sendall(role_message.encode())
            except:
                self.clients.remove(client)

    @pyqtSlot()
    def update_users_box(self):
        self.users_box.clear()
        for name in self.client_names.values():
            self.users_box.append(name)

    @pyqtSlot(str)
    def update_messages_box(self, message):
        self.messages_box.append(message)

    @pyqtSlot(str)
    def update_roles_box(self, roles):
        self.roles_box.clear()
        self.roles_box.append(roles)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    server_gui = ServerGUI()
    server_gui.start_server('localhost', 12345)
    sys.exit(app.exec_())
