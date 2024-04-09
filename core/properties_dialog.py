from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
import os
import datetime
from pathlib import Path
import urllib.request

class PropertiesDlg(QDialog):
    def __init__(
        self,
        current_dir,
        name,
        settings,
        file_path,
        video_duration_ms,
        parent=None
    ):
        super().__init__(parent)

        self.current_dir = current_dir
        self.name = name
        self.window = parent
        self.settings = settings
        self.file_path = file_path
        self.video_duration_ms = video_duration_ms

        loadUi(
            f'{self.current_dir}/core/ui/properties_dialog.ui', self
        )

        self._init_window()
        self._init_content()
        self._init_connect()

    def _init_content(self):
        self.get_file_properties(self.file_path)

        self.label_2.setPixmap(QPixmap(f"{self.current_dir}/resources/icons/{self.window.theme}/info_white_24dp.svg"))

    def _init_connect(self):
        self.buttonBox.accepted.connect(self.close)

    def get_size_formatted(self, size_in_bytes):
        units = ['byte', 'KB', 'MB', 'GB']
        
        unit_index = 0
        size = size_in_bytes
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        formatted_size = "{:,.0f}".format(size).replace(",", " ")
        formatted_size_in_bytes = f"{size_in_bytes:_}".replace('_', ' ')
        return f'{formatted_size} {units[unit_index]} ({formatted_size_in_bytes} bytes)'

    def format_datetime(self, datetime_obj):
        return datetime_obj.strftime('%d %B %Y, %H:%M:%S')

    def get_file_properties(self, file_path):
        file = Path(file_path)
        self.lineEdit.setText(file.name)
        self.lineEdit.setToolTip(file.name)
        self.lineEdit.home(False)
        self.lineEdit.setCursor(Qt.IBeamCursor)

        if not file.exists() or not file.is_file():
            pass
        else:   
            file_type = file.suffix      
            directory = str(file.parent)     
            file_path = str(file)       
            file_size = os.path.getsize(file)        
            formatted_size = self.get_size_formatted(file_size)       
            created = datetime.datetime.fromtimestamp(os.path.getctime(file))
            formatted_created = self.format_datetime(created)

            self.lineEdit_5.setText(file_type)
            self.lineEdit_5.setToolTip(file_type)
            self.lineEdit_5.home(False)
            self.lineEdit_5.setCursor(Qt.IBeamCursor)

            self.lineEdit_2.setText(directory)
            self.lineEdit_2.setToolTip(directory)
            self.lineEdit_2.home(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)

            self.lineEdit_3.setText(file_path)
            self.lineEdit_3.setToolTip(file_path)
            self.lineEdit_3.home(False)
            self.lineEdit_3.setCursor(Qt.IBeamCursor)

            self.lineEdit_6.setText(formatted_size)
            self.lineEdit_6.setToolTip(formatted_size)
            self.lineEdit_6.home(False)
            self.lineEdit_6.setCursor(Qt.IBeamCursor)

            self.lineEdit_4.setText(str(self.video_duration_ms))
            self.lineEdit_4.setToolTip(str(self.video_duration_ms))
            self.lineEdit_4.home(False)
            self.lineEdit_4.setCursor(Qt.IBeamCursor)

            self.lineEdit_7.setText(formatted_created)
            self.lineEdit_7.setToolTip(formatted_created)
            self.lineEdit_7.home(False)
            self.lineEdit_7.setCursor(Qt.IBeamCursor)

    def _init_window(self):
        self.setWindowTitle(self.name)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )