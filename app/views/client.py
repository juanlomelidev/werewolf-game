# WER-11 Creación Cliente View
# Asignado: Laura Esquibel
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt

class MiVentana(QWidget):
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

        self.etiqueta = QLabel('Usuario:', self)
        self.etiqueta.setStyleSheet('color: #D4AD62;')
        self.campo_texto = QLineEdit(self)
        self.campo_texto.setStyleSheet('background-color: #4D4D4D;')
        

        self.boton_mostrar = QPushButton('Guardar usuario', self)
        self.boton_mostrar.setStyleSheet('background-color: #4D4D4D;color: #D4AD62;')
        self.boton_limpiar = QPushButton('Borrar usuario', self)
        self.boton_limpiar.setStyleSheet('background-color: #4D4D4D;color: #D4AD62;')
        
        layout_principal = QVBoxLayout()
        layout_horizontal = QHBoxLayout()

        layout_principal.addWidget(self.titulo)
        layout_horizontal.addWidget(self.etiqueta)
        layout_horizontal.addWidget(self.campo_texto)
        layout_principal.addLayout(layout_horizontal)
        layout_principal.addWidget(self.boton_mostrar)
        layout_principal.addWidget(self.boton_limpiar)

        self.setLayout(layout_principal)

        self.boton_mostrar.clicked.connect(self.mostrarTexto)
        self.boton_limpiar.clicked.connect(self.limpiarTexto)

        self.show()

    def mostrarTexto(self):
        texto = self.campo_texto.text()
        print(f'Usuario ingresado: {texto}')

    def limpiarTexto(self):
        self.campo_texto.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    sys.exit(app.exec_())