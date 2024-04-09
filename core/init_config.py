from PyQt5.QtCore import Qt

def _init_config(self):        
	if self.settings.value("preset_1", "false") == "true":
		self.menubar.hide()
		self.actionPreset1.setChecked(True)
	if self.settings.value("preset_2", "false") == "true":
		self.frame_3.hide()
		self.actionPreset2.setChecked(True)
	if self.settings.value("preset_3", "false") == "true":
		self.frame.hide()
		self.actionPreset3.setChecked(True)
	if self.settings.value("preset_4", "false") == "true":
		self.frame_2.hide()
		self.actionPreset4.setChecked(True)

	if self.settings.value("movable_window", "false") == "true":
		self.actionMovable.setChecked(True)
	if self.settings.value("on_top_window", "false") == "true":
		self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
		self.actionOn_Top.setChecked(True)
		self.show()
	if self.settings.value("frameless_window", "false") == "true":
		self.setWindowFlag(Qt.FramelessWindowHint, True)
		self.actionFrameless.setChecked(True)
		self.show()