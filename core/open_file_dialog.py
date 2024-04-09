from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QFileDialog,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
import os
import shutil
from urllib.parse import urlparse

class OpenFileDlg(QDialog):
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
            f'{self.current_dir}/core/ui/open_file_dialog.ui', self
        )

        self._init_window()
        self._init_content()
        self._init_connect()

    def _init_content(self):
        self.lineEdit.setText(self.file_path)
        self.lineEdit.selectAll()

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(bool(self.lineEdit.text()))

        self.label_2.setPixmap(QPixmap(f"{self.current_dir}/resources/icons/{self.window.theme}/link_white_24dp.svg"))

    def _init_connect(self):
        self.buttonBox.button(
            QDialogButtonBox.Ok
        ).clicked.connect(self.open_url_media)

        self.buttonBox.button(
            QDialogButtonBox.Cancel
        ).clicked.connect(
                self.close
            )

        self.pushButton.clicked.connect(self.choose_media_file)
        self.lineEdit.textChanged.connect(self.url_validation)

    def url_validation(self, text):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(bool(text))

    def open_url_media(self):
        self.window.playlist_cleaner()
        
        urls = self.lineEdit.text().split('; ')
        if len(urls):
            for url in urls:
                self.window.add_to_playlist(url.strip())

        if not self.checkBox.isChecked():
            self.window.open_media(urls[0].strip())

        self.close()

    def choose_media_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_names, _ = QFileDialog.getOpenFileNames(
            self,
            "Open Media Files",
            "",
            f"All Files (*)",
            options=options
        )
        if file_names:
            self.lineEdit.setText('; '.join(file_names))

    def _init_window(self):
        self.setWindowTitle(self.name)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )