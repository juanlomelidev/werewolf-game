import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt
from PyQt5.QtGui import QPalette, QColor, QFont

class ClientSignals(QObject):
    update_users = pyqtSignal(str)
    update_messages = pyqtSignal(str)
    update_role = pyqtSignal(str)

class ClientGUI(QMainWindow):
    role_colors = {
        "witch": QColor(255, 182, 193),  # Light Pink
        "sorcerer": QColor(138, 135, 226),  # Blue Violet
        "seer": QColor(0, 255, 127),  # Spring Green
        "hunter": QColor(255, 140, 0),  # Dark Orange
        "mayor": QColor(255, 215, 0),  # Gold
        "villager": QColor(240, 240, 240),  # Light Grey
        "wolf": QColor(161, 130, 98)  # Maroon
    }

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
        self.setWindowTitle('Werewolf')
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.layout = QVBoxLayout(self.main_widget)

        self.role_label = QLabel("WAIT FOR YOUR ROLE")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.role_label.setFont(font)
        self.role_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.role_label)

        self.day_label = QLabel("DAY ACTIONS")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.day_label.setFont(font)
        self.layout.addWidget(self.day_label)

        self.chat_label = QLabel("CHAT")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.chat_label.setFont(font)
        self.chat_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.chat_label)
        
        self.messages_box = QTextEdit()
        self.messages_box.setReadOnly(True)
        self.layout.addWidget(self.messages_box)
        
        
        
        self.input_box = QLineEdit()
        self.layout.addWidget(self.input_box)
        
        self.send_button = QPushButton("SEND MESSAGE")
        self.send_button.setStyleSheet("QPushButton {"
                               "background-color: #ffffff;"
                               "border: 2px solid #ffffff;"
                               "color: #000000;"
                               "padding: 10px 20px;"
                               "border-radius: 5px;"
                               "}"
                               "QPushButton:hover {"
                               "background-color: #f0f0f0;"
                               "border: 2px solid #f0f0f0;"
                               "}"
                               "QPushButton:pressed {"
                               "background-color: #d9d9d9;"
                               "border: 2px solid #d9d9d9;"
                               "}")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.night_label = QLabel("NIGHT ACTIONS")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.night_label.setFont(font)
        self.layout.addWidget(self.night_label)

        self.night_secondary_label = QLabel("Here will appear the night actions that you rol has, if there is none nothing will pop up.")
        font = QFont()
        font.setPointSize(8)
        self.night_secondary_label.setFont(font)
        self.layout.addWidget(self.night_secondary_label)

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
                if decoded_message.startswith("Players connected:"):
                    self.signals.update_users.emit(decoded_message)
                elif decoded_message.startswith("Your role is:"):
                    role = decoded_message.split(": ")[1]
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
        self.role_label.setText(f"{role}")
        color = self.role_colors.get(role, QColor(240, 240, 240))
        palette = self.palette()
        palette.setColor(QPalette.Window, color)
        self.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_gui = ClientGUI()
    client_gui.connect_to_server('localhost', 12345)
    sys.exit(app.exec_())
