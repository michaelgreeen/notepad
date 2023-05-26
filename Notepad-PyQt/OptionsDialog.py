from PyQt5.QtWidgets import (QColorDialog, QDialog, QDialogButtonBox,
                             QFontDialog, QLabel, QPushButton, QSpinBox,
                             QVBoxLayout)


class OptionsDialog(QDialog):
    def __init__(self, text_edit, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Options')
        self.layout = QVBoxLayout()

        self.font_size_label = QLabel('Font Size:')
        self.layout.addWidget(self.font_size_label)

        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(6, 72)
        self.layout.addWidget(self.font_size_spinbox)

        self.font_label = QLabel('Font:')
        self.layout.addWidget(self.font_label)

        self.font_button = QPushButton('Select Font')
        self.font_button.clicked.connect(self.select_font)
        self.layout.addWidget(self.font_button)

        self.font_color_label = QLabel('Font Color:')
        self.layout.addWidget(self.font_color_label)

        self.font_color_button = QPushButton('Select Color')
        self.font_color_button.clicked.connect(self.select_color)
        self.layout.addWidget(self.font_color_button)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout.addWidget(button_box)

        self.setLayout(self.layout)

        self.text_edit = text_edit

    def select_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_edit.setFont(font)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextColor(color)
            