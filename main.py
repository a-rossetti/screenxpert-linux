import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt


class WindowArrangementUI(QWidget):

    def __init__(self):
        super().__init__()
        self.ACTIVE_WINDOW_ID = self.get_active_window_id()
        self.buttons = []  # List to hold all buttons
        self.initUI()

    def initUI(self):
        self.show_initial_options()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # Ensure the UI stays on top
        x, y, _, _ = self.get_active_window_geometry()
        self.move(x, y)
        self.show()


    def run_command(self, command):
        """Helper function to run a shell command."""
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.communicate()

    def get_active_window_id(self):
        """Return the active window ID."""
        command = "xdotool getactivewindow"
        result = subprocess.check_output(command, shell=True).decode('utf-8').strip()
        return result
        
    def get_active_window_geometry(self):
        """Return the (x, y, width, height) of the active window."""
        command = f"xdotool getwindowgeometry --shell {self.ACTIVE_WINDOW_ID}"
        result = subprocess.check_output(command, shell=True).decode('utf-8').strip().split("\n")
        geometry_info = {}
        for line in result:
            key, value = line.split("=")
            geometry_info[key] = int(value)
        return geometry_info["X"], geometry_info["Y"], geometry_info["WIDTH"], geometry_info["HEIGHT"]
    

    def add_title(self, text):
        lbl = QLabel(text, self)
        lbl.setAlignment(Qt.AlignCenter)  # Center the label text
        lbl.setGeometry(20, 20, self.width() - 40, 30)  # Set geometry
        lbl.show()
        self.buttons.append(lbl)

    def add_back_button(self, callback):
        back_btn = QPushButton("←", self)
        back_btn.setGeometry(20, 20, 50, 30)
        back_btn.clicked.connect(callback)
        back_btn.show()
        self.buttons.append(back_btn)
    
    
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

    def show_initial_options(self):
        self.clear_buttons()
        self.setFixedSize(424, 366)
        self.add_button('Main Display', 20, 20, 384, 216, self.show_main_display_options)
        self.add_button('ScreenPad Plus', 20, 236, 384, 110, self.show_screenpad_plus_options)


    def move_and_resize_window(self, x, y, width, height, tile_vertically=False, tile_horizontally=False):
        self.run_command(f"xdotool windowactivate --sync {self.ACTIVE_WINDOW_ID} key --clearmodifiers Alt+F5")
        # move window to top left corner before resizing and moving it to ensure there's space to change size correctly
        self.run_command(f"xdotool windowmove {self.ACTIVE_WINDOW_ID} 0 0") 
        self.run_command(f"xdotool windowsize {self.ACTIVE_WINDOW_ID} {width} {height} windowmove {self.ACTIVE_WINDOW_ID} {x} {y}")

        if tile_vertically:
            self.run_command(f"wmctrl -i -r {self.ACTIVE_WINDOW_ID} -b add,maximized_vert")
        if tile_horizontally:
            self.run_command(f"wmctrl -i -r {self.ACTIVE_WINDOW_ID} -b add,maximized_horz")
        
        self.close()


    def show_main_display_options(self):
        self.clear_buttons()
        self.setFixedSize(632, 430)
        self.add_title("Main Display")
        self.add_back_button(self.initUI)
        self.add_button('Full\n Screen', 20, 70, 288, 162, lambda: self.move_and_resize_window(0, 0, 3840, 2160, True, True))
        self.add_button('Left\n half', 324, 70, 144, 162, lambda: self.move_and_resize_window(0, 0, 1920, 2160, True))
        self.add_button('Right\n half', 468, 70, 144, 162, lambda: self.move_and_resize_window(1920, 0, 1920, 2160, True))
        self.add_button('Two\n thirds', 20, 248, 192, 162, lambda: self.move_and_resize_window(0, 0, 2560, 2160))
        self.add_button('One\n third', 212, 248, 96, 162, lambda: self.move_and_resize_window(2560, 0, 1280, 2160))
        self.add_button('Top\n left', 324, 248, 144, 81, lambda: self.move_and_resize_window(0, 0, 1920, 1080))
        self.add_button('Top\n right', 468, 248, 144, 81, lambda: self.move_and_resize_window(1920, 0, 1920, 1080))
        self.add_button('Bottom\n left', 324, 329, 144, 81, lambda: self.move_and_resize_window(0, 1080, 1920, 1080))
        self.add_button('Bottom\n right', 468, 329, 144, 81, lambda: self.move_and_resize_window(1920, 1080, 1920, 1080))

    def show_screenpad_plus_options(self):
        self.clear_buttons()
        self.setFixedSize(424, 326)
        self.add_title("ScreenPad Plus")
        self.add_back_button(self.initUI)
        self.add_button('Full\n Screen', 20, 70, 384, 110, lambda: self.move_and_resize_window(0, 2160, 3840, 1100, True, True))
        self.add_button('Left\n half', 20, 196, 192, 110, lambda: self.move_and_resize_window(0, 2160, 1920, 1100, True))
        self.add_button('Right\n half', 212, 196, 192, 110, lambda: self.move_and_resize_window(1920, 2160, 1920, 1100, True))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WindowArrangementUI()
    sys.exit(app.exec_())
