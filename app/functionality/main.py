import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal


class MainWindow(QWidget):
    mostrarMiVentana = pyqtSignal()
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
        self.title_font = QFont("Arial", 36, QFont.Bold)
        title_label.setFont(self.title_font)
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
        perfil_button.clicked.connect(self.perfil)
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

    def perfil(self):
        self.mostrarMiVentana.emit()
        self.hide()

class MiVentana(QWidget):
    mostrarMenuPrincipal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Lo que va a ver el cliente')
        self.setGeometry(150, 150, 400, 300)

        color_hex = '#2F2F2F'
        estilo = f'background-color: {color_hex};'

        self.setFont(QFont('Arial', 15))
        self.setStyleSheet(estilo)

        self.titulo = QLabel('Perfil', self)
        self.titulo.setStyleSheet('color: #D4AD62; font-size: 20px;')
        self.titulo.setAlignment(Qt.AlignCenter)

        self.campo_texto = QLineEdit(self)
        self.campo_texto.setStyleSheet('background-color: #4D4D4D;')
        self.campo_texto.setPlaceholderText('Usuario')
        self.campo_texto.setStyleSheet('color: #D4AD62; font-size: 20px;')

        self.boton_guardar = QPushButton('Guardar', self)
        self.boton_guardar.setStyleSheet('background-color: #4D4D4D;color: #D4AD62;')
        self.boton_borrar = QPushButton('Borrar', self)
        self.boton_borrar.setStyleSheet('background-color: #4D4D4D;color: #D4AD62;')
        self.boton_atras = QPushButton('Atras', self)
        self.boton_atras.setStyleSheet('background-color: #4D4D4D;color: #D4AD62;')
        self.boton_atras.clicked.connect(self.MenuPrincipal)
        
        layout_principal = QVBoxLayout()
        layout_horizontal = QHBoxLayout()

        layout_principal.addWidget(self.titulo)
        layout_horizontal.addWidget(self.campo_texto)
        layout_principal.addLayout(layout_horizontal)
        layout_principal.addWidget(self.boton_guardar)
        layout_principal.addWidget(self.boton_borrar)
        layout_principal.addWidget(self.boton_atras)

        self.setLayout(layout_principal)

        self.boton_guardar.clicked.connect(self.guardar)
        self.boton_borrar.clicked.connect(self.borrar)
        

    def guardar(self):
        texto = self.campo_texto.text()
        print(f'Usuario ingresado: {texto}')

    def borrar(self):
        self.campo_texto.clear()

    def MenuPrincipal(self):
        self.mostrarMenuPrincipal.emit()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    menuPrincipal = MainWindow()
    Perfil = MiVentana()

    menuPrincipal.mostrarMiVentana.connect(Perfil.show)
    Perfil.mostrarMenuPrincipal.connect(menuPrincipal.show)

    menuPrincipal.show()
    sys.exit(app.exec_())
