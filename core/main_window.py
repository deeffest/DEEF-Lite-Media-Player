import os, sys
import webbrowser
import random 
import requests
import mimetypes

from PyQt5.QtWidgets import (
    qApp, QMainWindow, QFileDialog, QMessageBox,
    QListWidgetItem, QWidget, QWidgetAction, 
    QMenu
)
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import (
    QMediaContent, QMediaPlayer
)
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtWinExtras import (
    QWinThumbnailToolBar, QWinThumbnailToolButton  
)
from PyQt5 import uic

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
from core.init_styles import _init_styles
from core.tray_icon import TrayIcon

class Window(QMainWindow):
    def __init__(
        self,
        name,
        version,
        current_dir,
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
        self._init_tray_icon()

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
        self.change_media_volume(value=None, player=False)
        self.horizontalSlider_2.setValue(self.media_volume)
        self.setAcceptDrops(True)

        self.theme = self.settings.value("app_theme", "dark")
        _init_icons(self, theme=self.theme)
        _init_styles(self)

    def open_media(self, file_path):
        if not self.is_media_file(file_path):
            return
        self.file_path = file_path
        self.setWindowTitle(f"{self.file_path} - {self.name}")
        self.tray_icon.setToolTip(self.file_path)
        self.label_3.setText("/")
        self.control_ui_elements(setEnabled=True)
        
        if file_path.lower().endswith('.m3u'):
            self.open_playlist(file_path)
        else:
            self.set_media()

    def is_media_file(self, file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is not None:
            return mime_type.startswith('video/') or mime_type.startswith('audio/')
        else:
            return False

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

        self.video_widget.hide()
        self.video_widget.show()

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
                    f"{self.current_dir}/resources/icons/{self.theme}/play_arrow_white_24dp.svg"
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

    def change_media_volume(self, value=None, player=None):
        if player:
            self.player.setVolume(int(value))
        if value:
            self.horizontalSlider_2.setValue(int(value))
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
                f"{self.current_dir}/resources/icons/dark/pause_white_24dp.svg"
            ))
            self.actionPlay_Pause.setChecked(False)

        elif status == QMediaPlayer.PausedState:
            self.toolButton_2.setChecked(True)
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/dark/play_arrow_white_24dp.svg"
            ))
            self.actionPlay_Pause.setChecked(True)

        elif status == QMediaPlayer.StoppedState:
            self.toolButton_2.setChecked(True)
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/dark/play_arrow_white_24dp.svg"
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
                        f"{self.current_dir}/resources/icons/{self.theme}/play_arrow_white_24dp.svg"
                    ))
                    item.setSelected(True)
                else:
                    item.setIcon(QIcon())
                    item.setSelected(False)

    def save_playlist_as_m3u(self):
        self.show()

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
        self.show()
        Dlg = SettingsDlg(
            self.current_dir,
            self.name,
            self.settings, 
            self.file_path, 
            parent=self
            )
        Dlg.exec_()

    def handle_on_top_window(self, checked=None):
        if checked:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.settings.setValue("on_top_window", "true")
        elif checked == False:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.settings.setValue("on_top_window", "false")
        elif checked is None:
            if self.actionOn_Top.isChecked():
                self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
                self.settings.setValue("on_top_window", "true")
                self.actionOn_Top.setChecked(False) 
            else:
                self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
                self.settings.setValue("on_top_window", "true")
                self.actionOn_Top.setChecked(True)
        self.show()

    def handle_movable_window(self, checked=None):
        if checked:
            self.settings.setValue("movable_window", "true") 
        elif checked == False:
            self.settings.setValue("movable_window", "false") 
        elif checked is None:
            if self.actionMovable.isChecked():
                self.settings.setValue("movable_window", "false")
                self.actionMovable.setChecked(False) 
            else:
                self.settings.setValue("movable_window", "true") 
                self.actionMovable.setChecked(True) 

    def handle_frameless_window(self, checked=None):
        if checked:
            self.setWindowFlag(Qt.FramelessWindowHint, True)
            self.settings.setValue("frameless_window", "true")
        elif checked == False:
            self.setWindowFlag(Qt.FramelessWindowHint, False)
            self.settings.setValue("frameless_window", "false")
        elif checked is None:
            if self.actionFrameless.isChecked():
                self.setWindowFlag(Qt.FramelessWindowHint, False)
                self.settings.setValue("frameless_window", "false")
                self.actionFrameless.setChecked(False)
            else:
                self.setWindowFlag(Qt.FramelessWindowHint, True)
                self.settings.setValue("frameless_window", "true")
                self.actionFrameless.setChecked(True)
        self.show()

    def open_fullscreen(self):   
        if self.isFullScreen():
            self.showNormal()
            self.actionFullscreen.setChecked(False)

            if self.settings.value("preset_1", "false") == "false":
                self.menubar.show()
            if self.settings.value("preset_2", "false") == "false":
                self.frame_3.show()
            if self.settings.value("preset_3", "false") == "false":
                self.frame.show()
            if self.settings.value("preset_4", "false") == "false":
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
            self.media_volume += 15
            if self.media_volume >= 100:
                self.media_volume = 100
                self.actionUp_2.setEnabled(False)
            self.actionDown_2.setEnabled(True)

        self.change_media_volume(self.media_volume, player=True)

    def decrease_media_volume(self):
        if self.media_volume > 0:
            self.media_volume -= 15
            if self.media_volume <= 0:
                self.media_volume = 0
                self.actionDown_2.setEnabled(False)
            self.actionUp_2.setEnabled(True)
        
        self.change_media_volume(self.media_volume, player=True)

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
        open_action = menu.addAction("Play")
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
        self.show()

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Media File",
            "",
            f"All Files (*)",
            options=options
        )
        if file_name:
            self.playlist_cleaner()
            self.open_media(file_name)

    def open_folder_dialog(self):
        self.show()

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

            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path) and self.is_media_file(file_path):
                    ext = file_path.rsplit(".", 1)[-1].lower()
                    if ext != "m3u":
                        file_paths.append(file_path)

            if file_paths:
                self.playlist_cleaner()
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
                f"{self.current_dir}/resources/icons/dark/skip_previous_white_24dp.svg"
            ))
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/dark/pause_white_24dp.svg"
            ))     
            self.tool_btn_next.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/dark/skip_next_white_24dp.svg"
            ))
        else:
            self.tool_btn_previous.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled/skip_previous_white_24dp.svg"
            ))
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled/pause_white_24dp.svg"
            ))  
            self.tool_btn_next.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled/skip_next_white_24dp.svg"
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
            f"{self.current_dir}/resources/icons/disabled/skip_previous_white_24dp.svg"
        ))
        self.win_toolbar.addButton(self.tool_btn_previous)

        self.tool_btn_play_pause = QWinThumbnailToolButton(self.win_toolbar)
        self.tool_btn_play_pause.setToolTip('Play/Pause')
        self.tool_btn_play_pause.setEnabled(False)
        self.tool_btn_play_pause.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/disabled/pause_white_24dp.svg"
        ))                     
        self.win_toolbar.addButton(self.tool_btn_play_pause)

        self.tool_btn_next = QWinThumbnailToolButton(self.win_toolbar)
        self.tool_btn_next.setToolTip('Next')
        self.tool_btn_next.setEnabled(False)
        self.tool_btn_next.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/disabled/skip_next_white_24dp.svg"
        ))
        self.win_toolbar.addButton(self.tool_btn_next)

    def _init_tray_icon(self):
        self.tray_icon = TrayIcon(            
            self.current_dir,
            self.name,
            self.settings, 
            parent=self
        )

    def click_on_preset1(self, checked=None):
        if checked:
            self.menubar.hide()
            self.settings.setValue("preset_1", "true") 
        elif checked == False:
            self.menubar.show()
            self.settings.setValue("preset_1", "false") 
        elif checked is None:
            if self.actionPreset1.isChecked():
                self.menubar.show()
                self.settings.setValue("preset_1", "false") 
                self.actionPreset1.setChecked(False)
            else:                
                self.menubar.hide()
                self.settings.setValue("preset_1", "true") 
                self.actionPreset1.setChecked(True)

    def click_on_preset2(self, checked=None):
        if checked:
            self.frame_3.hide() 
            self.settings.setValue("preset_2", "true")
        elif checked == False:
            self.frame_3.show() 
            self.settings.setValue("preset_2", "false")
        elif checked is None:
            if self.actionPreset2.isChecked():
                self.frame_3.show() 
                self.settings.setValue("preset_2", "false")
                self.actionPreset2.setChecked(False)
            else:                
                self.frame_3.hide() 
                self.settings.setValue("preset_2", "true")
                self.actionPreset2.setChecked(True)

    def click_on_preset3(self, checked=None):
        if checked:
            self.frame.hide()
            self.settings.setValue("preset_3", "true")
        elif checked == False:
            self.frame.show() 
            self.settings.setValue("preset_3", "false")
        elif checked is None:
            if self.actionPreset3.isChecked():
                self.frame.show() 
                self.settings.setValue("preset_3", "false")
                self.actionPreset3.setChecked(False)
            else:                
                self.frame.hide() 
                self.settings.setValue("preset_3", "true")
                self.actionPreset3.setChecked(True)

    def click_on_preset4(self, checked=None):
        if checked:
            self.frame_2.hide()
            self.settings.setValue("preset_4", "true")
        elif checked == False:
            self.frame_2.show() 
            self.settings.setValue("preset_4", "false")
        elif checked is None:
            if self.actionPreset4.isChecked():
                self.frame_2.show() 
                self.settings.setValue("preset_4", "false")
                self.actionPreset4.setChecked(False)
            else:                
                self.frame_2.hide() 
                self.settings.setValue("preset_4", "true")
                self.actionPreset4.setChecked(True)

    def on_slider_enter(self, event):
        pos = event.pos().x()
        slider_width = self.horizontalSlider.width() 
        max_val = min(self.horizontalSlider.maximum(), self.player.duration())

        slider_val = max_val * (pos / slider_width)
        slider_val = min(max_val, max(0, slider_val))

        self.horizontalSlider.setToolTip(self.format_time(slider_val))

    def on_slider_moved(self, event):
        pos = event.pos().x()
        slider_width = self.horizontalSlider.width() 
        max_val = min(self.horizontalSlider.maximum(), self.player.duration())

        slider_val = max_val * (pos / slider_width)
        slider_val = min(max_val, max(0, slider_val))

        self.horizontalSlider.setValue(int(slider_val))  
        self.set_media_position(slider_val)

    def on_slider_pressed(self, event):
        pos = event.pos().x()
        slider_width = self.horizontalSlider.width()
        max_val = min(self.horizontalSlider.maximum(), self.player.duration())

        slider_val = max_val * (pos / slider_width)
        slider_val = min(max_val, max(0, slider_val))

        self.horizontalSlider.setValue(int(slider_val))
        self.set_media_position(slider_val)

    def on_volume_slider_pressed(self, event):
        pos = event.pos().x() 
        slider_width = self.horizontalSlider_2.width()
        max_val = self.horizontalSlider_2.maximum()
        slider_val = max_val * (pos / slider_width)
        slider_val = min(max_val, max(0, slider_val))

        self.horizontalSlider_2.setValue(int(slider_val))

        self.change_media_volume(slider_val, player=True)

    def on_volume_slider_moved(self, event):
        pos = event.pos().x() 
        slider_width = self.horizontalSlider_2.width()
        max_val = self.horizontalSlider_2.maximum()

        slider_val = max_val * (pos / slider_width)
        slider_val = min(max_val, max(0, slider_val))

        self.horizontalSlider_2.setValue(int(slider_val)) 
        self.change_media_volume(slider_val, player=True)

    def set_media_position(self, position):
        self.player.setPosition(int(position))

    def format_time(self, ms, show_hours=False):
        s = ms // 1000
        m = s // 60
        h = m // 60
        s = s % 60
        m = m % 60

        s = int(s)
        m = int(m)
        h = int(h)

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
        self.horizontalSlider.setValue(max(0, min(position, 2147483647)))

    def open_go_to_dialog(self):
        duration = self.player.duration()
        show_hours = duration >= 3600000 
        current_time_fmt = self.format_time(self.player.position(), show_hours)

        self.show()
        Dlg = GoToDlg(
            self.current_dir,
            self.name,
            self.settings, 
            self.file_path, 
            current_time_fmt,
            duration,
            parent=self
            )
        Dlg.exec_()

    def open_media_dialog(self):
        self.show()

        Dlg = OpenFileDlg(
            self.current_dir,
            self.name,
            self.settings, 
            self.file_path, 
            parent=self
            )
        Dlg.exec_()

    def open_properties_dialog(self):
        if self.file_path is not None:
            video_duration_ms = self.format_time(self.player.duration())
            
            self.show()
            Dlg = PropertiesDlg(
                self.current_dir,
                self.name,
                self.settings, 
                self.file_path, 
                video_duration_ms,
                parent=self
                )
            Dlg.exec_()

    def open_about_dialog(self):
        self.show()

        Dlg = AboutDlg(
            self.current_dir,
            self.name,
            self.settings, 
            self.file_path, 
            parent=self
            )
        Dlg.exec_()

    def exit_app(self):
        self.settings.setValue("window_size", self.size())
        self.settings.setValue("media_volume", self.horizontalSlider_2.value())
        sys.exit(0)

    def check_for_updates(self, startup=None):
        try:
            response = requests.get(
                "https://api.github.com/repos/deeffest/DEEF-Lite-Media-Player/releases/latest"
            )
            item_version = response.json()["name"]
            item_download = response.json().get("html_url")         

            if item_version != self.version:
                update_msg_box = QMessageBox(self)
                update_msg_box.setIcon(QMessageBox.Information)
                update_msg_box.setText(f"New version of DLMPlayer is available!\n\nYour version: {self.version}\nNew version: {item_version}\n\nWould you like to update now?")
                update_msg_box.setWindowTitle(self.name)

                btn_update = update_msg_box.addButton("Update", QMessageBox.AcceptRole)
                btn_cancel = update_msg_box.addButton("Cancel", QMessageBox.RejectRole)
                
                update_msg_box.setDefaultButton(btn_update)
                
                ret = update_msg_box.exec()

                if update_msg_box.clickedButton() == btn_update:
                    webbrowser.open_new_tab(item_download)
                    self.exit_app()
            else:
                if not startup:
                    QMessageBox.information(self, 
                        self.name, 
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
        desktop = qApp.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            self.playlist_cleaner()
            file_paths = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path) and self.is_media_file(file_path):
                    file_paths.append(os.path.join(file_path))
                elif os.path.isdir(file_path):
                    directory = file_path
                    for file in os.listdir(directory):
                        file_path = os.path.join(directory, file)
                        if os.path.isfile(file_path) and self.is_media_file(file_path):
                            ext = file_path.rsplit(".", 1)[-1].lower()
                            if ext != "m3u":
                                file_paths.append(file_path)

            for path in file_paths:
                if path.endswith('.m3u'):
                    self.open_playlist(path)
                else:
                    self.add_to_playlist(path)

            if file_paths:
                self.open_media(file_paths[0])

            event.acceptProposedAction()

    def showEvent(self, event):
        super().showEvent(event)
        if not self.win_toolbar.window():
            self.win_toolbar.setWindow(self.windowHandle())

    def closeEvent(self, event):
        event.ignore()
        if self.settings.value("hide_window_in_tray", "false") == "true":
            self.hide()
        else:
            self.exit_app()