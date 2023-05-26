from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('About')
        self.layout = QVBoxLayout()

        label = QLabel('This is a simple notepad application created using PyQt.')
        self.layout.addWidget(label)

        self.setLayout(self.layout)
