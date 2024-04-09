from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QMessageBox
)
from PyQt5.QtCore import Qt, QRegExp 
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.uic import loadUi

class AboutDlg(QDialog):
    def __init__(
        self,
        current_dir,
        name,
        settings,
        file_path,
        parent=None
    ):
        super().__init__(parent)

        self.current_dir = current_dir
        self.name = name
        self.window = parent
        self.settings = settings
        self.file_path = file_path

        loadUi(
            f'{self.current_dir}/core/ui/about_dialog.ui', self
        )

        self._init_window()
        self._init_content()
        self._init_connect()

    def _init_content(self):
        pass

    def _init_connect(self):
        self.buttonBox.accepted.connect(self.close) 

    def _init_window(self):
        self.setWindowTitle(self.name)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )