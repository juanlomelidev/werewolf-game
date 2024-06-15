import socket
import threading
import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt
from PyQt5.QtGui import QPalette, QColor, QFont

class ServerSignals(QObject):
    update_users = pyqtSignal()
    update_messages = pyqtSignal(str)
    update_roles = pyqtSignal(str)
    update_vote_button_status = pyqtSignal(bool)
    update_night_button_status = pyqtSignal(bool)

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
        self.revealed_roles = set()
        self.signals = ServerSignals()
        self.votes = {}
        self.eliminated_players = set()
        self.signals.update_messages.connect(self.update_messages_box)
        self.signals.update_roles.connect(self.update_roles_box)
        self.signals.update_vote_button_status.connect(self.update_vote_button_status_box)
        self.signals.update_night_button_status.connect(self.update_night_button_status_box)

    def initUI(self):
        self.setWindowTitle('Moderator')
        self.setStyleSheet("background-color: #333333; color: #E6B31E; border-radius: 10px;")

        window_width = 600
        window_height = 400
        self.resize(window_width, window_height)

        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        self.move(x, y)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_layout = QHBoxLayout(self.main_widget)

        self.left_layout = QVBoxLayout()

        self.moderator_label = QLabel("moderator")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.moderator_label.setFont(font)
        self.moderator_label.setAlignment(Qt.AlignCenter)
        self.left_layout.addWidget(self.moderator_label)

        self.assign_roles_button = QPushButton("START GAME")
        self.assign_roles_button.clicked.connect(self.assign_roles)
        self.assign_roles_button.setStyleSheet("background-color: #E6B31E; color: #333333; border-radius: 5px; padding: 10px 20px;")
        self.left_layout.addWidget(self.assign_roles_button)

        self.users_label = QLabel("CHAT")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.users_label.setFont(font)
        self.users_label.setAlignment(Qt.AlignCenter)
        self.left_layout.addWidget(self.users_label)

        self.messages_box = QTextEdit()
        self.messages_box.setReadOnly(True)
        self.messages_box.setStyleSheet("background-color: #E6B31E; color: #333333; border-radius: 5px;")
        self.left_layout.addWidget(self.messages_box)

        self.input_box = QLineEdit()
        self.input_box.setStyleSheet("background-color: #E6B31E; color: #333333; border-radius: 2px;")
        self.left_layout.addWidget(self.input_box)

        self.send_button = QPushButton("SEND MESSAGE")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("background-color: #E6B31E; color: #333333; border-radius: 5px; padding: 10px 20px;")
        self.left_layout.addWidget(self.send_button)

        self.right_layout = QVBoxLayout()

        self.roles_label = QLabel("PLAYER ROLES")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.roles_label.setFont(font)
        self.roles_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.roles_label)

        self.roles_box = QTextEdit()
        self.roles_box.setReadOnly(True)
        self.roles_box.setStyleSheet("background-color: #E6B31E; color: #333333; border-radius: 5px;")
        self.right_layout.addWidget(self.roles_box)

        self.enable_vote_button = QPushButton("ENABLE VOTATION")
        self.enable_vote_button.clicked.connect(self.enable_vote_button_action)
        self.enable_vote_button.setStyleSheet("background-color: #E6B31E; color: #333333; border-radius: 5px; padding: 10px 20px;")
        self.right_layout.addWidget(self.enable_vote_button)

        self.disable_vote_button = QPushButton("DISABLE VOTATION")
        self.disable_vote_button.clicked.connect(self.disable_vote_button_action)
        self.disable_vote_button.setStyleSheet("background-color: #E6B31E; color: #333333; border-radius: 5px; padding: 10px 20px;")
        self.right_layout.addWidget(self.disable_vote_button)

        self.enable_night_actions = QPushButton("ENABLE NIGHT ACTIONS")
        self.enable_night_actions.clicked.connect(self.enable_night_action)
        self.enable_night_actions.setStyleSheet("background-color: #E6B31E; color: #333333; border-radius: 5px; padding: 10px 20px;")
        self.right_layout.addWidget(self.enable_night_actions)

        self.disable_night_actions = QPushButton("DISABLE NIGHT ACTIONS")
        self.disable_night_actions.clicked.connect(self.disable_night_action)
        self.disable_night_actions.setStyleSheet("background-color: #E6B31E; color: #333333; border-radius: 5px; padding: 10px 20px;")
        self.right_layout.addWidget(self.disable_night_actions)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

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
        non_eliminated_players = [name for conn, name in self.client_names.items() if self.client_names[conn] not in self.eliminated_players]
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
        special_roles = ["seer", "mayor"]
        villager_roles = ["villager"]
        wolf_roles = []
        players = len(self.clients)
        if 1 <= players <= 7:
            wolf_roles = ["wolf"]
        elif 8 <= players <= 10:
            wolf_roles = ["wolf", "wolf"]
        elif 11 <= players <= 13:
            wolf_roles = ["wolf", "wolf", "wolf"]
        elif 14 <= players <= 16:
            wolf_roles = ["wolf", "wolf", "wolf", "wolf"]
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

    def enable_night_action(self):
        self.broadcast("ENABLE_NIGHT_BUTTON")
        self.signals.update_night_button_status.emit(True)

        # Implement Seer's night action
        seer_name = None
        for player, role in self.roles.items():
            if role == 'seer':
                seer_name = player
                break

        if seer_name:
            available_players = [player for player in self.roles if player not in self.revealed_roles and player != seer_name]
            if available_players:
                chosen_player = random.choice(available_players)
                self.revealed_roles.add(chosen_player)
                seer_message = f"Seer sees: {chosen_player} is {self.roles[chosen_player]}"
                self.broadcast_to_seer(seer_message)
            else:
                self.revealed_roles.clear()  # Reset if all players have been revealed

    def disable_night_action(self):
        self.broadcast("DISABLE_NIGHT_BUTTON")
        self.signals.update_night_button_status.emit(False)
        self.count_votes_and_broadcast_winner()

    def broadcast_to_seer(self, message):
        for client, player_name in self.client_names.items():
            if self.roles.get(player_name) == 'seer':
                try:
                    client.sendall(message.encode())
                except:
                    self.clients.remove(client)

    def count_votes_and_broadcast_winner(self):
        if not self.votes:
            self.broadcast("No votes received.")
            return

        max_votes = max(self.votes.values())

        candidates = [player for player, votes in self.votes.items() if votes == max_votes]

        if len(candidates) == 1:
            winner = candidates[0]
            self.broadcast(f"The player eliminated with the most votes is: {winner} with {self.votes[winner]} votes.")
            self.send_elimination_status(winner, True)
        else:
            self.broadcast("The vote has resulted in a tie. No player will be eliminated.")

        self.votes.clear()
        self.check_victory_conditions()

    def send_elimination_status(self, player_name, eliminated):
        client = next((client for client, name in self.client_names.items() if name == player_name), None)
        if client:
            try:
                status_message = f"ELIMINATED:{eliminated}"
                client.sendall(status_message.encode())
                if eliminated:
                    self.eliminated_players.add(player_name)
            except:
                self.clients.remove(client)

    def check_victory_conditions(self):
        wolves = {name for name, role in self.roles.items() if 'wolf' in role}
        alive_players = {name for name in self.client_names.values() if name not in self.eliminated_players}
        alive_wolves = wolves.intersection(alive_players)
        alive_villagers = alive_players - wolves

        if not alive_wolves:
            self.broadcast("Villagers win! All wolves have been eliminated.")
            self.broadcast_game_result("YOU WIN", alive_villagers)
            self.disable_game()
        elif len(alive_wolves) >= len(alive_villagers):
            self.broadcast("Wolves win! They outnumber the remaining villagers.")
            self.broadcast_game_result("YOU WIN", alive_wolves)
            self.disable_game()
        elif len(alive_wolves) == 1 and len(alive_villagers) == 1:
            self.broadcast("Wolves win! Only one villager remains, unable to stop the wolf.")
            self.broadcast_game_result("YOU WIN", alive_wolves)
            self.disable_game()

    def broadcast_game_result(self, result, players):
        for client, player_name in self.client_names.items():
            if player_name in players:
                try:
                    client.sendall(result.encode())
                except:
                    self.clients.remove(client)

    def disable_game(self):
        self.broadcast("DISABLE_GAME")

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

    @pyqtSlot(bool)
    def update_night_button_status_box(self, status):
        self.enable_night_actions.setEnabled(not status)
        self.disable_night_actions.setEnabled(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    server_gui = ServerGUI()
    server_gui.start_server('localhost', 12345)
    sys.exit(app.exec_())
