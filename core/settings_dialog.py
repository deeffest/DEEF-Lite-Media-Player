from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QApplication
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
        self.label_2.setPixmap(QPixmap(f"{self.current_dir}/resources/icons/{self.window.theme}/settings_white_24dp.svg"))

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

        if self.settings.value("search_for_updates_at_startup", "true") == "true":
            self.checkBox_4.setChecked(True)
        else:
            self.checkBox_4.setChecked(False)

        if self.settings.value("hide_window_in_tray", "false") == "true":
            self.checkBox_3.setChecked(True)
        else:
            self.checkBox_3.setChecked(False)

    def _init_connect(self):
        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.save_settings_and_close)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.cancel)
        self.pushButton.clicked.connect(self.restart)

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

        self.settings.setValue("search_for_updates_at_startup", str(self.checkBox_4.isChecked()).lower())

        self.settings.setValue("hide_window_in_tray", str(self.checkBox_3.isChecked()).lower())
        if self.checkBox_3.isChecked():
            self.window.tray_icon.show()
        else:
            self.window.tray_icon.hide()

        self.settings.setValue("window_size", self.window.size())
        self.settings.setValue("media_volume", self.window.horizontalSlider_2.value())

    def restart(self):
        self.save_settings()

        QApplication.quit()
        status = QProcess.startDetached(sys.executable, sys.argv)
