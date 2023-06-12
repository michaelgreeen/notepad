import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import Gio as gio
from gi.repository import GLib as glib

class AboutDialog(gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            transient_for=parent,
            flags=gtk.DialogFlags.MODAL | gtk.DialogFlags.DESTROY_WITH_PARENT,
            title="About"
        )
        self.add_buttons(gtk.STOCK_CLOSE, gtk.ResponseType.CLOSE)

        content_area = self.get_content_area()
        label = gtk.Label(label="This is a simple notepad application created using Gtk.")
        content_area.pack_start(label, True, True, 0)
        self.show_all()


class CompareDialog(gtk.Dialog):
    def __init__(self, text1, text2, parent):
        super().__init__(
            transient_for=parent,
            flags=gtk.DialogFlags.MODAL | gtk.DialogFlags.DESTROY_WITH_PARENT,
            title="Compare Files"
        )
        self.add_buttons(gtk.STOCK_CLOSE, gtk.ResponseType.CLOSE)

        self.text_view1 = gtk.TextView()
        self.text_view1.get_buffer().set_text(text1)
        self.text_view2 = gtk.TextView()
        self.text_view2.get_buffer().set_text(text2)

        grid = gtk.Grid()
        grid.attach(self.text_view1, 0, 0, 1, 1)
        grid.attach(self.text_view2, 1, 0, 1, 1)
        self.get_content_area().add(grid)

        self.connect("close", self.on_close)

    def on_close(self, dialog):
        if self.get_transient_for().get_title() == 'Untitled':
            response = self.run_custom_question_dialog(
                self.get_transient_for(),
                "Do you want to save the file?",
                [
                    (gtk.STOCK_SAVE, gtk.ResponseType.YES),
                    (gtk.STOCK_CLOSE, gtk.ResponseType.NO),
                    (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL),
                ],
            )
            if response == gtk.ResponseType.YES:
                self.get_transient_for().save_untitled_file()
            elif response == gtk.ResponseType.CANCEL:
                return gtk.ResponseType.CANCEL
        else:
            self.get_transient_for().save_current_file()

        self.destroy()


class OptionsDialog(gtk.Dialog):
    def __init__(self, text_view, parent):
        super().__init__(
            transient_for=parent,
            flags=gtk.DialogFlags.MODAL | gtk.DialogFlags.DESTROY_WITH_PARENT,
            title="Options"
        )
        self.add_buttons(gtk.STOCK_OK, gtk.ResponseType.OK, gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL)

        self.text_view = text_view

        self.font_label = gtk.Label(label="Font:")
        self.font_button = gtk.Button(label="Select Font")
        self.font_button.connect("clicked", self.select_font)
        self.font_color_label = gtk.Label(label="Font Color:")
        self.font_color_button = gtk.Button(label="Select Color")
        self.font_color_button.connect("clicked", self.select_color)

        grid = gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(6)
        grid.attach(self.font_label, 0, 0, 1, 1)
        grid.attach(self.font_button, 0, 1, 1, 1)
        grid.attach(self.font_color_label, 0, 2, 1, 1)
        grid.attach(self.font_color_button, 0, 3, 1, 1)
        content_area = self.get_content_area()
        content_area.pack_start(grid, True, True, 0)
        self.show_all()

    def select_font(self, button):
        font_dialog = gtk.FontChooserDialog(transient_for=self, title="Select Font")
        font_dialog.set_font_desc(self.text_view.get_style_context().get_font())
        response = font_dialog.run()
        if response == gtk.ResponseType.OK:
            font_desc = font_dialog.get_font_desc()
            self.text_view.override_font(font_desc)
        font_dialog.destroy()

    def select_color(self, button):
        color_dialog = gtk.ColorChooserDialog(transient_for=self, title="Select Color")
        response = color_dialog.run()
        if response == gtk.ResponseType.OK:
            rgba = color_dialog.get_rgba()
            self.text_view.override_color(gtk.StateFlags.NORMAL, rgba)
        color_dialog.destroy()
