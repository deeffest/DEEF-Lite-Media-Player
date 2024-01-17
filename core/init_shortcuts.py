#init_shortcuts.py
from PyQt5.QtWidgets import (
    QShortcut
)
from PyQt5.QtGui import (
    QKeySequence
)
from PyQt5.QtCore import (
    Qt
)
import sys

def _init_shortcuts(self):
    shortcuts = {
        Qt.CTRL + Qt.Key_Q: self.open_file_dialog,
        Qt.CTRL + Qt.Key_O: self.open_media_dialog,
        Qt.CTRL + Qt.Key_F: self.open_folder_dialog,
        Qt.CTRL + Qt.Key_X: lambda: sys.exit(),
        Qt.Key_F11: self.open_fullscreen,
        Qt.Key_F12: self.open_properties_dialog,
        Qt.ALT + Qt.Key_S: self.open_settings_dialog,
        Qt.Key_Space: self.play_pause_media,
        Qt.CTRL + Qt.Key_S: self.stop_media,
        Qt.CTRL + Qt.Key_R: self.toggle_media_repeat,
        Qt.CTRL + Qt.Key_M: self.toggle_media_mute,
        Qt.CTRL + Qt.Key_Left: self.open_previous_media,
        Qt.CTRL + Qt.Key_Right: self.open_next_media,
        Qt.Key_Left: self.rewind_media,
        Qt.Key_Right: self.forward_media,
        Qt.CTRL + Qt.Key_G: self.open_go_to_dialog,
        Qt.CTRL + Qt.ALT + Qt.Key_S: self.reset_playback_speed,
        Qt.CTRL + Qt.Key_C: self.close_media,
        Qt.Key_Up: self.increase_media_volume,
        Qt.Key_Down: self.decrease_media_volume,
        Qt.CTRL + Qt.Key_Up: self.increase_playback_speed,
        Qt.CTRL + Qt.Key_Down: self.decrease_playback_speed,
        Qt.Key_1: self.click_on_preset1,
        Qt.Key_2: self.click_on_preset2,
        Qt.Key_3: self.click_on_preset3,
        Qt.Key_4: self.click_on_preset4,
        Qt.Key_5: self.handle_frameless_window,
        Qt.Key_6: self.handle_movable_window,
        Qt.Key_7: self.handle_on_top_window,
    }

    for key, value in shortcuts.items():
        shortcut = QShortcut(QKeySequence(key), self)
        shortcut.activated.connect(value)