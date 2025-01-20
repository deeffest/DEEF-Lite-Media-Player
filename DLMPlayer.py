import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from core.main_window import MainWindow

name = "DEEF-Lite-Media-Player"
version = "v2.2.0"
author = "deeffest"
website = "deeffest.pythonanywhere.com"

def setup_logging():
    log_dir = os.path.join(os.path.expanduser("~"), name, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "app.log")
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5
    )
    rotating_handler.setLevel(logging.INFO)
    rotating_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(message)s', datefmt='%Y.%m.%d %H:%M:%S'
    ))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            rotating_handler,
            logging.StreamHandler(sys.stdout)
        ]
    )

def is_dark_theme(app):
    color_scheme = app.styleHints().colorScheme()
    return color_scheme == Qt.ColorScheme.Dark

def customize_palette(app, is_dark):
    palette = app.palette()

    if is_dark:
        highlight_color = QColor(0, 99, 177)
        highlighted_text_color = QColor(255, 255, 255)
    else:
        highlight_color = QColor(145, 201, 247)
        highlighted_text_color = QColor(0, 0, 0)

    palette.setColor(QPalette.Highlight, highlight_color)
    palette.setColor(QPalette.HighlightedText, highlighted_text_color)

    app.setPalette(palette)

if __name__ == "__main__":
    setup_logging()

    app = QApplication(sys.argv)
    app.setApplicationName(name)
    app.setApplicationVersion(version)
    app.setOrganizationName(author)
    app.setOrganizationDomain(website)
    app.setStyle("Fusion")

    is_dark = is_dark_theme(app)
    customize_palette(app, is_dark)

    media_paths = None
    if len(sys.argv) > 1:
        media_paths = sys.argv[1:]

    window = MainWindow(app, "dark" if is_dark else "light", media_paths)
    window.show()

    sys.exit(app.exec())