from PyQt5.QtWidgets import QDialog, QMessageBox, QPlainTextEdit, QVBoxLayout


class CompareDialog(QDialog):
    def __init__(self, text1, text2, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Compare Files')
        self.layout = QVBoxLayout()

        self.text_edit1 = QPlainTextEdit()
        self.text_edit1.setPlainText(text1)
        self.layout.addWidget(self.text_edit1)

        self.text_edit2 = QPlainTextEdit()
        self.text_edit2.setPlainText(text2)
        self.layout.addWidget(self.text_edit2)

        self.setLayout(self.layout)

    def closeEvent(self, event):
        # Prompt to save changes for Untitled file
        if self.parent().tab_widget.tabText(self.parent().tab_widget.currentIndex()) == 'Untitled':
            reply = QMessageBox.question(self, 'Save File', 'Do you want to save the file?',
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if reply == QMessageBox.Save:
                self.parent().save_untitled_file()
            elif reply == QMessageBox.Cancel:
                event.ignore()
        else:
            # Automatically save changes for named files
            self.parent().save_current_file()

        event.accept()
