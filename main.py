import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt


class WindowArrangementUI(QWidget):

    def __init__(self):
        super().__init__()
        self.ACTIVE_WINDOW_ID = self.get_active_window_id()
        self.buttons = []  # List to hold all buttons
        self.initUI()


    def run_command(self, command):
        """Helper function to run a shell command."""
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.communicate()

    def get_active_window_id(self):
        """Return the active window ID."""
        command = "xdotool getactivewindow"
        result = subprocess.check_output(command, shell=True).decode('utf-8').strip()
        return result
    

    def initUI(self):
        self.add_button('Main Display', 20, 20, 384, 216, self.show_main_display_options)
        self.add_button('ScreenPad Plus', 20, 246, 384, 110, self.show_screenpad_plus_options)
        
        self.setFixedSize(424, 376)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # Ensure the UI stays on top
        self.show()

    def add_button(self, label, x, y, width, height, callback):
        btn = QPushButton(label, self)
        btn.setGeometry(x, y, width, height)
        if callback:
            btn.clicked.connect(callback)
        btn.show()
        self.buttons.append(btn)

    def clear_buttons(self):
        for btn in self.buttons:
            btn.hide()  # Hide the button
            btn.deleteLater()  # Schedule the button to be deleted later
        self.buttons = []


    def move_and_resize_window(self, x, y, width, height):
        # Move and resize the active window to the given coordinates and size
        self.run_command(f"xdotool windowactivate --sync {self.ACTIVE_WINDOW_ID} key --clearmodifiers Alt+F5")
        self.run_command(f"xdotool windowmove {self.ACTIVE_WINDOW_ID} {x} {y} windowsize {self.ACTIVE_WINDOW_ID} {width} {height}")


    def show_main_display_options(self):
        self.clear_buttons()
        self.setFixedSize(636, 382)
        self.add_button('Full\n Screen', 20, 20, 288, 162, lambda: self.move_and_resize_window(0, 0, 3840, 2160))
        self.add_button('Left\n half', 328, 20, 144, 162, lambda: self.move_and_resize_window(0, 0, 1920, 2160))
        self.add_button('Right\n half', 472, 20, 144, 162, lambda: self.move_and_resize_window(1920, 0, 1920, 2160))
        self.add_button('Two\n thirds', 20, 202, 192, 162, lambda: self.move_and_resize_window(0, 0, 2560, 2160))
        self.add_button('One\n third', 212, 202, 96, 162, lambda: self.move_and_resize_window(2560, 0, 1280, 2160))
        self.add_button('Top\n left', 328, 202, 144, 81, lambda: self.move_and_resize_window(0, 0, 1920, 1080))
        self.add_button('Top\n right', 472, 202, 144, 81, lambda: self.move_and_resize_window(1920, 0, 1920, 1080))
        self.add_button('Bottom\n left', 328, 283, 144, 81, lambda: self.move_and_resize_window(0, 1080, 1920, 1080))
        self.add_button('Bottom\n right', 472, 283, 144, 81, lambda: self.move_and_resize_window(1920, 1080, 1920, 1080))


    def show_screenpad_plus_options(self):
        self.clear_buttons()
        # Here, you will populate with buttons for ScreenPad Plus options
        # btn_full_screen_sp = QPushButton('Full Screen', self)
        # and so on...


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WindowArrangementUI()
    sys.exit(app.exec_())
