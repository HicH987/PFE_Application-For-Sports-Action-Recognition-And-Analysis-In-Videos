from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog, QLineEdit, QPushButton
from ui.Config import CSS

class CustomButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(
            Qt.PointingHandCursor
        )  # Set the cursor to a hand pointer by default

        # Set the common style sheet for all buttons
        self.setStyleSheet(CSS.btn)


class CustomInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Name")
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Enter your name:")
        self.line_edit = QLineEdit()
        self.button = QPushButton("OK")
        self.button.setStyleSheet(CSS.btn)
        self.button.clicked.connect(self.accept)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.button)

    def getText(self):
        return self.line_edit.text(), self.result() == QDialog.Accepted
