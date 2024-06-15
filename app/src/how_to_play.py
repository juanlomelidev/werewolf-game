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
        <h2 style="color: #E6B31E;">Fases del Juego</h2>
<ol style="color: #E6B31E; list-style-type: none; padding-left: 0;">
    <li><b>Configuración Inicial</b>
        <ul style="list-style-type: none;">
            <li>Los jugadores se conectan al juego y se les asignan roles de forma aleatoria.</li>
            <li>Cada jugador recibe una breve descripción de su rol y sus habilidades.</li>
        </ul>
    </li>
    <li><b>Noche</b>
        <ul style="list-style-type: none;">
            <li>La pantalla se oscurece y los jugadores con roles nocturnos pueden actuar.</li>
            <li><b>Hombres Lobo:</b> Seleccionan en secreto a un jugador para eliminar.</li>
            <li><b>Vidente:</b> Elige a un jugador para descubrir su rol.</li>
            <li><b>Bruja:</b> Decide si usa sus pociones (si aún las tiene).</li>
        </ul>
    </li>
    <li><b>Día</b>
        <ul style="list-style-type: none;">
            <li>Los jugadores discuten y comparten sus sospechas en el chat del juego.</li>
            <li>Se abre una votación para linchar a un jugador sospechoso.</li>
            <li>El jugador con más votos es eliminado y su rol se revela.</li>
        </ul>
    </li>
    <li><b>Repetición de Fases</b>
        <ul style="list-style-type: none;">
            <li>Las fases de noche y día se repiten hasta que se cumpla una condición de victoria:</li>
            <ul style="list-style-type: none;">
                <li>Todos los hombres lobo han sido eliminados.</li>
                <li>Los hombres lobo superan en número a los aldeanos.</li>
            </ul>
        </ul>
    </li>
</ol>

<h2 style="color: #E6B31E;">Controles y Funciones</h2>
<ul style="color: #E6B31E; list-style-type: none; padding-left: 0;">
    <li><b>Chat:</b> Comunícate con otros jugadores para discutir sospechas y estrategias.</li>
    <li><b>Votación:</b> Participa en las votaciones durante el día para linchar a los sospechosos.</li>
    <li><b>Habilidades:</b> Usa las habilidades de tu rol durante las fases correspondientes (noche para roles especiales).</li>
</ul>

<h2 style="color: #E6B31E;">Consejos de Juego</h2>
<ul style="color: #E6B31E; list-style-type: none; padding-left: 0;">
    <li><b>Aldeanos:</b>
        <ul style="list-style-type: none;">
            <li>Presta atención a los comportamientos sospechosos.</li>
            <li>Colabora y comparte información para descubrir a los hombres lobo.</li>
        </ul>
    </li>
    <li><b>Hombres Lobo:</b>
        <ul style="list-style-type: none;">
            <li>Actúa con cuidado y trata de no parecer sospechoso.</li>
            <li>Coordina con otros hombres lobo (si hay más de uno) para seleccionar a las víctimas.</li>
        </ul>
    </li>
    <li><b>Roles Especiales:</b>
        <ul style="list-style-type: none;">
            <li>Usa tus habilidades estratégicamente para maximizar su impacto.</li>
            <li>Mantén en secreto tu rol para evitar ser objetivo de los hombres lobo.</li>
        </ul>
    </li>
</ul>

<h2 style="color: #E6B31E;">Fin del Juego</h2>
<ul style="color: #E6B31E; list-style-type: none; padding-left: 0;">
    <li>El juego termina cuando se cumple una de las condiciones de victoria.</li>
    <li>Los roles de todos los jugadores se revelan y se muestra el equipo ganador.</li>
</ul>

<h2 style="color: #E6B31E;">Nota Final</h2>
<p style="color: #E6B31E;">Diviértete y disfruta del juego! La clave para ganar en "Werewolf" es la comunicación efectiva y la habilidad para engañar o descubrir a otros jugadores.</p>
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
