from PySide6.QtWidgets import QMainWindow
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QTimer

class VideoWidget(QVideoWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.inactivity_timer = QTimer(self)
        self.inactivity_timer.setInterval(3000)
        self.inactivity_timer.timeout.connect(self.hide_cursor)

        self.tool_bar_and_status_bar_zone_height = 61
    
        self.setMouseTracking(True)
        self.children()[0].setMouseTracking(True)

    def hide_cursor(self):
        if self.parent().isFullScreen():
            self.setCursor(Qt.BlankCursor)

    def show_cursor(self):
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if isinstance(self.parent(), QMainWindow):
                self.parent().toggle_play_pause()
        event.accept()

    def mouseDoubleClickEvent(self, event):
        if isinstance(self.parent(), QMainWindow):
            self.parent().toggle_fullscreen()
            self.parent().toggle_play_pause()
        event.accept()

    def mouseMoveEvent(self, event):
        if self.parent().isFullScreen():
            self.inactivity_timer.stop()
            self.show_cursor()

            window_height = self.parent().height()
            mouse_y = event.y()
            
            is_bottom_zone = mouse_y > window_height - self.tool_bar_and_status_bar_zone_height
            self.parent().tool_bar.setVisible(is_bottom_zone)
            self.parent().status_bar.setVisible(is_bottom_zone)

            self.inactivity_timer.start()

    def enterEvent(self, event):
        if self.parent().isFullScreen():
            self.inactivity_timer.start()

    def leaveEvent(self, event):
        self.inactivity_timer.stop()
        self.show_cursor()