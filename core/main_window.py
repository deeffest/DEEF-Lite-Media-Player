#main_window.py
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, 
    QListWidgetItem, QShortcut, QWidget, QWidgetAction,
    QAction, QMenu
)
from PyQt5.QtGui import (
    QIcon, QKeySequence, QColor, QBrush, QPixmap
)
from PyQt5.QtMultimedia import (
    QMediaContent, QMediaPlayer, QMediaStreamsControl
)
from PyQt5.QtCore import (
    QUrl, QTimer, Qt, QProcess, QCoreApplication, QEvent,
    QSize
)
from PyQt5.QtWinExtras import (
    QWinThumbnailToolBar, QWinThumbnailToolButton  
)

from PyQt5 import uic
import os, sys
import webbrowser
import random 
import requests

from core.open_file_dialog import OpenFileDlg
from core.go_to_dialog import GoToDlg
from core.properties_dialog import PropertiesDlg
from core.settings_dialog import SettingsDlg
from core.about_dialog import AboutDlg
from core.video_widget import VideoWidget
from core.init_connect import _init_connect
from core.init_shortcuts import _init_shortcuts
from core.init_config import _init_config
from core.init_icons import _init_icons

class Window(QMainWindow):
    def __init__(
        self,
        name,
        version,
        current_dir,
        filter_,
        settings,
        file_path=None,
        parent=None
    ):
        super().__init__(parent)

        self.win_toolbar = QWinThumbnailToolBar(self)  
        self.show()

        self.name = name
        self.version = version
        self.current_dir = current_dir
        self.filter_ = filter_
        self.file_path = file_path
        self.settings = settings

        uic.loadUi(
            f"{self.current_dir}/core/ui/main_window.ui", self
        ) 

        self._init_attributes()
        self._init_window()
        self._init_content()

    def _init_content(self):
        self.player = QMediaPlayer(None)
        
        self.video_widget = VideoWidget(self)
        self.horizontalLayout.addWidget(self.video_widget)

        self.create_win_toolbar_buttons()
        self.create_playlist_menu()
        
        if self.file_path is None:
            pass
        else:
            self.open_media(self.file_path)

        _init_connect(self)
        _init_shortcuts(self)
        _init_config(self)   

    def _init_attributes(self):
        self.playback_speed = 1.0
        self.media_muted = False
        self.media_volume = self.settings.value("media_volume", 100)
        self.horizontalSlider_2.setValue(self.media_volume)

        theme = self.settings.value("app_theme", "dark")
        if theme == "dark":
            self.icon_folder = "dark_icons"
        else:
            self.icon_folder = "light_icons"
        _init_icons(self, self.icon_folder, theme=theme)

    def open_media(self, file_path):
        self.file_path = file_path
        self.setWindowTitle(f"{self.file_path} - {self.name}")
        self.label_3.setText("/")
        self.control_ui_elements(setEnabled=True)

        if file_path.lower().endswith('.m3u'):
            self.open_playlist(file_path)
        else:
            self.set_media()

    def open_playlist(self, playlist_path):   
        try:
            with open(playlist_path, 'r', encoding='utf-8') as playlist_file:
                for file_path in playlist_file:
                    file_path = file_path.strip()
                    if file_path and not file_path.startswith('#'):
                        self.add_to_playlist(file_path)

            if self.playlistUiWidget.listWidget.count() > 0:
                first_item = self.playlistUiWidget.listWidget.item(0)
                self.open_media_from_playlist(first_item)
        except Exception as e: 
            QMessageBox.critical(self, "Error opening playlist", f"Failed to open the playlist:\n{e}")
    
    def set_media(self):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_path)))
        self.player.setVideoOutput(self.video_widget)
        self.player.setVolume(self.media_volume)
        self.player.play()

        self.setCursor(Qt.ArrowCursor)
        self.set_playlist()

    def set_playlist(self):    
        item = QListWidgetItem(self.file_path)
        item.setToolTip(item.text())  

        playing_items = self.playlistUiWidget.listWidget.findItems(self.file_path, Qt.MatchExactly)
        if not playing_items:
            self.playlistUiWidget.listWidget.addItem(item)
            playing_items = self.playlistUiWidget.listWidget.findItems(self.file_path, Qt.MatchExactly)

        for i in range(self.playlistUiWidget.listWidget.count()):
            item = self.playlistUiWidget.listWidget.item(i)
            if item in playing_items:
                item.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/{self.icon_folder}/play_arrow_white_24dp.svg"
                ))
                item.setSelected(True)
            else:
                item.setIcon(QIcon())
                item.setSelected(False)

        self.check_playlist_items()
        
    def open_media_from_playlist(self, item):
        file_path = item.text() 
        self.open_media(file_path)

    def add_to_playlist(self, url):
        playing_items = self.playlistUiWidget.listWidget.findItems(url, Qt.MatchExactly)
        if not playing_items:
            item = QListWidgetItem(url)
            item.setToolTip(url)
            self.playlistUiWidget.listWidget.addItem(item)

    def playlist_cleaner(self):
        self.playlistUiWidget.listWidget.clear()
        self.close_media()

    def stop_media(self):
        self.player.stop()

    def rewind_media(self):
        position = self.player.position() 
        if position > 10000:
            self.player.setPosition(max(0, position - 10 * 1000))

    def forward_media(self):
        position = self.player.position()  
        duration = self.player.duration() 
        if duration-position > 10000:
            self.player.setPosition(min(duration, position + 10 * 1000))

    def change_media_volume(self, value):
        self.player.setVolume(value)
        self.horizontalSlider_2.setValue(value)
        self.media_volume = value
            
        if self.media_volume <= 0:
            self.actionDown_2.setEnabled(False)
            self.actionUp_2.setEnabled(True)

        elif self.media_volume >= 100:
            self.actionUp_2.setEnabled(False)
            self.actionDown_2.setEnabled(True)

    def toggle_media_repeat(self, checked=None):
        if checked:
            self.actionRepeat.setChecked(True)
        elif checked == False:
            self.actionRepeat.setChecked(False)
        elif checked is None:     
            if self.actionRepeat.isChecked():
                self.actionRepeat.setChecked(False)
            else:
                self.actionRepeat.setChecked(True)

    def play_pause_media(self, event=None):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()

        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()

        elif self.player.state() == QMediaPlayer.StoppedState:
            if self.file_path is not None:
                self.open_media(self.file_path)

    def check_media_state(self, status):
        if status == QMediaPlayer.PlayingState:
            self.toolButton_2.setChecked(False)
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/dark_icons/pause_white_24dp.svg"
            ))
            self.actionPlay_Pause.setChecked(False)

        elif status == QMediaPlayer.PausedState:
            self.toolButton_2.setChecked(True)
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/dark_icons/play_arrow_white_24dp.svg"
            ))
            self.actionPlay_Pause.setChecked(True)

        elif status == QMediaPlayer.StoppedState:
            self.toolButton_2.setChecked(True)
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/dark_icons/play_arrow_white_24dp.svg"
            ))
            self.actionPlay_Pause.setChecked(True)

    def check_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            if self.actionRepeat.isChecked():
                if self.file_path is not None:
                    self.open_media(self.file_path)
            elif self.actionAutoPlay.isChecked():
                if self.file_path is not None:
                    self.open_next_media()
            self.label.setText("End Of Media")

        if status == QMediaPlayer.LoadingMedia:
            self.label.setText("Loading Media")
        if status == QMediaPlayer.LoadedMedia:
            self.label.setText("Loaded Media")
        if status == QMediaPlayer.StalledMedia:
            self.label.setText("Stalled Media")
        if status == QMediaPlayer.BufferingMedia:
            self.label.setText("Buffering Media")
        if status == QMediaPlayer.BufferedMedia:
            self.label.setText("Buffered Media")
        if status == QMediaPlayer.InvalidMedia:
            self.label.setText("Invalid Media")

    def handle_media_errors(self, error):
        error_message = self.player.errorString()

        if error == QMediaPlayer.ResourceError:
            self.label.setText(f"Resource Error: {error_message}")
        elif error == QMediaPlayer.FormatError:
            self.label.setText(f"Format Error: {error_message}")
        elif error == QMediaPlayer.NetworkError:
            self.label.setText(f"Network Error: {error_message}")
        elif error == QMediaPlayer.AccessDeniedError:
            self.label.setText(f"Access Denied Error: {error_message}")
        else:
            self.label.setText(f"Unknown Error: {error_message}")

    def shuffle_playlist(self):
        items = []
        for index in range(self.playlistUiWidget.listWidget.count()):
            items.append(self.playlistUiWidget.listWidget.takeItem(0))
        
        random.shuffle(items)
        
        for item in items:    
            self.playlistUiWidget.listWidget.addItem(item)
            for i in range(self.playlistUiWidget.listWidget.count()):
                playing_items = self.playlistUiWidget.listWidget.findItems(self.file_path, Qt.MatchExactly)
                item = self.playlistUiWidget.listWidget.item(i)
                if item in playing_items:
                    item.setIcon(QIcon(
                        f"{self.current_dir}/resources/icons/{self.icon_folder}/play_arrow_white_24dp.svg"
                    ))
                    item.setSelected(True)
                else:
                    item.setIcon(QIcon())
                    item.setSelected(False)

    def save_playlist_as_m3u(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Playlist", 
            "", 
            "M3U Playlist (*.m3u)"
        )
        if not file_name:
            return
        
        with open(file_name, 'w', encoding='utf-8') as playlist_file:
            for index in range(self.playlistUiWidget.listWidget.count()):
                item = self.playlistUiWidget.listWidget.item(index)
                playlist_file.write(f"{item.text()}\n")

    def open_settings_dialog(self):
        Dlg = SettingsDlg(
            self.current_dir,
            self.name,
            self.settings, 
            self.file_path, 
            self.filter_,
            parent=self
            )
        Dlg.exec_()

    def handle_on_top_window(self, checked=None):
        if checked:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.settings.setValue("on_top_window", True) 
        elif checked == False:
            self.setWindowFlags(Qt.Window)
            self.settings.setValue("on_top_window", False)  
        elif checked is None:
            if self.actionOn_Top.isChecked():
                self.setWindowFlags(Qt.Window)
                self.settings.setValue("on_top_window", False) 
                self.actionOn_Top.setChecked(False) 
            else:                
                self.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.settings.setValue("on_top_window", True)
                self.actionOn_Top.setChecked(True)
        self.show()

    def handle_movable_window(self, checked=None):
        if checked:
            self.settings.setValue("movable_window", True) 
        elif checked == False:
            self.settings.setValue("movable_window", False) 
        elif checked is None:
            if self.actionMovable.isChecked():
                self.settings.setValue("movable_window", False)
                self.actionMovable.setChecked(False) 
            else:
                self.settings.setValue("movable_window", True) 
                self.actionMovable.setChecked(True) 

    def handle_frameless_window(self, checked=None):
        if checked:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.settings.setValue("frameless_window", True) 
        elif checked == False:
            self.setWindowFlags(Qt.Window)
            self.settings.setValue("frameless_window", False)  
        elif checked is None:
            if self.actionFrameless.isChecked():
                self.setWindowFlags(Qt.Window)
                self.settings.setValue("frameless_window", False) 
                self.actionFrameless.setChecked(False) 
            else:                
                self.setWindowFlags(Qt.FramelessWindowHint)
                self.settings.setValue("frameless_window", True)
                self.actionFrameless.setChecked(True)
        self.show()

    def open_fullscreen(self):   
        if self.isFullScreen():
            self.showNormal()
            self.actionFullscreen.setChecked(False)

            if self.settings.value("preset_1", False) == "false":
                self.menubar.show()
            if self.settings.value("preset_2", False) == "false":
                self.frame_3.show()
            if self.settings.value("preset_3", False) == "false":
                self.frame.show()
            if self.settings.value("preset_4", False) == "false":
                self.frame_2.show()
        else:
            self.showFullScreen()
            self.actionFullscreen.setChecked(True)
            
            self.menubar.hide()
            self.frame_3.hide()
            self.frame.hide()
            self.frame_2.hide()

    def increase_media_volume(self):
        if self.media_volume < 100:
            self.media_volume += 25
            if self.media_volume >= 100:
                self.media_volume = 100
                self.actionUp_2.setEnabled(False)
            self.actionDown_2.setEnabled(True)

        self.change_media_volume(self.media_volume)

    def decrease_media_volume(self):
        if self.media_volume > 0:
            self.media_volume -= 25
            if self.media_volume <= 0:
                self.media_volume = 0
                self.actionDown_2.setEnabled(False)
            self.actionUp_2.setEnabled(True)
        
        self.change_media_volume(self.media_volume)

    def toggle_media_mute(self):
        self.media_muted = not self.media_muted
        self.player.setMuted(self.media_muted)

        self.actionMute_Unmute_2.setChecked(self.media_muted)
        self.toolButton_4.setChecked(self.media_muted)

    def increase_playback_speed(self):
        if self.playback_speed >= 1.0:
            self.playback_speed += 0.5
            if self.playback_speed >= 2.0:
                self.playback_speed = 2.0
                self.actionUp_3.setEnabled(False)
            self.actionDown_3.setEnabled(True)
        else:
            self.playback_speed += 0.25000
            if self.playback_speed >= 2.0:
                self.playback_speed = 2.0
                self.actionUp_3.setEnabled(False)
            self.actionDown_3.setEnabled(True)

        self.set_media_speed()

    def decrease_playback_speed(self):
        if self.playback_speed <= 1.0:
            self.playback_speed -= 0.25000
            if self.playback_speed <= 0.5:
                self.playback_speed = 0.5
                self.actionDown_3.setEnabled(False)
            self.actionUp_3.setEnabled(True)
        else:
            self.playback_speed -= 0.5
            if self.playback_speed <= 0.5:
                self.playback_speed = 0.5
                self.actionDown_3.setEnabled(False)
            self.actionUp_3.setEnabled(True)
        
        self.set_media_speed()

    def reset_playback_speed(self):
        self.playback_speed = 1.0
        self.actionUp_3.setEnabled(True)
        self.actionDown_3.setEnabled(True)

        self.set_media_speed()

    def open_previous_media(self):         
        current_row = self.get_current_playlist_row()
        if current_row > 0:
            prev_item = self.playlistUiWidget.listWidget.item(current_row - 1)
            self.open_media_from_playlist(prev_item)     

    def open_next_media(self):
        current_row = self.get_current_playlist_row()
        total_rows = self.playlistUiWidget.listWidget.count()
        if current_row < total_rows - 1:
            next_item = self.playlistUiWidget.listWidget.item(current_row + 1)
            self.open_media_from_playlist(next_item)

    def get_current_playlist_row(self):
        for i in range(self.playlistUiWidget.listWidget.count()):
            item = self.playlistUiWidget.listWidget.item(i)
            if item.text() == self.file_path:
                return i
        return -1

    def create_playlist_menu(self):
        self.playlistUiWidget = QWidget()
        uic.loadUi(f'{self.current_dir}/core/ui/playlist_frame.ui', self.playlistUiWidget)

        widgetAction = QWidgetAction(self.menuPlaylist)
        widgetAction.setDefaultWidget(self.playlistUiWidget)
        self.playlistUiWidget.listWidget.itemDoubleClicked.connect(self.open_media_from_playlist)
        self.playlistUiWidget.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playlistUiWidget.listWidget.customContextMenuRequested.connect(self.on_context_menu)

        if self.menuPlaylist.actions():
            firstAction = self.menuPlaylist.actions()[0]
            self.menuPlaylist.insertAction(firstAction, widgetAction)

    def on_context_menu(self, position):        
        item = self.playlistUiWidget.listWidget.currentItem()
        row = self.playlistUiWidget.listWidget.row(item)
        if item is None:
            return

        menu = QMenu()
        open_action = menu.addAction("Open File")
        menu.addSeparator()
        remove_action = menu.addAction("Remove from Playlist")
        action = menu.exec_(self.playlistUiWidget.listWidget.viewport().mapToGlobal(position))
        
        if action == open_action:
            self.open_media_from_playlist(item)
        elif action == remove_action:
            if item.text() == self.file_path:
                count = self.playlistUiWidget.listWidget.count()
                if row < count - 1:
                    self.open_next_media()
                elif count > 1:
                    self.open_previous_media()
                else:
                    self.playlist_cleaner()
                    return
            self.playlistUiWidget.listWidget.takeItem(row)

    def check_playlist_items(self):
        num_items = self.playlistUiWidget.listWidget.count()

        if num_items > 0:
            self.actionSave_As.setEnabled(True)
            self.actionClear.setEnabled(True)
            self.actionShuffle.setEnabled(True)
        else:
            self.actionSave_As.setEnabled(False)
            self.actionClear.setEnabled(False)
            self.actionShuffle.setEnabled(False)

    def set_media_speed(self):
        self.player.setPlaybackRate(self.playback_speed)

    def close_media(self):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(None)))
        self.player.setVideoOutput(self.video_widget)

        self.video_widget.hide()
        self.video_widget.show()

        self.toolButton_2.setChecked(False)
        self.control_ui_elements(setEnabled=False)
        self.setWindowTitle(self.name)
        self.file_path = None

        status_labels = [
            self.label,
            self.label_2,
            self.label_3,
            self.label_4
        ]
        for status_label in status_labels:
            status_label.setText("")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Media File",
            "",
            f"Media Files ({self.filter_});;All Files (*)",
            options=options
        )
        if file_name:
            self.open_media(file_name)

    def open_folder_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(
            self,
            "Open Folder",
            "",
            options=options
        )
        if directory:     
            file_paths = []

            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    ext = file_path.rsplit(".", 1)[-1].lower()

                    if ext in self.filter_ and ext != "m3u":
                        file_paths.append(file_path)

            if file_paths:
                self.playlistUiWidget.listWidget.clear()
                for path in file_paths:
                    self.add_to_playlist(path)
                self.open_media(file_paths[0])

    def control_ui_elements(self, setEnabled):
        ui_elements = [
            self.horizontalSlider,
            self.toolButton_5,
            self.toolButton_2,
            self.toolButton_9,
            self.toolButton_6,
            self.actionPlay_Pause,
            self.actionStop,
            self.actionPrevious_2,
            self.actionNext_2,
            self.actionRewind,
            self.actionForward,
            self.actionGo_To,
            self.tool_btn_previous,
            self.tool_btn_play_pause,
            self.tool_btn_next,
            self.actionProperties,
            self.actionClose,
            self.toolButton,
            self.toolButton_3
        ]
        for element in ui_elements:
            element.setEnabled(setEnabled)

        if setEnabled:
            self.tool_btn_previous.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/dark_icons/skip_previous_white_24dp.svg"
            ))
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/dark_icons/pause_white_24dp.svg"
            ))     
            self.tool_btn_next.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/dark_icons/skip_next_white_24dp.svg"
            ))
        else:
            self.tool_btn_previous.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_icons/skip_previous_white_24dp.svg"
            ))
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_icons/pause_white_24dp.svg"
            ))  
            self.tool_btn_next.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_icons/skip_next_white_24dp.svg"
            ))
            self.check_playlist_items()
            for i in range(self.playlistUiWidget.listWidget.count()):
                item = self.playlistUiWidget.listWidget.item(i)
                if item:
                    item.setIcon(QIcon(None))
                    item.setSelected(False)

    def create_win_toolbar_buttons(self):
        self.tool_btn_previous = QWinThumbnailToolButton(self.win_toolbar)
        self.tool_btn_previous.setToolTip('Previous')
        self.tool_btn_previous.setEnabled(False)
        self.tool_btn_previous.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/disabled_icons/skip_previous_white_24dp.svg"
        ))
        self.win_toolbar.addButton(self.tool_btn_previous)

        self.tool_btn_play_pause = QWinThumbnailToolButton(self.win_toolbar)
        self.tool_btn_play_pause.setToolTip('Play/Pause')
        self.tool_btn_play_pause.setEnabled(False)
        self.tool_btn_play_pause.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/disabled_icons/pause_white_24dp.svg"
        ))                     
        self.win_toolbar.addButton(self.tool_btn_play_pause)

        self.tool_btn_next = QWinThumbnailToolButton(self.win_toolbar)
        self.tool_btn_next.setToolTip('Next')
        self.tool_btn_next.setEnabled(False)
        self.tool_btn_next.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/disabled_icons/skip_next_white_24dp.svg"
        ))
        self.win_toolbar.addButton(self.tool_btn_next)

    def handle_on_top_window(self, checked=None):
        if checked:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.settings.setValue("on_top_window", True) 
        elif checked == False:
            self.setWindowFlags(Qt.Window)
            self.settings.setValue("on_top_window", False)  
        elif checked is None:
            if self.actionOn_Top.isChecked():
                self.setWindowFlags(Qt.Window)
                self.settings.setValue("on_top_window", False) 
                self.actionOn_Top.setChecked(False) 
            else:                
                self.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.settings.setValue("on_top_window", True)
                self.actionOn_Top.setChecked(True)

    def click_on_preset1(self, checked=None):
        if checked:
            self.menubar.hide()
            self.settings.setValue("preset_1", True) 
        elif checked == False:
            self.menubar.show()
            self.settings.setValue("preset_1", False) 
        elif checked is None:
            if self.actionPreset1.isChecked():
                self.menubar.show()
                self.settings.setValue("preset_1", False) 
                self.actionPreset1.setChecked(False)
            else:                
                self.menubar.hide()
                self.settings.setValue("preset_1", True) 
                self.actionPreset1.setChecked(True)

    def click_on_preset2(self, checked=None):
        if checked:
            self.frame_3.hide() 
            self.settings.setValue("preset_2", True)
        elif checked == False:
            self.frame_3.show() 
            self.settings.setValue("preset_2", False)
        elif checked is None:
            if self.actionPreset2.isChecked():
                self.frame_3.show() 
                self.settings.setValue("preset_2", False)
                self.actionPreset2.setChecked(False)
            else:                
                self.frame_3.hide() 
                self.settings.setValue("preset_2", True)
                self.actionPreset2.setChecked(True)

    def click_on_preset3(self, checked=None):
        if checked:
            self.frame.hide()
            self.settings.setValue("preset_3", True)
        elif checked == False:
            self.frame.show() 
            self.settings.setValue("preset_3", False)
        elif checked is None:
            if self.actionPreset3.isChecked():
                self.frame.show() 
                self.settings.setValue("preset_3", False)
                self.actionPreset3.setChecked(False)
            else:                
                self.frame.hide() 
                self.settings.setValue("preset_3", True)
                self.actionPreset3.setChecked(True)

    def click_on_preset4(self, checked=None):
        if checked:
            self.frame_2.hide()
            self.settings.setValue("preset_4", True)
        elif checked == False:
            self.frame_2.show() 
            self.settings.setValue("preset_4", False)
        elif checked is None:
            if self.actionPreset4.isChecked():
                self.frame_2.show() 
                self.settings.setValue("preset_4", False)
                self.actionPreset4.setChecked(False)
            else:                
                self.frame_2.hide() 
                self.settings.setValue("preset_4", True)
                self.actionPreset4.setChecked(True)

    def on_slider_moved(self, event):
        pos = event.pos().x()
        slider_width = self.horizontalSlider.width() 
        max_val = min(self.horizontalSlider.maximum(), self.player.duration())  # get the slider max value

        slider_val = max_val * (pos / slider_width)
        slider_val = min(max_val, max(0, slider_val))

        self.horizontalSlider.setValue(slider_val)  
        self.set_media_position(slider_val)        

    def on_slider_pressed(self, event):
        pos = event.pos().x() 
        slider_width = self.horizontalSlider.width()
        max_val = min(self.horizontalSlider.maximum(), self.player.duration())  # get slider max value

        slider_val = max_val * (pos / slider_width)
        slider_val = min(max_val, max(0, slider_val))

        self.horizontalSlider.setValue(slider_val) 
        self.set_media_position(slider_val)

    def on_volume_slider_pressed(self, event):
        pos = event.pos().x() 
        slider_width = self.horizontalSlider_2.width()
        max_val = self.horizontalSlider_2.maximum()

        slider_val = max_val * (pos / slider_width)
        slider_val = min(max_val, max(0, slider_val))

        self.horizontalSlider_2.setValue(slider_val)
        self.change_media_volume(slider_val)

    def on_volume_slider_moved(self, event):
        pos = event.pos().x() 
        slider_width = self.horizontalSlider_2.width()
        max_val = self.horizontalSlider_2.maximum()

        slider_val = max_val * (pos / slider_width)
        slider_val = min(max_val, max(0, slider_val))

        self.horizontalSlider_2.setValue(slider_val) 
        self.change_media_volume(slider_val)

    def set_media_position(self, position):
        self.player.setPosition(position)

    def format_time(self, ms, show_hours=False):
        s = ms // 1000
        m = s // 60
        h = m // 60
        s = s % 60
        m = m % 60
        if show_hours:
            return "{:01d}:{:02d}:{:02d}".format(h, m, s)
        else:
            if h == 0:
                return "{:02d}:{:02d}".format(m, s)
            else:
                return "{:01d}:{:02d}:{:02d}".format(h, m, s)

    def update_media_duration(self, duration):
        show_hours = duration >= 3600000  
        self.horizontalSlider.setMaximum(duration)
        formatted_time = self.format_time(duration, show_hours)
        self.label_4.setText(formatted_time)

    def update_media_position(self, position): 
        duration = self.player.duration()
        show_hours = duration >= 3600000 
        formatted_time = self.format_time(position, show_hours)
        self.label_2.setText(formatted_time)
        self.horizontalSlider.setValue(position)

    def open_go_to_dialog(self):
        duration = self.player.duration()
        show_hours = duration >= 3600000 
        current_time_fmt = self.format_time(self.player.position(), show_hours)

        Dlg = GoToDlg(
            self.current_dir,
            self.name,
            self.settings, 
            self.file_path, 
            self.filter_,
            current_time_fmt,
            duration,
            parent=self
            )
        Dlg.exec_()

    def open_media_dialog(self):
        Dlg = OpenFileDlg(
            self.current_dir,
            self.name,
            self.settings, 
            self.file_path, 
            self.filter_,
            parent=self
            )
        Dlg.exec_()

    def open_properties_dialog(self):
        if self.file_path is not None:
            video_duration_ms = self.format_time(self.player.duration())
            
            Dlg = PropertiesDlg(
                self.current_dir,
                self.name,
                self.settings, 
                self.file_path, 
                self.filter_,
                video_duration_ms,
                parent=self
                )
            Dlg.exec_()

    def open_about_dialog(self):
        Dlg = AboutDlg(
            self.current_dir,
            self.name,
            self.settings, 
            self.file_path, 
            self.filter_,
            parent=self
            )
        Dlg.exec_()

    def check_for_updates(self, startup=None):
        response = requests.get(
            "https://api.github.com/repos/deeffest/DEEF-Lite-Media-Player/releases/latest"
        )
        try:
            item_version = response.json()["name"]
            item_download = response.json().get("html_url")         

            if item_version != self.version:
                update_msg_box = QMessageBox(self)
                update_msg_box.setIcon(QMessageBox.Information)
                update_msg_box.setText(f"The new version of DLMPlayer is out.\n\nYour version: {self.version}\nNew version: {item_version}\n\nWould you like to update now?")
                update_msg_box.setWindowTitle("New update is available!")

                btn_update = update_msg_box.addButton("Update", QMessageBox.AcceptRole)
                btn_cancel = update_msg_box.addButton("Cancel", QMessageBox.RejectRole)
                
                update_msg_box.setDefaultButton(btn_update)
                
                ret = update_msg_box.exec()

                if update_msg_box.clickedButton() == btn_update:
                    webbrowser.open_new_tab(item_download)
            else:
                if not startup:
                    QMessageBox.information(self, 
                        "No new versions found:(", 
                        f"No new versions of DLMPlayer were found.\n\nYour version: {self.version}\nLatest version: {item_version}")
        except Exception as e:
            QMessageBox.critical(self, 
                "Error when searching for updates", 
                f"An error occurred while trying to check for updates: {e}"
            )

    def _init_window(self):       
        self.setWindowTitle(self.name)
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )    
        if self.settings.value("memorize_last_window_size", "false") == "true":
            size = self.settings.value("window_size")
        else:
            size = QSize(800,600)
        self.resize(size)
        self._move_window_to_center()
        self.raise_()
        self.activateWindow()

        if self.settings.value("search_for_updates_at_startup", "true") == "true":
            self.check_for_updates(startup=True)

    def _move_window_to_center(self):    
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.win_toolbar.window():
            self.win_toolbar.setWindow(self.windowHandle())

    def closeEvent(self, event):
        self.settings.setValue("window_size", self.size())
        self.settings.setValue("media_volume", self.horizontalSlider_2.value())
        event.accept()