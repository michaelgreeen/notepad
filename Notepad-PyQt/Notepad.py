import sys

from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QDialog,
                             QFileDialog, QMainWindow, QPlainTextEdit,
                             QTabWidget, QTextEdit)

from AboutDialog import AboutDialog
from CompareDialog import CompareDialog
from OptionsDialog import OptionsDialog


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.current_file = ''

    def init_ui(self):
        self.text_edit = QPlainTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.init_menu_bar()

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab_widget)
        
        self.create_new_tab()
        
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('NotatnikPyQT')
        self.show()

    def init_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('Plik')
        new_action = QAction('Nowy', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction('Otwórz', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('Zapisz', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        plugin_menu = menubar.addMenu('Wtyczki')

        plugin_group = QActionGroup(self)
        plugin_group.setExclusive(True)  # Only one plugin can be selected at a time

        compare_action = QAction('Porównaj', self)
        compare_action.triggered.connect(self.compare_files)
        compare_action.setCheckable(True)
        plugin_group.addAction(compare_action)
        plugin_menu.addAction(compare_action)

        options_menu = menubar.addMenu('Opcje')

        personalize_action = QAction('Personalizuj', self)
        personalize_action.triggered.connect(self.show_options_dialog)
        options_menu.addAction(personalize_action)

        about_menu = menubar.addMenu('O aplikacji')
        about_action = QAction('O aplikacji', self)
        about_action.triggered.connect(self.show_about_dialog)
        about_menu.addAction(about_action)

    def create_new_tab(self):
        new_tab = QTextEdit()
        self.tab_widget.addTab(new_tab, 'Bez tytułu')

    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def new_file(self):
        self.create_new_tab()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Otwórz plik', '', 'Pliki tekstowe (*.txt);;Wszystkie pliki (*.*)')
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                new_tab = QPlainTextEdit()
                new_tab.setPlainText(text)
                self.tab_widget.addTab(new_tab, file_path)

    def save_file(self):
        current_tab_index = self.tab_widget.currentIndex()
        current_tab = self.tab_widget.widget(current_tab_index)

        if self.tab_widget.tabText(current_tab_index) == 'Bez tytułu':
            # If the file is untitled, prompt for the file path
            file_path, _ = QFileDialog.getSaveFileName(self, 'Zapisz plik', '', 'Pliki tekstowe (*.txt);;Wszystkie pliki (*.*)')
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(current_tab.toPlainText())

                self.tab_widget.setTabText(current_tab_index, file_path)  # Update the tab name with the saved file name
        else:
            # If the file already has a name, save directly without prompting for the file path
            file_path = self.tab_widget.tabText(current_tab_index)
            with open(file_path, 'w') as file:
                file.write(current_tab.toPlainText())
                                                                                                             
    def compare_files(self):
        current_tab_index = self.tab_widget.currentIndex()
        current_tab = self.tab_widget.widget(current_tab_index)
        current_text = current_tab.toPlainText()

        file_path, _ = QFileDialog.getOpenFileName(self, 'Wybierz plik do porównania', '', 'Pliki tekstowe (*.txt);;Wszystkie pliki (*.*)')
        if file_path:
            with open(file_path, 'r') as file:
                other_text = file.read()

            dialog = CompareDialog(current_text, other_text, parent=self) 
            dialog.exec_()

            if dialog.result() == QDialog.Accepted:
                updated_text = dialog.text_edit1.toPlainText()
                current_tab.setPlainText(updated_text)
        dialog = CompareDialog(current_text, other_text, parent=self)  # Pass the parent instance to the dialog
        dialog.exec_()

        # Update the current tab with the changes made in the Compare dialog
        if dialog.result() == QDialog.Accepted:
            updated_text = dialog.text_edit1.toPlainText()
            current_tab.setPlainText(updated_text)

    def show_about_dialog(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()

    def show_options_dialog(self):
        current_tab_index = self.tab_widget.currentIndex()
        current_tab = self.tab_widget.widget(current_tab_index)

        options_dialog = OptionsDialog(current_tab, parent=self)  # Pass the current tab's text_edit
        options_dialog.exec_()

    def save_untitled_file(self):
        current_tab_index = self.tab_widget.currentIndex()
        current_tab = self.tab_widget.widget(current_tab_index)

        file_path, _ = QFileDialog.getSaveFileName(self, 'Zapisz plik', '', 'Pliki tekstowe (*.txt);;Wszystkie pliki (*.*)')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(current_tab.toPlainText())

            self.tab_widget.setTabText(current_tab_index, file_path)  # Update the tab name with the saved file name

    def save_current_file(self):
        current_tab_index = self.tab_widget.currentIndex()
        current_tab = self.tab_widget.widget(current_tab_index)
        file_path = self.tab_widget.tabText(current_tab_index)

        with open(file_path, 'w') as file:
            file.write(current_tab.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad = Notepad()
    sys.exit(app.exec_())
