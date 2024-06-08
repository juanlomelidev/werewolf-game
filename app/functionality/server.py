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
    update_vote_button_status = pyqtSignal(bool)

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
        self.votes = {}
        self.eliminated_players = set()  # Almacenar los jugadores eliminados
        self.signals.update_users.connect(self.update_users_box)
        self.signals.update_messages.connect(self.update_messages_box)
        self.signals.update_roles.connect(self.update_roles_box)
        self.signals.update_vote_button_status.connect(self.update_vote_button_status_box)

    def initUI(self):
        self.setWindowTitle('Moderator')
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        self.users_label = QLabel("Players connected:")
        self.layout.addWidget(self.users_label)
        self.users_box = QTextEdit()
        self.users_box.setReadOnly(True)
        self.layout.addWidget(self.users_box)
        self.messages_box = QTextEdit()
        self.messages_box.setReadOnly(True)
        self.layout.addWidget(self.messages_box)
        self.input_box = QLineEdit()
        self.layout.addWidget(self.input_box)
        self.send_button = QPushButton("SEND MESSAGE")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)
        self.assign_roles_button = QPushButton("ASSIGN ROLES")
        self.assign_roles_button.clicked.connect(self.assign_roles)
        self.layout.addWidget(self.assign_roles_button)
        self.roles_box = QTextEdit()
        self.roles_box.setReadOnly(True)
        self.layout.addWidget(self.roles_box)
        self.enable_vote_button = QPushButton("ENABLE VOTATION")
        self.enable_vote_button.clicked.connect(self.enable_vote_button_action)
        self.layout.addWidget(self.enable_vote_button)
        self.disable_vote_button = QPushButton("DISABLE VOTATION")
        self.disable_vote_button.clicked.connect(self.disable_vote_button_action)
        self.layout.addWidget(self.disable_vote_button)
        self.show()

    def start_server(self, address, port):
        self.server_socket.bind((address, port))
        self.server_socket.listen(8)
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
            self.broadcast(f"{player_name} has joined the chat.")
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
                elif decoded_message.startswith("VOTE:"):
                    vote_for = decoded_message.split("VOTE:")[1]
                    # Verificar si el votante tiene el rol de 'mayor'
                    if self.roles.get(player_name) == 'mayor':
                        self.votes[vote_for] = self.votes.get(vote_for, 0) + 2
                    else:
                        self.votes[vote_for] = self.votes.get(vote_for, 0) + 1
                else:
                    message = f"{player_name}: {decoded_message}"
                    self.messages.append(message)
                    self.signals.update_messages.emit(message)
                    self.broadcast(message)
        finally:
            connection.close()
            self.clients.remove(connection)
            del self.client_names[connection]
            self.broadcast(f"{player_name} has left the chat.")
            self.signals.update_users.emit()

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.sendall(message.encode())
            except:
                self.clients.remove(client)
        self.signals.update_messages.emit(message)

    def send_player_list(self, connection):
        # Enviar solo la lista de jugadores no eliminados
        non_eliminated_players = [name for conn, name in self.client_names.items() if conn not in self.eliminated_players]
        player_list = "Players connected:\n" + "\n".join(non_eliminated_players)
        try:
            connection.sendall(player_list.encode())
        except:
            self.clients.remove(connection)

    def send_message(self):
        message = self.input_box.text()
        if message:
            full_message = f"Server: {message}"
            self.messages.append(full_message)
            self.signals.update_messages.emit(full_message)
            self.broadcast(full_message)
            self.input_box.clear()

    def assign_roles(self):
        special_roles = ["witch", "sorcerer", "seer", "hunter", "mayor"]
        villager_roles = ["villager"]
        wolf_roles = []
        players = len(self.clients)
        if 1 <= players <= 7:
            wolf_roles = ["wolf"]
        elif 8 <= players <= 10:
            wolf_roles = ["wolf"]
        elif 11 <= players <= 13:
            wolf_roles = ["wolf", "wolf"]
        elif 14 <= players <= 16:
            wolf_roles = ["wolf", "wolf", "wolf"]
        else:
            print("Number of players out of range (8-16).")
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
                role_message = f"Your role is: {self.roles[self.client_names[client]]}"
                client.sendall(role_message.encode())
            except:
                self.clients.remove(client)

    def enable_vote_button_action(self):
        self.broadcast("ENABLE_VOTE_BUTTON")
        self.signals.update_vote_button_status.emit(True)

    def disable_vote_button_action(self):
        self.broadcast("DISABLE_VOTE_BUTTON")
        self.signals.update_vote_button_status.emit(False)
        self.count_votes_and_broadcast_winner()

    def count_votes_and_broadcast_winner(self):
        if not self.votes:
            self.broadcast("No votes received.")
            return

        # Calcular el número máximo de votos que recibió un jugador
        max_votes = max(self.votes.values())

        # Encontrar todos los jugadores que recibieron el número máximo de votos
        candidates = [player for player, votes in self.votes.items() if votes == max_votes]

        # Solo proceder con la eliminación si hay un único jugador con el máximo de votos
        if len(candidates) == 1:
            winner = candidates[0]
            self.broadcast(f"The player eliminated with the most votes is: {winner} with {self.votes[winner]} votes.")
            # Encuentra el cliente correspondiente al ganador y envía el estado de eliminación
            for client, name in self.client_names.items():
                if name == winner:
                    self.send_elimination_status(client, True)
        else:
            # Enviar un mensaje indicando que hay un empate y que no se eliminará a nadie
            self.broadcast("The vote has resulted in a tie. No player will be eliminated.")

        self.votes.clear()

    def send_elimination_status(self, client, eliminated):
        try:
            status_message = f"ELIMINATED:{eliminated}"
            client.sendall(status_message.encode())
            if eliminated:
                self.eliminated_players.add(client)  # Marcar como eliminado
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

    @pyqtSlot(bool)
    def update_vote_button_status_box(self, status):
        self.enable_vote_button.setEnabled(not status)
        self.disable_vote_button.setEnabled(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    server_gui = ServerGUI()
    server_gui.start_server('localhost', 12345)
    sys.exit(app.exec_())
