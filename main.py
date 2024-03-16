#main.py
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QPalette, QColor
import os
import sys

from core.main_window import Window

name = "DEEF Lite Media Player"
version = "1.1"
current_dir = os.path.dirname(os.path.abspath(__file__))

supported_formats = [
    "mp3", "wav", "ogg", "flac", 
    "aac", "wma", "m4a", "opus", 
    "webm", "mp4", "avi", "mov",
    "m3u", "3gpp", "mkv"
]
filter_ = "Media Files ({})".format(' '.join('*.' + fmt for fmt in supported_formats))

def is_media_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension[1:] 

    return file_extension in supported_formats

def set_app_palette():
    app_palette = QPalette()

    if app_theme == "dark":
        app_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        app_palette.setColor(QPalette.WindowText, Qt.white)
        app_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        app_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        app_palette.setColor(QPalette.Text, Qt.white)
        app_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        app_palette.setColor(QPalette.ButtonText, Qt.white)
        app_palette.setColor(QPalette.BrightText, Qt.red)
        app_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        app_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        app_palette.setColor(QPalette.HighlightedText, Qt.white)
        app_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
        app_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        app_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
        app_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        app_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
        app_palette.setColor(QPalette.Disabled, QPalette.ToolTipBase, Qt.black)
        app_palette.setColor(QPalette.Disabled, QPalette.ToolTipText, Qt.white)
    else:
        app_palette = QPalette()
        app_palette.setColor(QPalette.Highlight, QColor(144,200,246))
        app_palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(app_palette)

if __name__ == '__main__':
    settings = QSettings("deeffest", name)  
    app_theme = settings.value("app_theme", "dark")  
    
    app = QApplication(sys.argv + (['-platform', 'windows:darkmode=1'] if app_theme == "dark" else []))
    app.setStyle("Fusion")
    set_app_palette()

    multimedia_plugin = settings.value("preferred_multimedia_plugins", "directshow")
    os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = f"{multimedia_plugin}"

    file_path = None
    for arg in sys.argv[1:]:
        if os.path.exists(arg) and is_media_file(arg):
            file_path = arg
            break

    main_window = Window(
        name,
        version,
        current_dir,
        filter_,
        settings,
        file_path=file_path
    )
    
    sys.exit(app.exec_())