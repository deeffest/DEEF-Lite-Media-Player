from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QSizePolicy, QMenu, QAction
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMouseEvent, QIcon

class VideoWidget(QVideoWidget):
    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent)
        self.window = parent
        self.isDragging = False
        self.contextMenuActive = False
        self.drag_position = 0

        self._init_content()

    def contextMenuEvent(self, event):
        self.contextMenuActive = True
        contextMenu = QMenu(self)

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

        contextMenu.addAction(self.window.actionExit_2)

        contextMenu.exec_(event.globalPos())

    def _init_content(self):
        self.mouse_timer = QTimer(self)
        self.mouse_timer.setInterval(3000)
        self.mouse_timer.timeout.connect(self.hide_elements)

        self.setMouseTracking(True)  

    def hide_elements(self):
        self.setCursor(Qt.BlankCursor)

    def show_elements(self):
        self.setCursor(Qt.ArrowCursor)  

    def hide_playbar(self):
        if self.window.isFullScreen():
            self.window.menubar.hide()
            if self.window.settings.value("preset_2", "false") == "false":
                self.window.frame_3.hide()
            if self.window.settings.value("preset_3", "false") == "false":
                self.window.frame.hide()
            if self.window.settings.value("preset_4", "false") == "false":
                self.window.frame_2.hide()  

    def show_playbar(self):
        if self.window.isFullScreen():
            if self.window.settings.value("preset_2", "false") == "false":
                self.window.frame_3.show()
            if self.window.settings.value("preset_3", "false") == "false":
                self.window.frame.show()
            if self.window.settings.value("preset_4", "false") == "false":
                self.window.frame_2.show()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.contextMenuActive = False

        if event.buttons() == Qt.LeftButton and self.drag_position:
            if not self.isDragging: 
                self.isDragging = True 
            if not self.window.isFullScreen():
                if self.window.settings.value("movable_window", "false") == 'true':
                    self.window.move(event.globalPos() - self.drag_position)
        
        self.mouse_timer.stop() 

        hot_zone_height = 80
        if self.window.isFullScreen():
            window_height = self.window.height()
            
            if event.pos().y() > window_height - hot_zone_height:
                self.show_playbar()
            else:
                self.hide_playbar()

        self.show_elements()

        self.mouse_timer.start()

        super(VideoWidget, self).mouseMoveEvent(event) 

    def mousePressEvent(self, event: QMouseEvent):
        self.drag_position = event.globalPos() - self.window.frameGeometry().topLeft()
        self.isDragging = False
        super(VideoWidget, self).mousePressEvent(event)
        
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if not self.isDragging:  
                if self.contextMenuActive == True:
                    self.contextMenuActive = False
                else:
                    self.window.play_pause_media()
            self.drag_position = event.globalPos() - self.window.frameGeometry().topLeft()
            self.isDragging = False 
                
        super(VideoWidget, self).mouseReleaseEvent(event)

    def enterEvent(self, event):
        self.mouse_timer.start()

        super(VideoWidget, self).enterEvent(event)

    def leaveEvent(self, event):
        self.mouse_timer.stop()
        self.show_elements()

        super(VideoWidget, self).leaveEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.window.open_fullscreen()

        super(VideoWidget, self).mouseDoubleClickEvent(event)