class Notepad:
    def init(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("notepad.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("main_window")
        self.text_view = self.builder.get_object("text_view")
        self.tab_widget = self.builder.get_object("tab_widget")

        self.current_file = ""

        self.window.show_all()
    def on_main_window_destroy(self, widget):
        gtk.main_quit()

    def on_menu_new_activate(self, widget):
        self.create_new_tab()

    def on_menu_open_activate(self, widget):
        file_dialog = gtk.FileChooserDialog(
            title="Open",
            parent=self.window,
            action=gtk.FileChooserAction.OPEN,
            buttons=(
                gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
                gtk.STOCK_OPEN, gtk.ResponseType.ACCEPT
            )
        )
        response = file_dialog.run()
        if response == gtk.ResponseType.ACCEPT:
            file_path = file_dialog.get_filename()
            if file_path:
                with open(file_path, "r") as file:
                    text = file.read()
                    self.create_new_tab(text, file_path)
        file_dialog.destroy()

    def on_menu_save_activate(self, widget):
        current_tab_index = self.tab_widget.get_current_page()
        current_tab = self.tab_widget.get_nth_page(current_tab_index)
        if current_tab.get_label() == "Untitled":
            self.save_untitled_file()
        else:
            self.save_current_file()

    def on_menu_compare_activate(self, widget):
        current_tab_index = self.tab_widget.get_current_page()
        current_tab = self.tab_widget.get_nth_page(current_tab_index)
        current_text = current_tab.get_buffer().get_text(
            current_tab.get_buffer().get_start_iter(),
            current_tab.get_buffer().get_end_iter(),
            False
        )

        file_dialog = gtk.FileChooserDialog(
            title="Select File to Compare",
            parent=self.window,
            action=gtk.FileChooserAction.OPEN,
            buttons=(
                gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
                gtk.STOCK_OPEN, gtk.ResponseType.ACCEPT
            )
        )
        response = file_dialog.run()
        if response == gtk.ResponseType.ACCEPT:
            file_path = file_dialog.get_filename()
            if file_path:
                with open(file_path, "r") as file:
                    other_text = file.read()

                dialog = CompareDialog(current_text, other_text, parent=self)
                response = dialog.run()
                dialog.destroy()

                if response == gtk.ResponseType.ACCEPT:
                    updated_text = dialog.text_view1.get_buffer().get_text(
                        dialog.text_view1.get_buffer().get_start_iter(),
                        dialog.text_view1.get_buffer().get_end_iter(),
                        False
                    )
            current_tab.get_buffer().set_text(updated_text)
            file_dialog.destroy()

    def on_menu_personalize_activate(self, widget):
        current_tab_index = self.tab_widget.get_current_page()
        current_tab = self.tab_widget.get_nth_page(current_tab_index)
        options_dialog = OptionsDialog(current_tab, parent=self.window)
        response = options_dialog.run()
        options_dialog.destroy()

        if response == gtk.ResponseType.OK:
            font_desc = current_tab.override_font(None)
            font_color = current_tab.override_color(gtk.StateFlags.NORMAL, None)

    def on_menu_about_activate(self, widget):
        about_dialog = AboutDialog(parent=self.window)
        response = about_dialog.run()
        about_dialog.destroy()

    def on_tab_widget_switch_page(self, widget, page, page_num):
        if page_num >= 0:
            file_path = self.tab_widget.get_tab_label_text(page)
            self.current_file = file_path

    def create_new_tab(self, text="", file_path="Untitled"):
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)

        text_view = gtk.TextView()
        text_view.set_wrap_mode(gtk.WrapMode.WORD)
        text_view.get_buffer().set_text(text)
        scrolled_window.add(text_view)

        label = gtk.Label(file_path)
        label.set_tooltip_text(file_path)

        hbox = gtk.Box(orientation=gtk.Orientation.HORIZONTAL, spacing=6)
        hbox.pack_start(label, True, True, 0)
        close_button = gtk.Button.new_from_icon_name("window-close", gtk.IconSize.SMALL_TOOLBAR)
        close_button.set_focus_on_click(False)
        hbox.pack_start(close_button, False, False, 0)

        self.tab_widget.append_page(scrolled_window, hbox)
        self.tab_widget.set_tab_reorderable(scrolled_window, True)
        self.tab_widget.set_current_page(self.tab_widget.get_n_pages() - 1)

        close_button.connect("clicked", self.on_tab_close_button_clicked)

    def on_tab_close_button_clicked(self, button):
        page_num = self.tab_widget.page_num(button.get_parent())
        if page_num >= 0:
            tab_label = self.tab_widget.get_tab_label(button.get_parent())
            if tab_label.get_text() == "Untitled":
                response = self.run_custom_question_dialog(
                    self.window,
                    "Do you want to save the file?",
                    [
                        (gtk.STOCK_SAVE, gtk.ResponseType.YES),
                        (gtk.STOCK_CLOSE, gtk.ResponseType.NO),
                        (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL),
                    ],
                )
                if response == gtk.ResponseType.YES:
                    self.save_untitled_file()
                elif response == gtk.ResponseType.CANCEL:
                    return
            else:
                self.save_current_file()

            self.tab_widget.remove_page(page_num)

    def save_untitled_file(self):
        current_tab_index = self.tab_widget.get_current_page()
        current_tab = self.tab_widget.get_nth_page(current_tab_index)
        file_dialog = gtk.FileChooserDialog(
            title="Save File",
            parent=self.window,
            action=gtk.FileChooserAction.SAVE,
            buttons=(
                gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
                gtk.STOCK_SAVE, gtk.ResponseType.ACCEPT
            )
        )
        file_dialog.set_do_overwrite_confirmation(True)
        response = file_dialog.run()
        if response == gtk.ResponseType.ACCEPT:
            file_path = file_dialog.get_filename()
            if file_path:
                self.current_file = file_path
                with open(file_path, "w") as file:
                    text = current_tab.get_buffer().get_text(
                        current_tab.get_buffer().get_start_iter(),
                        current_tab.get_buffer().get_end_iter(),
                        False
                    )
                file.write(text)
                label = self.tab_widget.get_tab_label(current_tab)
                label.set_text(os.path.basename(file_path))
        file_dialog.destroy()

    def save_current_file(self):
        current_tab_index = self.tab_widget.get_current_page()
        current_tab = self.tab_widget.get_nth_page(current_tab_index)
        file_path = self.current_file
        if file_path:
            with open(file_path, "w") as file:
                text = current_tab.get_buffer().get_text(
                    current_tab.get_buffer().get_start_iter(),
                    current_tab.get_buffer().get_end_iter(),
                    False
                )
                file.write(text)

    def run_custom_question_dialog(self, parent, message, buttons):
        dialog = gtk.Dialog(
            transient_for=parent,
            flags=gtk.DialogFlags.MODAL | gtk.DialogFlags.DESTROY_WITH_PARENT,
            title="Question",
        )
        dialog.set_message_type(gtk.MessageType.QUESTION)
        dialog.set_markup(message)
        dialog.add_buttons(*buttons)
        dialog.set_default_response(gtk.ResponseType.CANCEL)
        response = dialog.run()
        dialog.destroy()
        return response

    def main(self):
        gtk.main()


if __name__ == "__main__":
    notepad = Notepad()
    notepad.main()