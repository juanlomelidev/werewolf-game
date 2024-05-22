import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject

class ServerSignals(QObject):
    update_users = pyqtSignal()
    update_messages = pyqtSignal(str)

class ServerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.client_names = {}
        self.messages = []
        self.player_counter = 1
        self.signals = ServerSignals()
        self.signals.update_users.connect(self.update_users_box)
        self.signals.update_messages.connect(self.update_messages_box)

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

    @pyqtSlot()
    def update_users_box(self):
        self.users_box.clear()
        for name in self.client_names.values():
            self.users_box.append(name)

    @pyqtSlot(str)
    def update_messages_box(self, message):
        self.messages_box.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    server_gui = ServerGUI()
    server_gui.start_server('localhost', 12345)
    sys.exit(app.exec_())
