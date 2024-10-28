import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSplashScreen, QWidget, QPushButton, QVBoxLayout, QMessageBox, QGridLayout, QLabel,QHBoxLayout
)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QImage, QBrush, QDesktopServices, QMovie
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize


class AnimationWindow:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Set up splash screen
        splash_pixmap = QPixmap(r"aa.png")
        self.splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
        self.splash.setMask(splash_pixmap.mask())
        self.splash.show()

        # Load main window after a delay of 1691 ms
        QTimer.singleShot(1691, self.load_main_window)

    def load_main_window(self):
        self.splash.hide()

        # Main window setup
        self.window = QMainWindow()
        self.window.setWindowTitle("CipherShield")
        self.window.showFullScreen()

        # Set background image for main window to fit screen
        background_image = QImage(r"ab.jpg").scaled(
            self.window.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.window.setPalette(palette)

        # Set up central widget and main layout
        self.central_widget = QWidget()
        self.window.setCentralWidget(self.central_widget)

        # Create and arrange main window components
        self.create_main_window()
        self.window.show()

    def create_main_window(self):
        layout = QVBoxLayout()
        grid_layout = QGridLayout()

        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()  # Create a horizontal layout

        # Create a QLabel for the heading
        heading_label = QLabel("Welcome to CipherShield")
        heading_label.setFont(QFont("Arial", 44, QFont.Bold))
        heading_label.setStyleSheet("color: white;")
        paragraph_label = QLabel(
        "This toolkit is designed to enhance your digital security by offering essential tools for password management. The Password Manager securely stores and organizes your credentials, while the Password Generator creates strong, unique passwords to protect your accounts. Use the Password Strength Checker to evaluate your existing passwords and receive improvement suggestions. The IP Lookup tool provides insights into your IP address and geolocation, helping you understand potential security risks. Finally, the Encryption/Decryption feature secures sensitive data, ensuring unauthorized access is prevented. Choose an option from the menu to get started and enhance your online safety."
        )
        paragraph_label.setFont(QFont("Arial", 18))
        paragraph_label.setStyleSheet("color: white;")
        paragraph_label.setWordWrap(True)  # Allow the paragraph to wrap
        # Create a vertical layout for the text
        text_layout = QVBoxLayout()
        text_layout.addWidget(heading_label)
        text_layout.addWidget(paragraph_label)

        # Create a grid layout for the buttons
        grid_layout = QGridLayout()
        # GitHub Repository Button
        github_button = self.create_button(
            "GitHub Repository",
            self.open_github_repo,
            font_size=18,
            align=Qt.AlignRight
        )
        grid_layout.addWidget(github_button, 1, 0, 1, 1)

        # Toolkit Button
        toolkit_button = self.create_button(
            "Toolkit",
            self.open_toolkit,
            font_size=18,
            align=Qt.AlignRight
        )
        grid_layout.addWidget(toolkit_button, 2, 0, 1, 1)

        # Quit Button
        quit_button = self.create_button(
            "Quit",
            self.confirm_quit_direct,
            font_size=18,
            align=Qt.AlignRight
        )
        grid_layout.addWidget(quit_button, 3, 0, 1, 1)

        horizontal_layout.addLayout(text_layout)  # Add the text layout on the left
        horizontal_layout.addLayout(grid_layout)  # Add the buttons layout on the right

        # Add the horizontal layout to the main layout
        layout.addLayout(horizontal_layout)

        self.central_widget.setLayout(layout)

    def create_button(self, text, method, font_size=14, align=Qt.AlignCenter):
        button = QPushButton(text)
        button.setFont(QFont("Arial", font_size))
        button.clicked.connect(method)
        button.setStyleSheet(
            "background-color: #00000; color: white; "
            "border: 2px solid white; padding: 10px; text-align: center;"
        )
        button.setCursor(Qt.PointingHandCursor)
        return button

    def open_github_repo(self):
        github_url = "https://github.com/harishy0406"
        QDesktopServices.openUrl(QUrl(github_url))

    def confirm_quit(self, event=None):
        confirm = QMessageBox.question(
            self.window,
            'Exit Confirmation',
            'Are you sure you want to quit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def confirm_quit_direct(self):
        # Confirmation for Quit button to prevent double prompt
        confirm = QMessageBox.question(
            self.window,
            'Exit Confirmation',
            'Are you sure you want to quit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.window.close()

    def open_toolkit(self):
        # Fullscreen toolkit window setup
        self.toolkit_window = QMainWindow()
        self.toolkit_window.setWindowTitle("Toolkit")
        self.toolkit_window.showFullScreen()

        # Background image for toolkit window
        background_image = QPixmap(r"toolkit back.jpg").scaled(self.toolkit_window.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.toolkit_window.setPalette(palette)

        central_widget = QWidget()
        self.toolkit_window.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Create toolkit buttons
        self.create_toolkit_buttons(layout)

        central_widget.setLayout(layout)
        self.toolkit_window.show()

    def create_toolkit_buttons(self, layout):
        # Toolkit buttons with labels and methods
        buttons = [
            ("Password Manager", self.password_manager),
            ("Password Generator", self.password_generator),
            ("Password Strength Checker", self.password_strength_checker),
            ("IP Lookup", self.ip_look),
            ("Encryption/Decryption", self.encryption_decryption),
            ("Back", self.toolkit_window.close)
        ]

        # Add buttons to layout
        for text, method in buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 30))
            button.clicked.connect(method)
            button.setStyleSheet(
                "background-color: #00000; color: white; border: 4px solid black; "
                "padding: 30px; text-align: center;"
            )
            button.setCursor(Qt.PointingHandCursor)
            layout.addWidget(button)

    def password_manager(self):
        subprocess.Popen(["python", r"password_manager.py"])

    def password_generator(self):
        subprocess.Popen(["python", r"password_generator.py"])

    def password_strength_checker(self):
        subprocess.Popen(["python", r"password_strength.py"])

    def ip_look(self):
        subprocess.Popen(["python", r"ip_lookup_latest.py"])

    def encryption_decryption(self):
        subprocess.Popen(["python", r"encry_decry.py"])

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = AnimationWindow()
    app.run()
