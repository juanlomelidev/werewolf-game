# WER-12 Creación Menú Principal View
# Asignado: Francisco Morales

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, pyqtSignal

class MainWindow(QWidget):
    mostrarClientView = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Werewolf")
        self.setWindowIcon(QIcon('Icon.png'))
        self.setStyleSheet("background-color: #2F2F2F")
        
        layout = QVBoxLayout()

        self.is_fullscreen = False 

        label = QLabel()
        layout.addWidget(label, alignment=Qt.AlignCenter)
        
        fs_button = QPushButton()
        fs_button.clicked.connect(self.fullscreen)
        layout.addWidget(fs_button, alignment=Qt.AlignCenter)

        # Layout para el título
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop) 
        title_layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(title_layout)

        title_label = QLabel("Werewolf")
        title_font = QFont("Consolas", 70, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #E6B31E;")
        title_layout.addWidget(title_label)

    
        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(0, 70, 0, 70)
        title_layout.addLayout(button_layout)

        button_font = QFont("Consolas", 15, QFont.Bold)

        perfil_button = QPushButton("Perfil")
        perfil_button.setFont(button_font)
        perfil_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 20px;")
        perfil_button.clicked.connect(self.perfil)
        button_layout.addWidget(perfil_button)

        start_button = QPushButton("Iniciar juego")
        start_button.setFont(button_font)
        start_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 20px;")
        button_layout.addWidget(start_button)

        settings_button = QPushButton("How to Play")
        settings_button.setFont(button_font)
        settings_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 20px;")
        button_layout.addWidget(settings_button)

        exit_button = QPushButton("Salir")
        exit_button.setFont(button_font)
        exit_button.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 20px;")
        button_layout.addWidget(exit_button)
        exit_button.clicked.connect(self.close)

        button_layout.addStretch() 


    def fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
        else:
            self.showFullScreen()
        self.is_fullscreen = not self.is_fullscreen

    def perfil(self):
        self.mostrarClientView.emit()
        self.hide()


class ClientView(QWidget):
    mostrarMenuPrincipal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Lo que va a ver el cliente')
        self.setStyleSheet("background-color: #2F2F2F")

        self.is_fullscreen = False 

        layout = QVBoxLayout()

        label = QLabel()
        layout.addWidget(label, alignment=Qt.AlignCenter)

        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop) 
        title_layout.setContentsMargins(50, 50, 50, 50)
        
        title_label = QLabel("Perfil")
        title_font = QFont("Consolas", 70, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #E6B31E;")
        title_layout.addWidget(title_label)

        campo_texto_font = QFont("Consolas", 15, QFont.Bold)
        
        campo_texto = QLineEdit(self)
        campo_texto.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 20px;")
        campo_texto.setPlaceholderText('Usuario')
        campo_texto.setFont(campo_texto_font)
        self.campo_texto = campo_texto

        boton_font = QFont("Consolas", 15, QFont.Bold)

        boton_guardar = QPushButton('Guardar', self)
        boton_guardar.setFont(boton_font)
        boton_guardar.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 20px;")
        boton_guardar.clicked.connect(self.guardar)
        
        boton_borrar = QPushButton('Borrar', self)
        boton_borrar.setFont(boton_font)
        boton_borrar.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 20px;")
        boton_borrar.clicked.connect(self.borrar)
        
        boton_atras = QPushButton('Atras', self)
        boton_atras.setFont(boton_font)
        boton_atras.setStyleSheet("background-color: #3E3E3E; color: #E6B31E; padding: 20px;")
        boton_atras.clicked.connect(self.MenuPrincipal)
        
        layout_principal = QVBoxLayout()
        layout_horizontal = QHBoxLayout()

        layout_horizontal.addWidget(campo_texto)
        layout_principal.addLayout(layout_horizontal)
        layout_principal.addWidget(boton_guardar)
        layout_principal.addWidget(boton_borrar)
        layout_principal.addWidget(boton_atras)

        layout.addLayout(title_layout)
        layout.addLayout(layout_principal)
        
        self.setLayout(layout)

    def guardar(self):
        texto = self.campo_texto.text()
        print(f'Usuario ingresado: {texto}')

    def borrar(self):
        self.campo_texto.clear()

    def MenuPrincipal(self):
        self.mostrarMenuPrincipal.emit()
        self.close()

    def fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
        else:
            self.showFullScreen()
        self.is_fullscreen = not self.is_fullscreen


if __name__ == "__main__":
    app = QApplication(sys.argv)

    menuPrincipal = MainWindow()
    Perfil = ClientView()

    menuPrincipal.mostrarClientView.connect(Perfil.show)
    Perfil.mostrarMenuPrincipal.connect(menuPrincipal.show)

    menuPrincipal.show()
    sys.exit(app.exec_())
