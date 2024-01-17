#main.py
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtCore import QSettings, Qt
import os
import sys
import logging
from tempfile import gettempdir

from core.main_window import Window

name = "DEEF Lite Media Player"
version = "1.0"
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

def read_style_sheet(file_path):
    try:
        with open(file_path, 'r') as file:
            css = file.read()
            css = css.replace(
                "RESOURCE_PATH", 
                current_dir.replace("\\", "/")
            )
            return css
    except Exception as e:
        logging.error(str(e))
        return ""

def setup_logging():
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=os.path.join(gettempdir(), 'error.log'),
        filemode='w'
    )

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def apply_theme(app_theme, theme_style):
    app.setStyleSheet(read_style_sheet(f"{current_dir}/core/css/{app_theme}/{theme_style}.css"))
    if theme_style != "classic" and theme_style != "modern":
        app.setStyle(theme_style)

if __name__ == '__main__':
    setup_logging() 
    sys.excepthook = handle_exception

    settings = QSettings("deeffest", name)  
    app_theme = settings.value("app_theme", "dark")
    theme_style = settings.value("theme_style", "classic")    
    
    app = QApplication(sys.argv + (['-platform', 'windows:darkmode=1'] if app_theme == "dark" else []))
    apply_theme(app_theme, theme_style)

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