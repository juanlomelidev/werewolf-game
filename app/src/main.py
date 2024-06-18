import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

class MainWindow(QWidget):
    startGameSignal = pyqtSignal()
    mostrarHowToPlay = pyqtSignal()
    mostrarLoginRegister = pyqtSignal()
    mostrarMenuPrincipal = pyqtSignal()
    mostrarLeaderboard = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Werewolf")

        window_width = 400
        window_height = 300
        self.resize(window_width, window_height)

        self.setStyleSheet("background-color: #2F2F2F")
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.welcome_label = QLabel()
        self.initUI()

    def initUI(self):
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop) 
        title_layout.setContentsMargins(50, 50, 50, 50)
        self.layout.addLayout(title_layout)

        title_label = QLabel("Werewolf")
        title_font = QFont("Consolas", 60, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #E6B31E;")
        title_layout.addWidget(title_label)

        button_layout = QVBoxLayout()
        self.layout.addLayout(button_layout)

        button_font = QFont("Consolas", 15, QFont.Bold)

        start_button = QPushButton("START GAME")
        start_button.setFont(button_font)
        start_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 15px;")
        button_layout.addWidget(start_button)
        start_button.clicked.connect(self.startGame)

        settings_button = QPushButton("HOW TO PLAY")
        settings_button.setFont(button_font)
        settings_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 15px;")
        button_layout.addWidget(settings_button)
        settings_button.clicked.connect(self.openHowToPlay)

        login_button = QPushButton("LOGIN / REGISTER")
        login_button.setFont(button_font)
        login_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 15px;")
        button_layout.addWidget(login_button)
        login_button.clicked.connect(self.openLoginRegister)

        leaderboard_button = QPushButton("LEADERBOARD")
        leaderboard_button.setFont(button_font)
        leaderboard_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 15px;")
        button_layout.addWidget(leaderboard_button)
        leaderboard_button.clicked.connect(self.openLeaderboard)

        exit_button = QPushButton("EXIT")
        exit_button.setFont(button_font)
        exit_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 15px;")
        button_layout.addWidget(exit_button)
        exit_button.clicked.connect(self.close)

        button_layout.addStretch()

    def setWelcomeMessage(self, username):
        self.welcome_label.setText(f"Bienvenido {username}")
        self.welcome_label.setFont(QFont("Consolas", 20, QFont.Bold))
        self.welcome_label.setStyleSheet("color: #E6B31E;")
        self.layout.insertWidget(0, self.welcome_label, alignment=Qt.AlignCenter)

    def startGame(self):
        self.startGameSignal.emit()
        self.close()

    def openHowToPlay(self):
        self.mostrarHowToPlay.emit()

    def openLoginRegister(self):
        self.mostrarLoginRegister.emit()

    def openLeaderboard(self):
        self.mostrarLeaderboard.emit()

    def returnToMenu(self):
        self.show()

if __name__ == "__main__":
    from how_to_play import HowtoPlay
    import client
    from register import AuthWindow
    from leaderboard import GameWindow

    app = QApplication(sys.argv)

    menuPrincipal = MainWindow()
    howToPlayWindow = HowtoPlay()
    authWindow = AuthWindow()
    leaderboardWindow = GameWindow()

    menuPrincipal.mostrarHowToPlay.connect(howToPlayWindow.show)
    howToPlayWindow.mostrarMenuPrincipal.connect(menuPrincipal.show)

    menuPrincipal.mostrarLoginRegister.connect(authWindow.show)
    authWindow.loginSuccessful.connect(menuPrincipal.setWelcomeMessage)  # Conectar la señal del login exitoso
    authWindow.mostrarMenuPrincipal.connect(menuPrincipal.show)

    menuPrincipal.mostrarLeaderboard.connect(leaderboardWindow.show)
    leaderboardWindow.mostrarMenuPrincipal.connect(menuPrincipal.show)

    def show_client_gui():
        client_gui = client.ClientGUI()
        client_gui.show()
        client_gui.connect_to_server('localhost', 12345)

    menuPrincipal.startGameSignal.connect(show_client_gui)

    menuPrincipal.show()
    sys.exit(app.exec_())
