import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject

class ClientSignals(QObject):
    update_users = pyqtSignal(str)
    update_messages = pyqtSignal(str)
    update_role = pyqtSignal(str)

class ClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages = []
        self.signals = ClientSignals()
        self.signals.update_users.connect(self.update_users_box)
        self.signals.update_messages.connect(self.update_messages_box)
        self.signals.update_role.connect(self.update_role_label)

    def initUI(self):
        self.setWindowTitle('Cliente de Chat')
        
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
        
        self.role_label = QLabel("Tu rol: ")
        self.layout.addWidget(self.role_label)
        
        self.input_box = QLineEdit()
        self.layout.addWidget(self.input_box)
        
        self.send_button = QPushButton("Enviar")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)
        
        self.request_users_button = QPushButton("Solicitar lista de jugadores")
        self.request_users_button.clicked.connect(self.request_player_list)
        self.layout.addWidget(self.request_users_button)
        
        self.show()
    
    def connect_to_server(self, address, port):
        self.client_socket.connect((address, port))
        
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def receive_messages(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                decoded_message = data.decode()
                if decoded_message.startswith("Jugadores conectados:"):
                    self.signals.update_users.emit(decoded_message)
                elif decoded_message.startswith("ROLE:"):
                    role = decoded_message.split(":")[1]
                    self.signals.update_role.emit(role)
                else:
                    self.signals.update_messages.emit(decoded_message)
        finally:
            self.client_socket.close()

    def send_message(self):
        message = self.input_box.text()
        if message:
            self.client_socket.sendall(message.encode())
            self.input_box.clear()
            if message.lower() == 'exit':
                self.close()

    def request_player_list(self):
        self.client_socket.sendall("SOLICITAR_LISTA_JUGADORES".encode())

    @pyqtSlot(str)
    def update_users_box(self, player_list):
        self.users_box.clear()
        self.users_box.append(player_list)

    @pyqtSlot(str)
    def update_messages_box(self, message):
        if message not in self.messages:
            self.messages.append(message)
            self.messages_box.append(message)

    @pyqtSlot(str)
    def update_role_label(self, role):
        self.role_label.setText(f"Tu rol: {role}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_gui = ClientGUI()
    client_gui.connect_to_server('localhost', 12345)
    sys.exit(app.exec_())
