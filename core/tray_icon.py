from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import requests
import sys

class TrayIcon(QSystemTrayIcon):
    def __init__(
        self,
        current_dir,
        name,
        settings,
        parent=None
    ):
        super().__init__(parent)

        self.current_dir = current_dir
        self.name = name
        self.window = parent
        self.settings = settings

        self.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )
        self.activated.connect(self.on_tray_icon_activated)
        
        if self.settings.value("hide_window_in_tray", "true") == "true":
            self.show() 
        else:
            self.hide()

        self._init_content()

    def _init_content(self):
        contextMenu = QMenu(self.window)

        menuFile = self.window.menuFile
        contextMenu.addMenu(menuFile)
        contextMenu.addSeparator()

        for action in self.window.menuPlay.actions():
            if isinstance(action, QMenu):
                contextMenu.addMenu(action.menu())
            else:
                contextMenu.addAction(action)
        contextMenu.addSeparator()         

        for action in self.window.menuNavigate.actions():
            if isinstance(action, QMenu):
                contextMenu.addMenu(action.menu())
            else:
                contextMenu.addAction(action)
        contextMenu.addSeparator()
       
        menuPlaylist = self.window.menuPlaylist
        contextMenu.addMenu(menuPlaylist)
        contextMenu.addSeparator()     

        for action in self.window.menuView.actions():
            if isinstance(action, QMenu):
                contextMenu.addMenu(action.menu())
            else:
                contextMenu.addAction(action)
        contextMenu.addSeparator()

        menuHelp = self.window.menuHelp
        contextMenu.addMenu(menuHelp)
        contextMenu.addSeparator()

        self.setContextMenu(contextMenu)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.hide_show_check()

    def hide_show_check(self):
        if self.window.isMinimized():
            self.window.showNormal()
            self.window.activateWindow()
        else:
            if self.window.isMinimized():
                self.window.showNormal()
                self.window.activateWindow()
            elif self.window.isVisible():
                self.window.hide()
            else:
                self.window.showNormal()
                self.window.activateWindow()