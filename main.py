import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSplashScreen, QWidget, QPushButton, QVBoxLayout, QMessageBox, QGridLayout, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QImage, QBrush, QDesktopServices
from PyQt5.QtCore import Qt, QTimer, QUrl


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
        horizontal_layout = QHBoxLayout()  # Create a horizontal layout

        # Create a QLabel for the heading
        heading_label = QLabel("Welcome to CipherShield")
        heading_label.setFont(QFont("Arial", 44, QFont.Bold))
        heading_label.setStyleSheet("color: white;")

        # Description paragraph
        paragraph_label = QLabel(
            "This toolkit is designed to enhance your digital security by offering essential tools for password management. "
            "The Password Manager securely stores and organizes your credentials, while the Password Generator creates strong, unique passwords "
            "to protect your accounts. Use the Password Strength Checker to evaluate your existing passwords and receive improvement suggestions. "
            "The IP Lookup tool provides insights into your IP address and geolocation, helping you understand potential security risks. "
            "Finally, the Encryption/Decryption feature secures sensitive data, ensuring unauthorized access is prevented."
        )
        paragraph_label.setFont(QFont("Arial", 18))
        paragraph_label.setStyleSheet("color: white;")
        paragraph_label.setWordWrap(True)

        # Layout for heading and paragraph
        text_layout = QVBoxLayout()
        text_layout.addWidget(heading_label)
        text_layout.addWidget(paragraph_label)

        # Grid layout for buttons
        grid_layout = QGridLayout()

        # Add buttons to grid layout
        buttons = [
            ("GitHub Repository", self.open_github_repo),
            ("Toolkit", self.open_toolkit),
            ("Team Members", self.open_team_members),
            ("Quit", self.confirm_quit_direct)
        ]

        for i, (text, method) in enumerate(buttons):
            button = self.create_button(text, method)
            grid_layout.addWidget(button, i, 0, 1, 1)

        # Arrange main layout
        horizontal_layout.addLayout(text_layout)
        horizontal_layout.addLayout(grid_layout)
        layout.addLayout(horizontal_layout)

        self.central_widget.setLayout(layout)

    def create_button(self, text, method, font_size=18):
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
        github_url = "https://github.com/harishy0406/CipherShield"
        QDesktopServices.openUrl(QUrl(github_url))

    def confirm_quit_direct(self):
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
        background_image = QPixmap(r"toolkit back.png").scaled(
            self.toolkit_window.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.toolkit_window.setPalette(palette)

        central_widget = QWidget()
        self.toolkit_window.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Toolkit buttons with labels and methods
        buttons = [
            ("Password Manager", self.password_manager),
            ("Password Generator", self.password_generator),
            ("Password Strength Checker", self.password_strength_checker),
            ("IP Lookup", self.ip_look),
            ("Encryption/Decryption", self.encryption_decryption),
            ("Back", self.toolkit_window.close)
        ]

        # Add buttons to toolkit layout
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

        central_widget.setLayout(layout)
        self.toolkit_window.show()

    def open_team_members(self):
        # Create a new window to display team members' information
        self.team_window = QMainWindow()
        self.team_window.setWindowTitle("Team Members")
        self.team_window.resize(600, 400)

        # Set up background image for the team window
        team_background = QPixmap(r"team_background.jpg").scaled(
            self.team_window.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(team_background))
        self.team_window.setPalette(palette)

        # Set up central widget and layout for the team window
        team_widget = QWidget()
        team_layout = QVBoxLayout()

        # Add team members' information
        team_info = QLabel("Team Members:\n\n1.Anmol Verma - 22MIS0153\n2. Azmil Ashruff - 22MIS0074\n3. M Harish Gautham - 22MIS0421\n4. Ratnesh Chandra Pandey - 22MIS0009\n5. Prasoon Jha - 22MIS0033 ")
        team_info.setFont(QFont("Arial", 16))
        team_info.setStyleSheet("color: white;")
        team_info.setAlignment(Qt.AlignLeft)
        team_layout.addWidget(team_info)

        # Add a "Back" button to return to the main window
        back_button = QPushButton("Back")
        back_button.setFont(QFont("Arial", 16))
        back_button.clicked.connect(self.team_window.close)
        back_button.setStyleSheet(
            "background-color: #00000; color: white; border: 2px solid white; padding: 10px; text-align: center;"
        )
        back_button.setCursor(Qt.PointingHandCursor)
        team_layout.addWidget(back_button)

        team_widget.setLayout(team_layout)
        self.team_window.setCentralWidget(team_widget)
        self.team_window.show()

    # Define toolkit feature methods
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
