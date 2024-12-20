import os
import platform
import webbrowser
import mimetypes
import random
import resources.resources_rc
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu, QStatusBar, QToolBar, \
    QDockWidget, QLabel, QMessageBox, QFileDialog, QInputDialog, QListWidgetItem, \
    QAbstractItemView, QWidget, QLineEdit, QListWidget, QVBoxLayout
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData
from PySide6.QtGui import QIcon, QAction, QActionGroup
from PySide6.QtCore import QSettings, QUrl, Qt, QTimer, QEvent
from .video_widget import VideoWidget
from .clickable_slider import ClickableSlider
from .update_checker import UpdateChecker
from packaging import version as pkg_version

class MainWindow(QMainWindow):
    def __init__(self, app, theme, media_paths=None, parent=None):
        super().__init__(parent)
        self.app = app
        self.theme = theme
        self.settings = QSettings()
        self.loop_mode = None
        self.playlist = []
        self.current_index = -1
        self.autoplay_enabled = False
        self.was_playlist_visible = False
        if self.settings.contains("sort_option"):
            self.sort_option = self.settings.value("sort_option")
        else:
            self.sort_option = "Date"
        if self.settings.contains("sort_order"):
            self.sort_order_descending = self.settings.value("sort_order")
        else:
            self.sort_order_descending = True

        self.setWindowTitle("DEEF Lite Media Player")
        self.setObjectName("MainWindow")
        self.setAcceptDrops(True)
        self.setWindowIcon(QIcon(":/icons/icon"))        
            
        if self.settings.value("geometry") is not None:
            self.restoreGeometry(self.settings.value("geometry"))
        else:
            self.resize(800, 600)

        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)
        if self.settings.value("volume") is not None:
            volume = int(self.settings.value("volume"))
            self.audio_output.setVolume(volume / 100)
        self.video_widget = VideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)
        self.setCentralWidget(self.video_widget)

        self.media_player.playbackStateChanged.connect(self.handle_playback_state_changed)
        self.media_player.mediaStatusChanged.connect(self.handle_media_status_changed)
        self.media_player.errorOccurred.connect(self.handle_media_error_changed)
        self.media_player.positionChanged.connect(self.update_slider_position)
        self.media_player.durationChanged.connect(self.update_slider_duration)
        self.audio_output.volumeChanged.connect(self.update_slider_volume)
        self.media_player.tracksChanged.connect(self.handle_tracks_changed)

        self.dock_widget = QDockWidget(self)
        self.dock_widget.setObjectName("PlaylistDock")
        self.dock_widget.setWindowTitle("Playlist")
        self.dock_widget.setTitleBarWidget(QWidget())
        self.dock_widget.setFeatures(QDockWidget.DockWidgetClosable)
        self.dock_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dock_widget.setFocusPolicy(Qt.NoFocus)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setMenuBar(self.menu_bar)

        self.menu_file = QMenu("File")
        self.menu_bar.addMenu(self.menu_file)

        self.action_open_file = QAction("Open File")
        self.action_open_file.setIcon(QIcon(f":/icons/file_{self.theme}"))
        self.action_open_file.setShortcut("Ctrl+O")
        self.action_open_file.triggered.connect(self.open_file_dialog)
        self.menu_file.addAction(self.action_open_file)
        self.addAction(self.action_open_file)

        self.action_open_url = QAction("Open URL")
        self.action_open_url.setIcon(QIcon(f":/icons/url_{self.theme}"))
        self.action_open_url.setShortcut("Ctrl+U")
        self.action_open_url.triggered.connect(self.open_url_dialog)
        self.menu_file.addAction(self.action_open_url)
        self.addAction(self.action_open_url)

        self.action_open_folder = QAction("Open Folder")
        self.action_open_folder.setIcon(QIcon(f":/icons/folder_{self.theme}"))
        self.action_open_folder.setShortcut("Ctrl+F")
        self.action_open_folder.triggered.connect(self.open_folder_dialog)
        self.menu_file.addAction(self.action_open_folder)
        self.addAction(self.action_open_folder)

        self.action_quit = QAction("Quit")
        self.action_quit.setIcon(QIcon(f":/icons/quit_{self.theme}"))
        self.action_quit.setShortcut("Ctrl+Q")
        self.action_quit.triggered.connect(self.close)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_quit)
        self.addAction(self.action_quit)

        self.menu_playback = QMenu("Playback")
        self.menu_bar.addMenu(self.menu_playback)
        
        self.action_play_pause = QAction("Play/Pause")
        self.action_play_pause.setIcon(QIcon(f":/icons/play_{self.theme}"))
        self.action_play_pause.setShortcut("Space")
        self.action_play_pause.triggered.connect(self.toggle_play_pause)
        self.menu_playback.addAction(self.action_play_pause)
        self.addAction(self.action_play_pause)

        self.action_stop = QAction("Stop")
        self.action_stop.setIcon(QIcon(f":/icons/stop_{self.theme}"))
        self.action_stop.setShortcut("Ctrl+S")
        self.action_stop.triggered.connect(self.stop_media)
        self.menu_playback.addAction(self.action_stop)
        self.addAction(self.action_stop)

        self.menu_loop = QMenu("Loop")
        self.menu_loop.setIcon(QIcon(f":/icons/loop_{self.theme}"))
        self.menu_playback.addMenu(self.menu_loop)

        self.action_loop_none = QAction("No Loop", self)
        self.action_loop_none.setCheckable(True)
        self.action_loop_none.triggered.connect(lambda: self.set_loop_mode(None))
        self.menu_loop.addAction(self.action_loop_none)

        self.action_loop_single = QAction("Loop Single", self)
        self.action_loop_single.setCheckable(True)
        self.action_loop_single.triggered.connect(lambda: self.set_loop_mode("single"))
        self.menu_loop.addAction(self.action_loop_single)

        self.action_loop_playlist = QAction("Loop Playlist", self)
        self.action_loop_playlist.setCheckable(True)
        self.action_loop_playlist.triggered.connect(lambda: self.set_loop_mode("playlist"))
        self.menu_loop.addAction(self.action_loop_playlist)

        loop_action_group = QActionGroup(self)
        loop_action_group.addAction(self.action_loop_none)
        loop_action_group.addAction(self.action_loop_single)
        loop_action_group.addAction(self.action_loop_playlist)
        self.action_loop_none.setChecked(True)

        self.action_mute_unmute = QAction("Mute/Unmute")
        self.action_mute_unmute.setIcon(QIcon(f":/icons/unmute_{self.theme}"))
        self.action_mute_unmute.setShortcut("Ctrl+M")
        self.action_mute_unmute.triggered.connect(self.toggle_mute_unmute)
        self.menu_playback.addAction(self.action_mute_unmute)
        self.addAction(self.action_mute_unmute)

        self.menu_speed = QMenu("Speed")
        self.menu_speed.setIcon(QIcon(f":/icons/speed_{self.theme}"))
        self.menu_playback.addMenu(self.menu_speed)

        self.action_speed_025x = QAction("0.25x", self)
        self.action_speed_025x.setCheckable(True)
        self.action_speed_025x.triggered.connect(lambda: self.set_playback_rate(0.25))
        self.menu_speed.addAction(self.action_speed_025x)

        self.action_speed_05x = QAction("0.5x", self)
        self.action_speed_05x.setCheckable(True)
        self.action_speed_05x.triggered.connect(lambda: self.set_playback_rate(0.5))
        self.menu_speed.addAction(self.action_speed_05x)

        self.action_speed_075x = QAction("0.75x", self)
        self.action_speed_075x.setCheckable(True)
        self.action_speed_075x.triggered.connect(lambda: self.set_playback_rate(0.75))
        self.menu_speed.addAction(self.action_speed_075x)

        self.action_speed_1x = QAction("1.0x", self)
        self.action_speed_1x.setCheckable(True)
        self.action_speed_1x.setChecked(True)
        self.action_speed_1x.triggered.connect(lambda: self.set_playback_rate(1.0))
        self.menu_speed.addAction(self.action_speed_1x)

        self.action_speed_125x = QAction("1.25x", self)
        self.action_speed_125x.setCheckable(True)
        self.action_speed_125x.triggered.connect(lambda: self.set_playback_rate(1.25))
        self.menu_speed.addAction(self.action_speed_125x)

        self.action_speed_15x = QAction("1.5x", self)
        self.action_speed_15x.setCheckable(True)
        self.action_speed_15x.triggered.connect(lambda: self.set_playback_rate(1.5))
        self.menu_speed.addAction(self.action_speed_15x)

        self.action_speed_175x = QAction("1.75x", self)
        self.action_speed_175x.setCheckable(True)
        self.action_speed_175x.triggered.connect(lambda: self.set_playback_rate(1.75))
        self.menu_speed.addAction(self.action_speed_175x)

        self.action_speed_2x = QAction("2.0x", self)
        self.action_speed_2x.setCheckable(True)
        self.action_speed_2x.triggered.connect(lambda: self.set_playback_rate(2.0))
        self.menu_speed.addAction(self.action_speed_2x)
        
        self.action_speed_25x = QAction("2.5x", self)
        self.action_speed_25x.setCheckable(True)
        self.action_speed_25x.triggered.connect(lambda: self.set_playback_rate(2.5))
        self.menu_speed.addAction(self.action_speed_25x)

        self.menu_audio_tracks = QMenu("Audio Tracks")
        self.menu_playback.addMenu(self.menu_audio_tracks)
        self.audio_tracks_group = QActionGroup(self)
        self.audio_tracks_group.setExclusive(True)

        self.menu_video_tracks = QMenu("Video Tracks")
        self.menu_playback.addMenu(self.menu_video_tracks)
        self.video_tracks_group = QActionGroup(self)
        self.video_tracks_group.setExclusive(True)

        self.menu_subtitle_tracks = QMenu("Subtitle Tracks")
        self.menu_subtitle_tracks.setIcon(QIcon(f":/icons/subtitle_{self.theme}"))
        self.menu_playback.addMenu(self.menu_subtitle_tracks)
        self.subtitle_tracks_group = QActionGroup(self)
        self.subtitle_tracks_group.setExclusive(True)

        self.add_placeholder_if_empty(self.menu_audio_tracks)
        self.add_placeholder_if_empty(self.menu_video_tracks)
        self.add_placeholder_if_empty(self.menu_subtitle_tracks)

        self.action_backward_10 = QAction("Backward 10s")
        self.action_backward_10.setShortcut("Left")
        self.action_backward_10.triggered.connect(self.backward_10_seconds)
        self.addAction(self.action_backward_10)

        self.action_forward_10 = QAction("Forward 10s")
        self.action_forward_10.setShortcut("Right")
        self.action_forward_10.triggered.connect(self.forward_10_seconds)
        self.addAction(self.action_forward_10)

        self.menu_playlist = QMenu("Playlist")
        self.menu_bar.addMenu(self.menu_playlist)

        self.action_add_files_to_playlist = QAction("Add File(s) to Playlist")
        self.action_add_files_to_playlist.setIcon(QIcon(f":/icons/add_{self.theme}"))
        self.action_add_files_to_playlist.setShortcut("Ctrl+L")
        self.action_add_files_to_playlist.triggered.connect(self.add_files_to_playlist)
        self.menu_playlist.addAction(self.action_add_files_to_playlist)
        self.addAction(self.action_add_files_to_playlist)

        self.action_shuffle = QAction("Shuffle")
        self.action_shuffle.setIcon(QIcon(f":/icons/shuffle_{self.theme}"))
        self.action_shuffle.setShortcut("Ctrl+H")
        self.action_shuffle.triggered.connect(self.shuffle_playlist)
        self.menu_playlist.addSeparator()
        self.menu_playlist.addAction(self.action_shuffle)

        self.action_clear_all_playlist = QAction("Clear All Playlist")
        self.action_clear_all_playlist.setIcon(QIcon(f":/icons/clear_all_{self.theme}"))
        self.action_clear_all_playlist.setShortcut("Ctrl+C")
        self.action_clear_all_playlist.triggered.connect(self.clear_all_playlist)
        self.menu_playlist.addAction(self.action_clear_all_playlist)
        self.addAction(self.action_clear_all_playlist)

        self.action_clear_except_current = QAction("Clear Except Current")
        self.action_clear_except_current.setIcon(QIcon(f":/icons/clear_except_current_{self.theme}"))
        self.action_clear_except_current.setShortcut("Ctrl+E")
        self.action_clear_except_current.triggered.connect(self.clear_except_current)
        self.menu_playlist.addAction(self.action_clear_except_current)
        self.addAction(self.action_clear_except_current)

        self.action_previous = QAction("Previous")
        self.action_previous.setIcon(QIcon(f":/icons/previous_{self.theme}"))
        self.action_previous.setShortcut("Ctrl+Left")
        self.action_previous.triggered.connect(self.play_previous)
        self.menu_playlist.addSeparator()
        self.menu_playlist.addAction(self.action_previous)
        self.addAction(self.action_previous)

        self.action_next = QAction("Next")
        self.action_next.setIcon(QIcon(f":/icons/next_{self.theme}"))
        self.action_next.setShortcut("Ctrl+Right")
        self.action_next.triggered.connect(self.play_next)
        self.menu_playlist.addAction(self.action_next)
        self.addAction(self.action_next)

        self.sort_by_menu = QMenu("Sort by...", self)
        self.sort_by_menu.setIcon(QIcon(f":/icons/sort_by_{self.theme}"))
        self.menu_playlist.addSeparator()
        self.menu_playlist.addMenu(self.sort_by_menu)

        self.sort_by_date_action = QAction("Date", self)
        self.sort_by_date_action.setCheckable(True)
        self.sort_by_date_action.triggered.connect(lambda: self.set_sort_option("Date"))

        self.sort_by_name_action = QAction("Name", self)
        self.sort_by_name_action.setCheckable(True)
        self.sort_by_name_action.triggered.connect(lambda: self.set_sort_option("Name"))

        self.sort_by_type_action = QAction("Type", self)
        self.sort_by_type_action.setCheckable(True)
        self.sort_by_type_action.triggered.connect(lambda: self.set_sort_option("Type"))

        self.sort_by_size_action = QAction("Size", self)
        self.sort_by_size_action.setCheckable(True)
        self.sort_by_size_action.triggered.connect(lambda: self.set_sort_option("Size"))

        if self.sort_option == "Date":
            self.sort_by_date_action.setChecked(True)
        elif self.sort_option == "Name":
            self.sort_by_name_action.setChecked(True)
        elif self.sort_option == "Type":
            self.sort_by_type_action.setChecked(True)
        elif self.sort_option == "Size":
            self.sort_by_size_action.setChecked(True)

        self.sort_ascending_action = QAction("Ascending", self)
        self.sort_ascending_action.setCheckable(True)
        self.sort_ascending_action.triggered.connect(lambda: self.set_sort_order(False))

        self.sort_descending_action = QAction("Descending", self)
        self.sort_descending_action.setCheckable(True)
        self.sort_descending_action.triggered.connect(lambda: self.set_sort_order(True))

        if self.sort_order_descending:
            self.sort_descending_action.setChecked(True)
            self.sort_ascending_action.setChecked(False)
        else:
            self.sort_ascending_action.setChecked(True)
            self.sort_descending_action.setChecked(False)

        self.sort_group = QActionGroup(self)
        self.sort_group.addAction(self.sort_by_date_action)
        self.sort_group.addAction(self.sort_by_name_action)
        self.sort_group.addAction(self.sort_by_type_action)
        self.sort_group.addAction(self.sort_by_size_action)

        self.order_group = QActionGroup(self)
        self.order_group.addAction(self.sort_ascending_action)
        self.order_group.addAction(self.sort_descending_action)

        self.sort_by_menu.addAction(self.sort_by_date_action)
        self.sort_by_menu.addAction(self.sort_by_name_action)
        self.sort_by_menu.addAction(self.sort_by_type_action)
        self.sort_by_menu.addAction(self.sort_by_size_action)
        self.sort_by_menu.addSeparator()
        self.sort_by_menu.addAction(self.sort_ascending_action)
        self.sort_by_menu.addAction(self.sort_descending_action)

        self.action_autoplay = QAction("Autoplay")
        self.action_autoplay.setCheckable(True)
        self.action_autoplay.setShortcut("Ctrl+A")
        self.action_autoplay.triggered.connect(self.toggle_autoplay)
        self.menu_playlist.addSeparator()
        self.menu_playlist.addAction(self.action_autoplay)
        self.addAction(self.action_autoplay)
        
        self.menu_view = QMenu("View")
        self.menu_bar.addMenu(self.menu_view)

        self.action_fullscreen = QAction("Full screen")
        self.action_fullscreen.setIcon(QIcon(f":/icons/fullscreen_{self.theme}"))
        self.action_fullscreen.setShortcut("F11")
        self.action_fullscreen.triggered.connect(self.toggle_fullscreen)
        self.menu_view.addAction(self.action_fullscreen)
        self.addAction(self.action_fullscreen)

        self.action_always_on_top = QAction("Always On Top")
        self.action_always_on_top.setIcon(QIcon(f":/icons/pin_{self.theme}"))
        self.action_always_on_top.setShortcut("Ctrl+T")
        self.action_always_on_top.triggered.connect(self.toggle_always_on_top)
        self.menu_view.addAction(self.action_always_on_top)
        self.addAction(self.action_always_on_top)

        self.action_playlist = self.dock_widget.toggleViewAction()
        self.action_playlist.setText("Hide Playlist")
        self.action_playlist.setCheckable(False)
        self.action_playlist.setIcon(QIcon(f":/icons/close_playlist_{self.theme}"))
        self.action_playlist.setShortcut("Ctrl+P")
        self.action_playlist.triggered.connect(self.toggle_playlist_visibility)
        self.menu_view.addSeparator()
        self.menu_view.addAction(self.action_playlist)
        self.addAction(self.action_playlist)

        self.menu_help = QMenu("Help")
        self.menu_bar.addMenu(self.menu_help)

        self.action_search_for_updates = QAction("Search for Updates")
        self.action_search_for_updates.setIcon(QIcon(f":/icons/search_{self.theme}"))
        self.action_search_for_updates.triggered.connect(lambda: self.check_updates(manual_check=True))
        self.menu_help.addAction(self.action_search_for_updates)

        self.action_about = QAction("About")
        self.action_about.setIcon(QIcon(f":/icons/about_{self.theme}"))
        self.action_about.triggered.connect(self.about_app)
        self.menu_help.addSeparator()
        self.menu_help.addAction(self.action_about)

        self.action_about_qt = QAction("About Qt")
        self.action_about_qt.setIcon(QIcon(f":/qt-project.org/logos/pysidelogo.png"))
        self.action_about_qt.triggered.connect(self.about_qt)
        self.menu_help.addAction(self.action_about_qt)

        self.seek_slider = ClickableSlider()
        self.seek_slider.setCursor(Qt.PointingHandCursor)
        self.seek_slider.valueChanged.connect(self.seek_media)

        self.volume_slider = ClickableSlider()
        self.volume_slider.setMaximumWidth(70)
        self.volume_slider.setCursor(Qt.PointingHandCursor)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.audio_output.volume() * 100)
        self.volume_slider.valueChanged.connect(self.set_volume)

        self.elapsed_time_label = QLabel("00:00")
        self.elapsed_time_label.setStyleSheet("QLabel { color: gray; }")
        self.separator_time_label = QLabel("/")
        self.separator_time_label.setStyleSheet("QLabel { color: gray; }")
        self.total_time_label = QLabel("00:00")

        self.tool_bar = QToolBar(self)
        self.tool_bar.setObjectName("Playbar") 
        self.tool_bar.setMovable(False)
        self.tool_bar.setFloatable(False)
        self.tool_bar.setWindowTitle("Playbar")
        self.tool_bar.addAction(self.action_previous)
        self.tool_bar.addAction(self.action_play_pause)
        self.tool_bar.addAction(self.action_next)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.elapsed_time_label)
        self.tool_bar.addWidget(self.seek_slider)
        self.tool_bar.addWidget(self.total_time_label)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.action_mute_unmute)
        self.tool_bar.addWidget(self.volume_slider)
        self.tool_bar.addAction(self.action_playlist)
        self.tool_bar.addAction(self.action_fullscreen)
        self.tool_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        self.addToolBar(Qt.BottomToolBarArea, self.tool_bar)
        
        self.context_menu = QMenu(self)
        self.context_menu.addAction(self.action_playlist)
        self.context_menu.addSeparator()
        self.context_menu.addAction(self.action_fullscreen)
        self.context_menu.addSeparator()
        self.context_menu.addAction(self.action_shuffle)
        self.context_menu.addMenu(self.menu_loop)
        self.context_menu.addSeparator()
        self.context_menu.addMenu(self.menu_audio_tracks)
        self.context_menu.addMenu(self.menu_video_tracks)
        self.context_menu.addMenu(self.menu_subtitle_tracks)
        self.context_menu.addSeparator()
        self.context_menu.addAction(self.action_always_on_top)
        self.context_menu.addSeparator()
        self.context_menu.addAction(self.action_quit)

        self.full_context_menu = QMenu(self)
        self.full_context_menu.addAction(self.action_mute_unmute)
        self.full_context_menu.addMenu(self.menu_audio_tracks)
        self.full_context_menu.addMenu(self.menu_video_tracks)
        self.full_context_menu.addMenu(self.menu_subtitle_tracks)
        self.full_context_menu.addSeparator()
        self.full_context_menu.addAction(self.action_play_pause)
        self.full_context_menu.addAction(self.action_stop)
        self.full_context_menu.addAction(self.action_previous)
        self.full_context_menu.addAction(self.action_next)
        self.full_context_menu.addMenu(self.menu_speed)
        self.full_context_menu.addSeparator()
        self.full_context_menu.addMenu(self.menu_loop)
        self.full_context_menu.addAction(self.action_shuffle)
        self.full_context_menu.addSeparator()
        self.full_context_menu.addAction(self.action_fullscreen)
        self.full_context_menu.addSeparator()
        self.full_context_menu.addAction(self.action_quit)

        self.action_play_from_playlist = QAction("Play selected item")
        self.action_play_from_playlist.setIcon(QIcon(f":/icons/play_{self.theme}"))
        self.action_play_from_playlist.triggered.connect(self.play_selected_item)
        self.addAction(self.action_play_from_playlist)
        
        self.action_clear = QAction("Remove selected item")
        self.action_clear.setIcon(QIcon(f":/icons/clear_{self.theme}"))
        self.action_clear.triggered.connect(self.clear_selected_item)

        self.dock_container = QWidget(self.dock_widget)
        self.dock_layout = QVBoxLayout(self.dock_container)
        self.dock_layout.setContentsMargins(0, 0, 0, 0)

        self.search_line_edit = QLineEdit(self.dock_container)
        self.search_line_edit.setPlaceholderText("Search...")
        self.search_line_edit.setClearButtonEnabled(True)
        self.search_line_edit.setFocusPolicy(Qt.NoFocus)
        self.search_line_edit.installEventFilter(self)
        self.search_line_edit.textChanged.connect(self.filter_playlist)
        self.dock_layout.addWidget(self.search_line_edit)

        self.playlist_widget = QListWidget(self.dock_container)
        self.playlist_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.playlist_widget.setDragDropMode(QAbstractItemView.InternalMove)
        self.playlist_widget.setDefaultDropAction(Qt.MoveAction)
        self.playlist_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.playlist_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playlist_widget.model().rowsMoved.connect(self.update_playlist_order)
        self.playlist_widget.itemDoubleClicked.connect(self.play_selected_item)
        self.playlist_widget.customContextMenuRequested.connect(self.show_playlist_context_menu)
        self.dock_layout.addWidget(self.playlist_widget)

        self.dock_widget.setWidget(self.dock_container)

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.media_player_state_label = QLabel(self.status_bar)
        self.media_player_state_label.setText("")
        self.status_bar.addWidget(self.media_player_state_label)

        self.media_player_status_label = QLabel(self.status_bar)
        self.media_player_status_label.setText("")
        self.status_bar.addPermanentWidget(self.media_player_status_label)

        if self.settings.value("windowState") is not None:
            self.restoreState(self.settings.value("windowState"))

        if self.dock_widget.isHidden():
            self.action_playlist.setText("Show Playlist")
            self.action_playlist.setIcon(QIcon(f":/icons/playlist_{self.theme}"))
            
        if self.isFullScreen():
            self.action_fullscreen.setText("Exit full screen")
            self.action_fullscreen.setIcon(QIcon(f":/icons/close_fullscreen_{self.theme}"))
            self.fullscreen_mode()
            
        self.installEventFilter(self)
        self.check_updates(manual_check=False)

        if media_paths:
            self.add_to_playlist(media_paths)
            if self.playlist:
                self.current_index = 0
                self.play_media(self.playlist[self.current_index])
    
    def is_valid_mime_type(self, file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            return mime_type.startswith('audio/') or mime_type.startswith('video/')
        return False
    
    def is_valid_url(self, url):
        return url.lower().startswith(('http://', 'https://'))

    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            if self.is_valid_mime_type(selected_file):
                self.stop_media()
                index = self.add_to_playlist([selected_file])
                self.current_index = index
                self.play_media(self.playlist[self.current_index])

    def open_url_dialog(self):
        open_url_dialog = QInputDialog(self)
        open_url_dialog.setInputMode(QInputDialog.TextInput)
        open_url_dialog.setWindowTitle("Open URL")
        open_url_dialog.setLabelText("Enter URL:")
        open_url_dialog.resize(500, 100)
        if open_url_dialog.exec():
            url = open_url_dialog.textValue()
            if self.is_valid_url(url):
                self.stop_media()
                index = self.add_to_playlist([url])
                self.current_index = index
                self.play_media(self.playlist[self.current_index])

    def open_folder_dialog(self):
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if folder_dialog.exec():
            selected_folder = folder_dialog.selectedFiles()[0]
            files = self.get_files_in_folder(selected_folder)
            valid_files = [file for file in files if self.is_valid_mime_type(file)]
            if valid_files:
                self.stop_media()
                initial_playlist_length = len(self.playlist)
                self.add_to_playlist(valid_files)
                self.current_index = initial_playlist_length
                if self.playlist:
                    self.play_media(self.playlist[self.current_index])

    def normalize_path(self, path):
        return path.replace('\\', '/')

    def set_sort_order(self, descending):
        self.sort_order_descending = descending
    
    def set_sort_option(self, option):
        self.sort_option = option

    def get_files_in_folder(self, folder_path):
        files = []
        folder_path = self.normalize_path(os.path.normpath(folder_path))

        with os.scandir(folder_path) as entries:
            entries = [entry for entry in entries if entry.is_file()]

            if self.sort_option == "Date":
                entries.sort(key=lambda e: e.stat().st_mtime, reverse=self.sort_order_descending)
            elif self.sort_option == "Name":
                entries.sort(key=lambda e: e.name.lower(), reverse=self.sort_order_descending)
            elif self.sort_option == "Type":
                entries.sort(key=lambda e: os.path.splitext(e.name)[1], reverse=self.sort_order_descending)
            elif self.sort_option == "Size":
                entries.sort(key=lambda e: e.stat().st_size, reverse=self.sort_order_descending)

            for entry in entries:
                file_path = self.normalize_path(os.path.normpath(entry.path))
                if self.is_valid_mime_type(file_path):
                    files.append(file_path)

        return files
    
    def add_files_to_playlist(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            valid_files = [file for file in selected_files if self.is_valid_mime_type(file)]
            if valid_files:
                self.add_to_playlist(valid_files)

    def add_to_playlist(self, files):
        for file in files:
            normalized_file = self.normalize_path(file)
            
            if self.is_valid_mime_type(normalized_file) or self.is_valid_url(normalized_file):
                if normalized_file not in self.playlist:
                    self.playlist.append(normalized_file)
                    item = QListWidgetItem(normalized_file)
                    item.setToolTip(normalized_file)
                    self.playlist_widget.addItem(item)
        
        return len(self.playlist) - 1 if self.playlist else -1
    
    def play_media(self, media_path):
        def go():
            self.media_player.setSource(QUrl.fromLocalFile(media_path))
            self.media_player.play()

        QTimer.singleShot(0, lambda: go())

        file_name = os.path.basename(media_path)
        self.setWindowTitle(f"DEEF Lite Media Player - {file_name}")

        self.update_playlist_icons()

    def toggle_autoplay(self):
        self.autoplay_enabled = not self.autoplay_enabled
        if self.autoplay_enabled:
            self.action_autoplay.setChecked(True)
        else:
            self.action_autoplay.setChecked(False)

    def add_placeholder_if_empty(self, menu):
        menu.clear()
        placeholder_action = QAction("No Tracks Available", self)
        placeholder_action.setEnabled(False)
        menu.addAction(placeholder_action)

    def handle_tracks_changed(self):
        self.menu_audio_tracks.clear()
        self.menu_video_tracks.clear()
        self.menu_subtitle_tracks.clear()

        def create_no_track_action(menu, action_group, set_track_func):
            no_track_action = QAction("No Track", self)
            no_track_action.setData(-1)
            no_track_action.setCheckable(True)
            no_track_action.triggered.connect(lambda: set_track_func(None))
            menu.addAction(no_track_action)
            action_group.addAction(no_track_action)
            return no_track_action

        no_audio_track_action = create_no_track_action(self.menu_audio_tracks, self.audio_tracks_group, self.set_audio_track)
        no_video_track_action = create_no_track_action(self.menu_video_tracks, self.video_tracks_group, self.set_video_track)
        no_subtitle_track_action = create_no_track_action(self.menu_subtitle_tracks, self.subtitle_tracks_group, self.set_subtitle_track)

        audio_tracks = self.media_player.audioTracks()
        current_audio_track = self.media_player.activeAudioTrack()
        
        for index, track in enumerate(audio_tracks):
            title = track.stringValue(QMediaMetaData.Title) or "Unknown"
            language = track.stringValue(QMediaMetaData.Language) or "Unknown"
            action = QAction(f"{title} ({language})", self)
            action.setData(index)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, idx=index: self.set_audio_track(idx))
            self.menu_audio_tracks.addAction(action)
            self.audio_tracks_group.addAction(action)
            if current_audio_track == index:
                action.setChecked(True)

        if current_audio_track == -1:
            no_audio_track_action.setChecked(True)

        video_tracks = self.media_player.videoTracks()
        current_video_track = self.media_player.activeVideoTrack()
        
        for index, track in enumerate(video_tracks):
            title = track.stringValue(QMediaMetaData.Title) or "Unknown"
            language = track.stringValue(QMediaMetaData.Language) or "Unknown"
            action = QAction(f"{title} ({language})", self)
            action.setData(index)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, idx=index: self.set_video_track(idx))
            self.menu_video_tracks.addAction(action)
            self.video_tracks_group.addAction(action)
            if current_video_track == index:
                action.setChecked(True)

        if current_video_track == -1:
            no_video_track_action.setChecked(True)

        subtitle_tracks = self.media_player.subtitleTracks()
        current_subtitle_track = self.media_player.activeSubtitleTrack()
        
        for index, track in enumerate(subtitle_tracks):
            title = track.stringValue(QMediaMetaData.Title) or "Unknown"
            language = track.stringValue(QMediaMetaData.Language) or "Unknown"
            action = QAction(f"{title} ({language})", self)
            action.setData(index)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, idx=index: self.set_subtitle_track(idx))
            self.menu_subtitle_tracks.addAction(action)
            self.subtitle_tracks_group.addAction(action)
            if current_subtitle_track == index:
                action.setChecked(True)

        if current_subtitle_track == -1:
            no_subtitle_track_action.setChecked(True)

    def set_audio_track(self, index):
        if index is None or index == -1:
            self.media_player.setActiveAudioTrack(-1)
        else:
            self.media_player.setActiveAudioTrack(index)

    def set_video_track(self, index):
        if index is None or index == -1:
            self.media_player.setActiveVideoTrack(-1)
        else:
            self.media_player.setActiveVideoTrack(index)

    def set_subtitle_track(self, index):
        if index is None or index == -1:
            self.media_player.setActiveSubtitleTrack(-1)
        else:
            self.media_player.setActiveSubtitleTrack(index)

    def show_playlist_context_menu(self, pos):
        menu = QMenu(self)
        menu.addAction(self.action_play_from_playlist)
        menu.addSeparator()
        menu.addAction(self.action_clear)
        global_pos = self.playlist_widget.mapToGlobal(pos)
        menu.exec(global_pos)

    def filter_playlist(self, text):
        for index in range(self.playlist_widget.count()):
            item = self.playlist_widget.item(index)
            item.setHidden(text.lower() not in item.text().lower())

    def get_current_item(self):
        selected_items = self.playlist_widget.selectedItems()
        if selected_items:
            return selected_items[0]
        return None

    def play_selected_item(self):
        item = self.get_current_item()
        if item:
            self.current_index = self.playlist_widget.row(item)
            file_path = item.text()
            self.stop_media()
            self.play_media(file_path)

    def clear_selected_item(self):
        selected_items = self.playlist_widget.selectedItems()
        
        if not selected_items:
            return

        for item in selected_items:
            item_index = self.playlist_widget.row(item)
            file_path = item.text()

            self.playlist.remove(file_path)
            self.playlist_widget.takeItem(item_index)

            if item_index == self.current_index:
                if len(self.playlist) > 0:
                    if item_index >= len(self.playlist):
                        self.current_index = len(self.playlist) - 1
                    else:
                        self.current_index = item_index

                    next_file = self.playlist[self.current_index]
                    self.stop_media()
                    self.play_media(next_file)
                else:
                    self.clear_all_playlist()
            elif item_index < self.current_index:
                self.current_index -= 1

    def clear_all_playlist(self):
        self.playlist.clear()
        self.playlist_widget.clear()
        self.current_index = -1

        self.stop_media()
        self.setWindowTitle("DEEF Lite Media Player")
        
        self.update_playlist_icons()
        self.add_placeholder_if_empty(self.menu_audio_tracks)
        self.add_placeholder_if_empty(self.menu_video_tracks)
        self.add_placeholder_if_empty(self.menu_subtitle_tracks)
        
        self.seek_slider.setValue(0)
        self.total_time_label.setText("00:00")
        self.elapsed_time_label.setText("00:00")
        QTimer.singleShot(100, lambda: self.media_player.setSource(QUrl()))

    def clear_except_current(self):
        if self.current_index >= 0 and self.playlist:
            current_media = self.playlist[self.current_index]
            self.playlist = [current_media]
            self.playlist_widget.clear()

            item = QListWidgetItem(current_media)
            item.setToolTip(current_media)

            item.setIcon(QIcon(f":/icons/playing_{self.theme}"))
            self.playlist_widget.addItem(item)
   
            self.current_index = 0
            self.playlist_widget.setCurrentRow(self.current_index)
        else:
            self.clear_all_playlist()

        self.update_playlist_icons()

    def update_playlist_icons(self):
        play_icon = QIcon(f":/icons/play_cricle_{self.theme}")
        empty_icon = QIcon()
        
        for i in range(self.playlist_widget.count()):
            item = self.playlist_widget.item(i)
            if i == self.current_index:
                item.setIcon(play_icon)
                item.setSelected(True)
            else:
                item.setIcon(empty_icon)
                item.setSelected(False)

    def handle_playback_state_changed(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.action_play_pause.setIcon(QIcon(f":/icons/pause_{self.theme}"))
        elif state == QMediaPlayer.PlaybackState.PausedState:
            self.action_play_pause.setIcon(QIcon(f":/icons/play_{self.theme}"))
        elif state == QMediaPlayer.PlaybackState.StoppedState:
            self.action_play_pause.setIcon(QIcon(f":/icons/play_{self.theme}"))
        self.media_player_state_label.setText(str(state))

    def handle_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self.loop_mode == "single":
                self.media_player.play()
            elif self.loop_mode == "playlist" or self.autoplay_enabled:
                self.play_next()
            else:
                self.stop_media()
        self.media_player_status_label.setText(str(status))

    def handle_media_error_changed(self, error):
        QMessageBox.critical(self, "Media Player Error", f"{str(error)}: {self.media_player.errorString()}")

    def toggle_play_pause(self):
        if self.media_player.isPlaying():
            self.media_player.pause()
        else:
            self.media_player.play()

    def stop_media(self):
        self.media_player.stop()

    def play_next(self):
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.stop_media()
            self.play_media(self.playlist[self.current_index])
        elif self.loop_mode == "playlist":
            self.current_index = 0
            self.stop_media()
            self.play_media(self.playlist[self.current_index])
        else:
            self.stop_media()

    def play_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.stop_media()
            self.play_media(self.playlist[self.current_index])

    def set_loop_mode(self, mode):
        self.loop_mode = mode
        if mode == "single":
            self.action_loop_single.setChecked(True)
        elif mode == "playlist":
            self.action_loop_playlist.setChecked(True)
        else:
            self.action_loop_none.setChecked(True)

    def update_playlist_order(self):
        current_media = self.playlist[self.current_index] if self.current_index != -1 else None
        new_playlist = []
        
        for i in range(self.playlist_widget.count()):
            item = self.playlist_widget.item(i)
            new_playlist.append(item.text())

        self.playlist = new_playlist

        if current_media:
            self.current_index = self.playlist.index(current_media)

    def shuffle_playlist(self):
        if self.playlist:
            current_media = self.playlist[self.current_index] if self.current_index != -1 else None

            if current_media:
                self.playlist.remove(current_media)

            random.shuffle(self.playlist)

            if current_media:
                self.playlist.insert(0, current_media)

            self.playlist_widget.clear()
            for media in self.playlist:
                item = QListWidgetItem(media)
                item.setToolTip(media)
                self.playlist_widget.addItem(item)

            self.current_index = 0
            self.playlist_widget.setCurrentRow(self.current_index)

            self.update_playlist_icons()

    def update_slider_position(self, position):
        self.seek_slider.blockSignals(True)
        self.seek_slider.setValue(position)
        self.seek_slider.blockSignals(False)
        self.elapsed_time_label.setText(self.format_time(position))

    def update_slider_duration(self, duration):
        self.seek_slider.setRange(0, duration)
        self.total_time_label.setText(self.format_time(duration))

    def seek_media(self, position):
        self.media_player.setPosition(position)
        
    def backward_10_seconds(self):
        current_position = self.media_player.position()

        if current_position > 10000:
            self.media_player.setPosition(current_position - 10000)

    def forward_10_seconds(self):
        current_position = self.media_player.position()
        duration = self.media_player.duration()

        if current_position + 10000 < duration:
            self.media_player.setPosition(current_position + 10000)

    def set_playback_rate(self, rate):
        self.media_player.setPlaybackRate(rate)
        self.action_speed_025x.setChecked(rate == 0.25)
        self.action_speed_05x.setChecked(rate == 0.5)
        self.action_speed_075x.setChecked(rate == 0.75)
        self.action_speed_1x.setChecked(rate == 1.0)
        self.action_speed_125x.setChecked(rate == 1.25)
        self.action_speed_15x.setChecked(rate == 1.5)
        self.action_speed_175x.setChecked(rate == 1.75)
        self.action_speed_2x.setChecked(rate == 2.0)
        self.action_speed_25x.setChecked(rate == 2.5)
    
    def format_time(self, ms):
        seconds = (ms // 1000) % 60
        minutes = (ms // (1000 * 60)) % 60
        hours = (ms // (1000 * 60 * 60)) % 24
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"
        
    def set_volume(self, value):
        volume = value / 100.0
        self.audio_output.setVolume(volume)
    
    def update_slider_volume(self, volume):
        self.volume_slider.setValue(volume * 100)
    
    def toggle_mute_unmute(self):
        if self.audio_output.isMuted():
            self.action_mute_unmute.setIcon(QIcon(f":/icons/unmute_{self.theme}"))
            self.audio_output.setMuted(False)
        else:
            self.action_mute_unmute.setIcon(QIcon(f":/icons/mute_{self.theme}"))
            self.audio_output.setMuted(True)

    def toggle_playlist_visibility(self):
        if self.dock_widget.isVisible():
            self.was_playlist_visible = False
            self.dock_widget.hide()
            self.action_playlist.setText("Show Playlist")
            self.action_playlist.setIcon(QIcon(f":/icons/playlist_{self.theme}"))
        else:
            self.was_playlist_visible = True
            self.dock_widget.show()
            self.action_playlist.setText("Hide Playlist")
            self.action_playlist.setIcon(QIcon(f":/icons/close_playlist_{self.theme}"))

    def toggle_always_on_top(self):
        if self.isFullScreen(): 
            return
        if self.windowFlags() & Qt.WindowStaysOnTopHint:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.action_always_on_top.setIcon(QIcon(f":/icons/pin_{self.theme}"))
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.action_always_on_top.setIcon(QIcon(f":/icons/unpin_{self.theme}"))
        self.show()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.action_fullscreen.setText("Full screen")
            self.action_fullscreen.setIcon(QIcon(f":/icons/fullscreen_{self.theme}"))
            self.close_fullscreen_mode()
        else:
            self.showFullScreen()
            self.action_fullscreen.setText("Exit full screen")
            self.action_fullscreen.setIcon(QIcon(f":/icons/close_fullscreen_{self.theme}"))
            self.fullscreen_mode()

    def fullscreen_mode(self):
        self.menu_bar.hide()
        self.tool_bar.hide()
        self.status_bar.hide()

        self.was_playlist_visible = self.dock_widget.isVisible()

        if self.was_playlist_visible:
            self.dock_widget.hide()

        self.action_playlist.setText("Show Playlist")
        self.action_playlist.setIcon(QIcon(f":/icons/playlist_{self.theme}"))

    def close_fullscreen_mode(self):
        self.menu_bar.show()
        self.tool_bar.show()
        self.status_bar.show()

        if self.was_playlist_visible:
            self.dock_widget.show()
            self.action_playlist.setText("Hide Playlist")
            self.action_playlist.setIcon(QIcon(f":/icons/close_playlist_{self.theme}"))

    def check_updates(self, manual_check=False):
        self.action_search_for_updates.setEnabled(False)

        self.update_checker = UpdateChecker(manual_check)
        self.update_checker.update_checked.connect(self.handle_update_checked)
        self.update_checker.update_checked_failed.connect(self.handle_update_checked_failed)
        self.update_checker.start()
        
    def handle_update_checked(self, version, download, manual_check):
        current_version = pkg_version.parse(self.app.applicationVersion())
        latest_version = pkg_version.parse(version)

        if current_version < latest_version:
            msg_box = QMessageBox.question(
                self,
                "Update Available",
                f"A new version {version} is available. Do you want to download it?",
                QMessageBox.Yes | QMessageBox.No
            )
            if msg_box == QMessageBox.Yes:
                webbrowser.open_new_tab(download)
                self.close()
        elif manual_check:
            QMessageBox.information(
                self,
                "No Updates",
                f"You are using the latest version ({self.app.applicationVersion()})."
            )
        self.action_search_for_updates.setEnabled(True)

    def handle_update_checked_failed(self, error, manual_check):
        self.action_search_for_updates.setEnabled(True)
        if manual_check:
            QMessageBox.critical(self, "Update Check Failed", f"Failed to check for updates: {error}")

    def about_app(self):
        description = (f"<h3>DEEF Lite Media Player</h3>"
            "It is a simple, lightweight and open source cross-platform media player based on Qt (PySide6).<br><br>"    
            f"{self.app.applicationVersion()}<br>"
            "Created with ♥ by deeffest, 2024")
        QMessageBox.about(self, "About app", description)
    
    def about_qt(self):
        QMessageBox.aboutQt(self, "About Qt")

    def save_settings(self):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        self.settings.setValue("volume", self.volume_slider.value())
        self.settings.setValue("sort_option", self.sort_option)
        self.settings.setValue("sort_order", self.sort_order_descending)
        self.settings.sync()

    def contextMenuEvent(self, event):
        if self.isFullScreen():
            self.full_context_menu.exec(event.globalPos())
        else:
            self.context_menu.exec(event.globalPos())

    def eventFilter(self, obj, event):
        if obj == self.search_line_edit:
            if event.type() == QEvent.MouseButtonPress:
                self.search_line_edit.setFocus()
            elif event.type() == QEvent.Leave:
                self.search_line_edit.clearFocus()
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                if self.isFullScreen():
                    self.toggle_fullscreen()
                return True
        return super().eventFilter(obj, event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            files = []
            for url in urls:
                if url.isLocalFile():
                    files.append(url.toLocalFile())
            if files:
                self.add_to_playlist(files)
        else:
            super().dropEvent(event)

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)