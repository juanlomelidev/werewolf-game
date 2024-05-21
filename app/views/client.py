# WER-11 Creación Cliente View
# Asignado: Laura Esquibel
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, pyqtSignal

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    sys.exit(app.exec_())