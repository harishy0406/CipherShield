import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt


class PasswordStrengthChecker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Strength Checker")
        self.setGeometry(0, 0, 600, 400)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)

        self.password_label = QLabel("Enter Password:", self)
        self.password_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        layout.addWidget(self.password_input)

        self.view_button = QPushButton("Show", self)
        self.view_button.setFixedWidth(60)
        self.view_button.setStyleSheet("QPushButton { background-color: #F2F2F2; border: 1px solid #DADADA; border-radius: 5px; padding: 5px; }"
                                        "QPushButton:hover { background-color: #E6E6E6; }"
                                        "QPushButton:pressed { background-color: #DADADA; }")
        layout.addWidget(self.view_button)

        self.check_button = QPushButton("Check Strength", self)
        self.check_button.setFixedWidth(150)
        self.check_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 5px; }"
                                        "QPushButton:hover { background-color: #45A049; }"
                                        "QPushButton:pressed { background-color: #3C893D; }")
        layout.addWidget(self.check_button)

        self.result_label = QLabel(self)
        self.result_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.result_label)

        # Suggestions layout
        self.suggestions_layout = QVBoxLayout()
        self.suggestion_labels = []
        for message in self.get_suggestion_messages():
            h_layout = QHBoxLayout()
            suggestion_label = QLabel(message["message"])
            suggestion_label.setStyleSheet("color: red")
            tick_label = QLabel("❌")  # Cross by default
            tick_label.setStyleSheet("font-size: 18px;")  # Increase size for visibility
            h_layout.addWidget(tick_label)
            h_layout.addWidget(suggestion_label)
            self.suggestions_layout.addLayout(h_layout)
            self.suggestion_labels.append((tick_label, message["regex"]))

        layout.addLayout(self.suggestions_layout)

        self.strength_score_label = QLabel("Strength Score: 0", self)
        self.strength_score_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.strength_score_label)

        self.check_button.clicked.connect(self.check_password_strength)
        self.view_button.clicked.connect(self.view_password)

        self.password_input.textChanged.connect(self.update_suggestions)
        self.password_input.returnPressed.connect(self.check_button.click)

    def check_password_strength(self):
        password = self.password_input.text()
        strength = self.calculate_password_strength(password)
        self.strength_score_label.setText(f"Strength Score: {strength}")

        if strength < 40:
            self.result_label.setText("Weak Password")
            self.result_label.setStyleSheet("color: red")
        elif strength < 70:
            self.result_label.setText("Medium Password")
            self.result_label.setStyleSheet("color: orange")
        else:
            self.result_label.setText("Strong Password")
            self.result_label.setStyleSheet("color: green")

    def update_suggestions(self):
        password = self.password_input.text()
        strength = self.calculate_password_strength(password)

        for tick_label, regex in self.suggestion_labels:
            if re.search(regex, password):
                tick_label.setText("✅")  # Tick mark for passed suggestions
            else:
                tick_label.setText("❌")  # Cross for failed suggestions

    def view_password(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.view_button.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.view_button.setText("Show")

    @staticmethod
    def calculate_password_strength(password):
        # Initialize score
        score = 0
        
        length = len(password)

        has_lowercase = any(char.islower() for char in password)
        has_uppercase = any(char.isupper() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special_char = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None

        # Calculate score based on criteria
        if length >= 8:
            score += 20  # +20 for length
        if length >= 12:
            score += 20  # +20 for longer length
        if length >= 16:
            score += 20  # +20 for very long length
        if has_lowercase:
            score += 10  # +10 for lowercase
        if has_uppercase:
            score += 10  # +10 for uppercase
        if has_digit:
            score += 10  # +10 for digit
        if has_special_char:
            score += 10  # +10 for special character

        return score

    @staticmethod
    def get_suggestion_messages():
        return [
            {"message": "At least 1 lowercase letter", "regex": r"[a-z]"},
            {"message": "At least 1 uppercase letter", "regex": r"[A-Z]"},
            {"message": "At least 1 special character", "regex": r"[!@#$%^&*(),.?\":{}|<>]"},
            {"message": "At least 1 number", "regex": r"[0-9]"},
            {"message": "At least 8 characters long", "regex": r".{8,}"},
        ]

    def closeEvent(self, event):
        confirm_exit = self.confirm_exit()
        if confirm_exit:
            event.accept()
        else:
            event.ignore()

    @staticmethod
    def confirm_exit():
        choice = QMessageBox.question(None, "Exit Confirmation",
                                      "Are you sure you want to exit?", 
                                      QMessageBox.Yes | QMessageBox.No)
        return choice == QMessageBox.Yes


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordStrengthChecker()
    
    # Setting the background color
    palette = window.palette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    window.setPalette(palette)
    
    window.show()
    sys.exit(app.exec_())
