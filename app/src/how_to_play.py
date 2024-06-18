import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from roles_gui import RoleGUI

class HowtoPlay(QWidget):
    mostrarMenuPrincipal = pyqtSignal()
    mostrarRoles = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("How to play")
        self.setStyleSheet("background-color: #2F2F2F;")
        self.resize(1000, 600)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        
        title_label = QLabel("HOW TO PLAY")
        self.title_font = QFont("Consolas", 50, QFont.Bold)
        title_label.setFont(self.title_font)
        title_label.setStyleSheet("color: #E6B31E;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        info_larga = """
        <h2 style="color: #E6B31E;">Phases of the Game</h2>
<ol style="color: #E6B31E; list-style-type: none; padding-left: 0;">
    <li><b>Initial Setup</b>
        <ul style="list-style-type: none;">
            <li>Players connect to the game and are assigned roles randomly.</li>
            <li>Each player receives a brief description of their role and abilities.</li>
        </ul>
    </li>
    <li><b>Noche</b>
        <ul style="list-style-type: none;">
            <li>The screen darkens and players with nocturnal roles can take action.</li>
            <li><b>Werewolf:</b> They secretly select a player to eliminate.</li>
            <li><b>Seer:</b> Choose a player to reveal their role.</li>
            <li><b>Witch:</b> Decide whether to use their potions (if they still have them).</li>
        </ul>
    </li>
    <li><b>Day</b>
        <ul style="list-style-type: none;">
            <li>Players discuss and share their suspicions in the game chat.</li>
            <li>A vote is opened to lynch a suspicious player.</li>
            <li>The player with the most votes is eliminated and their role is revealed.</li>
        </ul>
    </li>
    <li><b>Repetition of Phases</b>
        <ul style="list-style-type: none;">
            <li>The night and day phases repeat until a victory condition is met:</li>
            <ul style="list-style-type: none;">
                <li>All the werewolves have been eliminated.</li>
                <li>The werewolves outnumber or equal the number of villagers.</li>
            </ul>
        </ul>
    </li>
</ol>

<h2 style="color: #E6B31E;">Controls and Functions</h2>
<ul style="color: #E6B31E; list-style-type: none; padding-left: 0;">
    <li><b>Chat:</b> Communicate with other players to discuss suspicions and strategies.</li>
    <li><b>Votation:</b> Participate in the votes during the day to lynch the suspects.</li>
    <li><b>Habilities:</b> Use your role's abilities during the corresponding phases (night for special roles).</li>
</ul>

<h2 style="color: #E6B31E;">Game Tips</h2>
<ul style="color: #E6B31E; list-style-type: none; padding-left: 0;">
    <li><b>Villagers:</b>
        <ul style="list-style-type: none;">
            <li>Pay attention to suspicious behaviors.</li>
            <li>Collaborate and share information to uncover the werewolves.</li>
        </ul>
    </li>
    <li><b>Werewolves:</b>
        <ul style="list-style-type: none;">
            <li>Act carefully and try not to appear suspicious.</li>
            <li>Coordinate with other werewolves (if there is more than one) to select the victims.</li>
        </ul>
    </li>
    <li><b>Special Roles:</b>
        <ul style="list-style-type: none;">
            <li>Use your abilities strategically to maximize their impact.</li>
            <li>Keep your role a secret to avoid being targeted by the werewolves.</li>
        </ul>
    </li>
</ul>

<h2 style="color: #E6B31E;">End of game</h2>
<ul style="color: #E6B31E; list-style-type: none; padding-left: 0;">
    <li>The game ends when one of the victory conditions is met.</li>
    <li>The roles of all players are revealed and the winning team is displayed.</li>
</ul>

<h2 style="color: #E6B31E;">Final Note</h2>
<p style="color: #E6B31E;">Have fun and enjoy the game! The key to winning in "Werewolf" is effective communication and the ability to deceive or uncover other players.</p>
        """ 

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(info_larga)
        text_edit.setFont(QFont("Consolas", 15, QFont.Bold))
        text_edit.setStyleSheet("border: none;")
        text_edit.setMinimumHeight(400)
        
        layout.addWidget(text_edit)
        
        button_font = QFont("Consolas", 15, QFont.Bold)

        roles_button = QPushButton("ROLES")
        roles_button.setFont(button_font)
        roles_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 20px;")
        roles_button.clicked.connect(self.show_roles)
        layout.addWidget(roles_button)

        back_button = QPushButton("BACK")
        back_button.setFont(button_font)
        back_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 20px;")
        back_button.clicked.connect(self.returnToMenu)
        layout.addWidget(back_button)

        layout.addStretch()

        self.setLayout(layout)

    def returnToMenu(self):
        self.mostrarMenuPrincipal.emit()
        self.close()

    def show_roles(self):
        self.hide()
        self.roles_window = RoleGUI()
        self.roles_window.mostrarHowToPlay.connect(self.show)
        self.roles_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HowtoPlay()
    window.show()
    sys.exit(app.exec_())
