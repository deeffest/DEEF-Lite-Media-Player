from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QMessageBox
)
from PyQt5.QtCore import Qt, QRegExp 
from PyQt5.QtGui import QIcon, QRegExpValidator, QPixmap
from PyQt5.uic import loadUi

class GoToDlg(QDialog):
    def __init__(
        self,
        current_dir,
        name,
        settings,
        file_path,
        current_time_fmt,
        video_duration_ms,
        parent=None
    ):
        super().__init__(parent)

        self.current_dir = current_dir
        self.name = name
        self.window = parent
        self.settings = settings
        self.file_path = file_path
        self.current_time_fmt = current_time_fmt
        self.video_duration_ms = video_duration_ms

        loadUi(
            f'{self.current_dir}/core/ui/go_to_dialog.ui', self
        )

        self._init_window()
        self._init_content()
        self._init_connect()

    def _init_content(self):
        self.lineEdit.setText(self.current_time_fmt)
        self._setup_time_validator()
        
        self.label_2.setPixmap(QPixmap(f"{self.current_dir}/resources/icons/{self.window.theme}/schedule_white_24dp.svg"))

    def _init_connect(self):
        self.buttonBox.accepted.connect(self.on_ok_clicked) 
        self.buttonBox.rejected.connect(self.close)

    def on_ok_clicked(self):
        time_text = self.lineEdit.text()
        time_ms = self._convert_time_to_ms(time_text)

        if time_ms is None:
            return

        if time_ms > self.video_duration_ms:
            QMessageBox.warning(self, "Invalid time", "The specified time exceeds the duration of the video.")
            return

        if self.window and self.window.player:
            self.window.player.setPosition(time_ms)
            self.window.player.pause()
            self.accept()

    def _setup_time_validator(self):
        time_format_regex = QRegExp("^[0-9:]*$")
        time_validator = QRegExpValidator(time_format_regex, self.lineEdit)
        self.lineEdit.setValidator(time_validator)
    
    def _convert_time_to_ms(self, time_str):
        parts = time_str.split(':')
        try:
            if len(parts) == 3:
                hours, minutes, seconds = parts
            elif len(parts) == 2:
                hours = 0
                minutes, seconds = parts
            else:
                raise ValueError("Invalid time format")

            hours, minutes, seconds = int(hours), int(minutes), int(seconds)
            return (hours * 3600 + minutes * 60 + seconds) * 1000
        except ValueError as e:
            self._show_error_message_box(f"Error converting time: {e}\nFormat: hh:mm:ss")
            return None 
      
    def _show_error_message_box(self, message):
        QMessageBox.warning(self, "Error converting time", message)

    def _init_window(self):
        self.setWindowTitle(self.name)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )