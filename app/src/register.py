import sys
import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

class AuthWindow(QWidget):
    mostrarMenuPrincipal = pyqtSignal()
    loginSuccessful = pyqtSignal(str)  # Señal para indicar que el login fue exitoso

    def __init__(self):
        super().__init__()
        self.initUI()

        # Ruta al archivo JSON usando os.path
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_path, 'werewolf-users.json')

        # Inicializa Firebase Admin SDK
        cred = credentials.Certificate(json_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def initUI(self):
        self.setWindowTitle("Werewolf Auth")
        self.setStyleSheet("background-color: #2F2F2F;")

        self.stacked_widget = QStackedWidget()
        self.init_login_ui()
        self.init_register_ui()

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def init_login_ui(self):
        login_widget = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel("Werewolf Auth")
        title_font = QFont("Consolas", 30, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #E6B31E;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFont(QFont("Consolas", 15))
        self.email_input.setStyleSheet('background-color: #4D4D4D; color: #D4AD62; padding: 10px;')
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFont(QFont("Consolas", 15))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet('background-color: #4D4D4D; color: #D4AD62; padding: 10px;')
        layout.addWidget(self.password_input)

        login_button = QPushButton("Login")
        login_button.setFont(QFont("Consolas", 15, QFont.Bold))
        login_button.setStyleSheet('background-color: #3E3E3E; color: #E6B31E; padding: 20px;')
        login_button.clicked.connect(self.login_user)
        layout.addWidget(login_button)

        new_label = QLabel("Are you new?")
        font = QFont("Consolas", 14, QFont.Bold)
        new_label.setFont(font)
        new_label.setStyleSheet("color: #E6B31E; padding: 10px;")
        new_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(new_label)

        switch_to_register_button = QPushButton("REGISTER")
        switch_to_register_button.setFont(QFont("Consolas", 15, QFont.Bold))
        switch_to_register_button.setStyleSheet('background-color: #3E3E3E; color: #E6B31E; padding: 20px;')
        switch_to_register_button.clicked.connect(self.show_register)
        layout.addWidget(switch_to_register_button)

        back_button = QPushButton("BACK")
        back_button.setFont(QFont("Consolas", 15, QFont.Bold))
        back_button.setStyleSheet('background-color: #3E3E3E; color: #E6B31E; padding: 20px;')
        back_button.clicked.connect(self.returnToMenu)
        layout.addWidget(back_button)

        login_widget.setLayout(layout)
        self.stacked_widget.addWidget(login_widget)

    def init_register_ui(self):
        register_widget = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel("Register")
        title_font = QFont("Consolas", 30, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #E6B31E;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(QFont("Consolas", 15))
        self.username_input.setStyleSheet('background-color: #4D4D4D; color: #D4AD62; padding: 10px;')
        layout.addWidget(self.username_input)

        self.email_input_register = QLineEdit()
        self.email_input_register.setPlaceholderText("Email")
        self.email_input_register.setFont(QFont("Consolas", 15))
        self.email_input_register.setStyleSheet('background-color: #4D4D4D; color: #D4AD62; padding: 10px;')
        layout.addWidget(self.email_input_register)

        self.password_input_register = QLineEdit()
        self.password_input_register.setPlaceholderText("Password")
        self.password_input_register.setFont(QFont("Consolas", 15))
        self.password_input_register.setEchoMode(QLineEdit.Password)
        self.password_input_register.setStyleSheet('background-color: #4D4D4D; color: #D4AD62; padding: 10px;')
        layout.addWidget(self.password_input_register)

        register_button = QPushButton("REGISTER")
        register_button.setFont(QFont("Consolas", 15, QFont.Bold))
        register_button.setStyleSheet('background-color: #3E3E3E; color: #E6B31E; padding: 20px;')
        register_button.clicked.connect(self.register_user)
        layout.addWidget(register_button)

        new_label = QLabel("Already registered?")
        font = QFont("Consolas", 14, QFont.Bold)
        new_label.setFont(font)
        new_label.setStyleSheet("color: #E6B31E; padding: 10px;")
        new_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(new_label)

        switch_to_login_button = QPushButton("LOGIN")
        switch_to_login_button.setFont(QFont("Consolas", 15, QFont.Bold))
        switch_to_login_button.setStyleSheet('background-color: #3E3E3E; color: #E6B31E; padding: 20px;')
        switch_to_login_button.clicked.connect(self.show_login)
        layout.addWidget(switch_to_login_button)

        register_widget.setLayout(layout)
        self.stacked_widget.addWidget(register_widget)

    def register_user(self):
        username = self.username_input.text()
        email = self.email_input_register.text()
        password = self.password_input_register.text()

        if username and email and password:
            try:
                # Verifica si el usuario ya está registrado
                user_ref = self.db.collection('users').where('email', '==', email).limit(1)
                docs = list(user_ref.stream())

                if docs:
                    QMessageBox.warning(self, "Error", "The user is already registered!")
                else:
                    # Crea un nuevo documento en la colección 'users' con los campos correspondientes
                    user_data = {
                        'username': username,
                        'email': email,
                        'password': password
                    }
                    self.db.collection('users').add(user_data)
                    QMessageBox.information(self, "Success", "User registered successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to register user: {e}")
        else:
            QMessageBox.warning(self, "Input Error", "All fields are required!")

    def login_user(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if email and password:
            # Verifica las credenciales en Firestore
            user_ref = self.db.collection('users').where('email', '==', email).where('password', '==', password).limit(1)
            docs = list(user_ref.stream())  # Convierte el iterador en una lista para verificar si hay documentos

            if docs:
                # Credenciales válidas
                QMessageBox.information(self, "Success", "Login successful!")
                user_data = docs[0].to_dict()  # Obtiene los datos del usuario
                username = user_data.get('username', 'Usuario')
                self.loginSuccessful.emit(username)  # Emite la señal con el nombre de usuario
                self.close()
            else:
                # Credenciales inválidas
                QMessageBox.warning(self, "Error", "Invalid email or password!")
        else:
            QMessageBox.warning(self, "Input Error", "All fields are required!")

    def show_login(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_register(self):
        self.stacked_widget.setCurrentIndex(1)

    def returnToMenu(self):
        self.mostrarMenuPrincipal.emit()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    auth_window = AuthWindow()
    auth_window.show()

    sys.exit(app.exec_())
