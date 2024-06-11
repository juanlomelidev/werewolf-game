import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel, QDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt
from PyQt5.QtGui import QPalette, QColor, QFont

class ClientSignals(QObject):
    update_users = pyqtSignal(str)
    update_messages = pyqtSignal(str)
    update_role = pyqtSignal(str)
    update_vote_button_status = pyqtSignal(bool)
    update_night_button_status = pyqtSignal(bool)

class VoteDialog(QDialog):
    def __init__(self, client_socket, players):
        super().__init__()
        self.client_socket = client_socket
        self.setWindowTitle("Vote")
        self.setStyleSheet("background-color: #333333; color: #ffffff; border-radius: 10px;")
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Choose a player to vote for elimination:")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        for player in players:
            button = QPushButton(player)
            button.setStyleSheet("QPushButton {"
                                 "background-color: #555555;"
                                 "color: #ffffff;"
                                 "padding: 10px 20px;"
                                 "border-radius: 5px;"
                                 "}"
                                 "QPushButton:hover {"
                                 "background-color: #777777;"
                                 "}"
                                 "QPushButton:pressed {"
                                 "background-color: #999999;"
                                 "}")
            button.clicked.connect(self.vote)
            self.layout.addWidget(button)

    def vote(self):
        sender = self.sender()
        vote_message = f"VOTE:{sender.text()}"
        self.client_socket.sendall(vote_message.encode())
        print(f"Voted for: {sender.text()}")
        self.close()

class ClientGUI(QMainWindow):
    role_colors = {
        "witch": QColor(255, 182, 193),
        "sorcerer": QColor(138, 135, 226),
        "seer": QColor(0, 255, 127),
        "hunter": QColor(255, 140, 0),
        "mayor": QColor(255, 215, 0),
        "villager": QColor(240, 240, 240),
        "wolf": QColor(161, 130, 98)
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
        self.signals.update_vote_button_status.connect(self.update_vote_button_status)
        self.signals.update_night_button_status.connect(self.update_night_button_status)
        self.is_eliminated = False

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
        self.chat_label = QLabel("CHAT")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.chat_label.setFont(font)
        self.chat_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.chat_label)
        self.messages_box = QTextEdit()
        self.messages_box.setReadOnly(True)
        self.messages_box.setStyleSheet("color: black; background-color: white;")
        self.messages_box.setTextInteractionFlags(Qt.NoTextInteraction)
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
        self.vote_button = QPushButton("VOTE")
        self.vote_button.setStyleSheet("QPushButton {"
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
        self.vote_button.clicked.connect(self.request_vote)
        self.vote_button.setEnabled(False)
        self.layout.addWidget(self.vote_button)
        self.night_button = QPushButton("NIGHT ACTION")
        self.night_button.setStyleSheet("QPushButton {"
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
        self.night_button.setEnabled(True)
        self.night_button.clicked.connect(self.perform_night_action)
        self.layout.addWidget(self.night_button)
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
                elif decoded_message == "DISABLE_GAME":
                    self.disable_all_buttons()
                elif decoded_message.startswith("Your role is:"):
                    role = decoded_message.split(": ")[1]
                    self.current_role = role
                    self.signals.update_role.emit(role)
                elif decoded_message == "ENABLE_VOTE_BUTTON":
                    self.signals.update_vote_button_status.emit(True)
                elif decoded_message == "DISABLE_VOTE_BUTTON":
                    self.signals.update_vote_button_status.emit(False)
                elif decoded_message == "ENABLE_NIGHT_ACTION":
                    self.signals.update_night_button_status.emit(True)
                elif decoded_message == "DISABLE_NIGHT_ACTION":
                    self.signals.update_night_button_status.emit(False)
                elif decoded_message.startswith("ELIMINATED:"):
                    eliminated = decoded_message.split(":")[1] == 'True'
                    self.handle_elimination(eliminated)
                elif decoded_message == "YOU WIN":
                    self.chat_label.setText("YOU WIN")
                    font = QFont()
                    font.setPointSize(14)
                    font.setBold(True)
                    self.chat_label.setFont(font)
                    self.chat_label.setStyleSheet("color: #00FF00; font-weight: bold;")
                else:
                    self.signals.update_messages.emit(decoded_message)
        finally:
            self.client_socket.close()

    def disable_all_buttons(self):
        self.send_button.setEnabled(False)
        self.vote_button.setEnabled(False)
        self.night_button.setEnabled(False)
        self.send_button.setStyleSheet("QPushButton {"
                                       "background-color: #d4d4d4;"
                                       "border: 2px solid #d4d4d4;"
                                       "color: #d4d4d4;"
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
        self.vote_button.setStyleSheet("QPushButton {"
                                       "background-color: #d4d4d4;"
                                       "border: 2px solid #d4d4d4;"
                                       "color: #d4d4d4;"
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
        self.night_button.setStyleSheet("QPushButton {"
                                       "background-color: #d4d4d4;"
                                       "border: 2px solid #d4d4d4;"
                                       "color: #d4d4d4;"
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

    def send_message(self):
        message = self.input_box.text()
        if message:
            self.client_socket.sendall(message.encode())
            self.input_box.clear()
            if message.lower() == 'exit':
                self.close()

    def request_vote(self):
        self.client_socket.sendall("SOLICITAR_LISTA_JUGADORES".encode())

    @pyqtSlot(str)
    def update_users_box(self, player_list):
        self.vote_dialog = VoteDialog(self.client_socket, player_list.split("\n")[1:])
        self.vote_dialog.exec_()

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
        if role == "wolf":
            self.night_button.setText(f"Kill a player")
            self.night_button.setEnabled(True)
            self.night_button.setStyleSheet("QPushButton {"
                                       "background-color: red;"
                                       "border: 2px solid red;"
                                       "color: white;"
                                       "padding: 10px 20px;"
                                       "border-radius: 5px;"
                                       "}"
                                       "QPushButton:pressed {"
                                       "background-color: #8B0000;"
                                       "border: 2px solid #8B0000;"
                                       "}")
        else:
            self.night_button.setEnabled(False)
            self.night_button.setStyleSheet("QPushButton {"
                                       "background-color: #d4d4d4;"
                                       "border: 2px solid #d4d4d4;"
                                       "color: #d4d4d4;"
                                       "padding: 10px 20px;"
                                       "border-radius: 5px;"
                                       "}")

    @pyqtSlot(bool)
    def update_vote_button_status(self, status):
        if not self.is_eliminated:
            self.vote_button.setEnabled(status)

    @pyqtSlot(bool)
    def update_night_button_status(self, status):
        self.night_button.setEnabled(status)

    def perform_night_action(self):
        self.client_socket.sendall("SOLICITAR_LISTA_JUGADORES".encode())
        self.night_button.setEnabled(False)

    def handle_elimination(self, eliminated):
        self.is_eliminated = eliminated
        if eliminated:
            self.vote_button.setEnabled(False)
            self.send_button.setEnabled(False)
            self.input_box.setReadOnly(True)
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor('red'))
            self.setPalette(palette)
            self.role_label.setText("ELIMINATED")
            self.role_label.setStyleSheet("color: white; font-weight: bold;")
            self.disable_all_buttons()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_gui = ClientGUI()
    client_gui.connect_to_server('localhost', 12345)
    sys.exit(app.exec_())