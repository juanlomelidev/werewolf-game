import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mi Ventana con Botones y Campos de Texto')
        self.setGeometry(100, 100, 400, 300)  # (x, y, width, height)

        # Cambiar color de fondo de la ventana
        color_hex = '#83E1FF'
        estilo = f'background-color: {color_hex};'

        self.setStyleSheet(estilo)

        # Crear etiqueta y campo de texto
        self.etiqueta = QLabel('Texto:', self)
        self.campo_texto = QLineEdit(self)

        # Crear botones
        self.boton_mostrar = QPushButton('Mostrar Texto', self)
        self.boton_limpiar = QPushButton('Limpiar Texto', self)

        # Agrega los widgets en un Layout donde quedan uno abajo del otro
        layout = QVBoxLayout()
        layout.addWidget(self.etiqueta)
        layout.addWidget(self.campo_texto)
        layout.addWidget(self.boton_mostrar)
        layout.addWidget(self.boton_limpiar)

        # Establecer el diseño principal de la ventana
        self.setLayout(layout)

        # Conectar señales y slots
        self.boton_mostrar.clicked.connect(self.mostrarTexto)
        self.boton_limpiar.clicked.connect(self.limpiarTexto)

        self.show()

    def mostrarTexto(self):
        texto = self.campo_texto.text()
        print(f'Texto ingresado: {texto}')

    def limpiarTexto(self):
        self.campo_texto.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    sys.exit(app.exec_())
