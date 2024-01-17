#settings_dialog.py
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox,
    QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
import os
import sys

class SettingsDlg(QDialog):
    def __init__(
        self,
        current_dir,
        name,
        settings,
        file_path,
        filter_,
        parent=None
    ):
        super().__init__(parent)

        self.current_dir = current_dir
        self.name = name
        self.window = parent
        self.settings = settings
        self.file_path = file_path
        self.filter_ = filter_

        loadUi(
            f"{self.current_dir}/core/ui/settings_dialog.ui", self
        )

        self._init_window()
        self._init_content()
        self._init_connect()

    def _init_content(self):
        self.label_2.setPixmap(QPixmap(f"{self.current_dir}/resources/icons/{self.window.icon_folder}/settings_white_24dp.svg"))

        if self.settings.value("memorize_last_window_size", "false") == "true":
            self.checkBox.setChecked(True)
        else:
            self.checkBox.setChecked(False)

        if self.settings.value("preferred_multimedia_plugins", "directshow") == "windowsmediafoundation":
            self.comboBox.setCurrentIndex(1)
        else:
            self.comboBox.setCurrentIndex(0)

        if self.settings.value("app_theme", "dark") == "dark":
            self.comboBox_2.setCurrentIndex(0)
        else:
            self.comboBox_2.setCurrentIndex(1)

        theme_style = self.settings.value("theme_style", "classic")
        if theme_style == "classic":
            self.comboBox_3.setCurrentIndex(0)
        elif theme_style == "modern":
            self.comboBox_3.setCurrentIndex(1)
        elif theme_style == "windowsvista":
            self.comboBox_3.setCurrentIndex(2)
        elif theme_style == "windows":
            self.comboBox_3.setCurrentIndex(3)
        else:
            self.comboBox_3.setCurrentIndex(4)

        if self.settings.value("search_for_updates_at_startup", "true") == "true":
            self.checkBox_2.setChecked(True)
        else:
            self.checkBox_2.setChecked(False)

    def _init_connect(self):
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.save_settings_and_close)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.cancel)

    def _init_window(self):
        self.setWindowTitle(self.name)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon(f"{self.current_dir}/resources/icons/icon.ico"))

    def save_settings_and_close(self):
        self.save_settings()
        self.close()

    def cancel(self):
        self.close()

    def save_settings(self):
        self.settings.setValue("memorize_last_window_size", str(self.checkBox.isChecked()).lower())

        preferred_plugins = "directshow" if self.comboBox.currentIndex() == 0 else "windowsmediafoundation"
        self.settings.setValue("preferred_multimedia_plugins", preferred_plugins)

        app_theme = "dark" if self.comboBox_2.currentIndex() == 0 else "light"
        self.settings.setValue("app_theme", app_theme)

        theme_style = "classic"
        index = self.comboBox_3.currentIndex()
        if index == 1:
            theme_style = "modern"
        elif index == 2:
            theme_style = "windowsvista"
        elif index == 3:
            theme_style = "windows"
        elif index == 4:
            theme_style = "fusion"
        self.settings.setValue("theme_style", theme_style)

        self.settings.setValue("search_for_updates_at_startup", str(self.checkBox_2.isChecked()).lower())

        msg = QMessageBox.question(self,
            "A reboot is required to apply settings",
            "A reboot is required to apply settings, do you really want to reboot App now?"
        )
        if msg == QMessageBox.Yes:
            self.settings.setValue("window_size", self.window.size())
            self.settings.setValue("media_volume", self.window.horizontalSlider_2.value())
            
            QApplication.quit()
            status = QProcess.startDetached(sys.executable, sys.argv) 
