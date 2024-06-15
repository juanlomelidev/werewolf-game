import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import os

class RoleGUI(QWidget):
    mostrarHowToPlay = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roles of the Werewolf Game")
        self.setStyleSheet("background-color: #2F2F2F;")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        title_label = QLabel("Roles of the Werewolf Game")
        title_label.setFont(QFont("Consolas", 30, QFont.Bold))
        title_label.setStyleSheet("color: #E6B31E;")
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        self.combo_box = QComboBox()
        self.combo_box.setFont(QFont("Consolas", 15, QFont.Bold))
        self.combo_box.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 15px;")
        self.combo_box.addItems(["werewolf", "villager", "seer", "witch", "sorcerer", "hunter", "mayor"])
        self.combo_box.currentIndexChanged.connect(self.update_role_display)
        self.layout.addWidget(self.combo_box)

        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.text_label = QLabel()
        self.text_label.setFont(QFont("Consolas", 15, QFont.Bold))
        self.text_label.setStyleSheet("color: #E6B31E;")
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.text_label)

        back_button = QPushButton("BACK")
        back_button.setFont(QFont("Consolas", 15, QFont.Bold))
        back_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 20px;")
        back_button.clicked.connect(self.go_back)
        self.layout.addWidget(back_button)

        base_path = os.path.join(os.path.dirname(__file__), 'assets')
        self.roles_info = {
            "werewolf": (os.path.join(base_path, "werewolf.jpg"), "The werewolf tries to eliminate the villagers during the night."),
            "villager": (os.path.join(base_path, "villager.jpg"), "The villager tries to identify the wolves and survive."),
            "seer": (os.path.join(base_path, "seer.jpg"), "The seer can see the true identity of one player each night."),
            "witch": (os.path.join(base_path, "witch.jpg"), "The witch has a healing potion and a poison potion."),
            "sorcerer": (os.path.join(base_path, "sorcerer.jpg"), "The sorcerer works with the wolves and can see the seer."),
            "hunter": (os.path.join(base_path, "hunter.jpg"), "The hunter can shoot someone if eliminated."),
            "mayor": (os.path.join(base_path, "mayor.jpg"), "The mayor has the deciding vote in case of a tie.")
        }

        self.update_role_display()

    def update_role_display(self):
        role = self.combo_box.currentText()
        image_path, description = self.roles_info[role]

        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.text_label.setText(description)

    def go_back(self):
        self.mostrarHowToPlay.emit()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoleGUI()
    window.show()
    sys.exit(app.exec_())
