# WER-12 Creación Menú Principal View
# Asignado: Francisco Morales

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Werewolf")
        self.setStyleSheet("background-color: #2F2F2F;")
        self.showFullScreen() 

        # Layout para el título
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop) 
        self.setLayout(title_layout)

    
        title_label = QLabel("Werewolf")
        title_font = QFont("Arial", 36, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #E6B31E;")
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)

    
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignBottom) 
        title_layout.addLayout(button_layout)

    
        button_font = QFont("Arial", 14, QFont.Bold)

        perfil_button = QPushButton("Perfil")
        perfil_button.setFont(button_font)
        perfil_button.setStyleSheet("background-color: #4D4D4D; color: #E6B31E; padding: 10px;")
        button_layout.addWidget(perfil_button)

        start_button = QPushButton("Iniciar juego")
        start_button.setFont(button_font)
        start_button.setStyleSheet("background-color: #4D4D4D; color: #E6B31E; padding: 10px;")
        button_layout.addWidget(start_button)

        settings_button = QPushButton("Configuración")
        settings_button.setFont(button_font)
        settings_button.setStyleSheet("background-color: #4D4D4D; color: #E6B31E; padding: 10px;")
        button_layout.addWidget(settings_button)

        exit_button = QPushButton("Salir")
        exit_button.setFont(button_font)
        exit_button.setStyleSheet("background-color: #4D4D4D; color: #E6B31E; padding: 10px;")
        button_layout.addWidget(exit_button)

        button_layout.addStretch() 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
