from PyQt5.QtCore import Qt

def _init_config(self):        
	if self.settings.value("preset_1", False) == "true":
		self.menubar.hide()
		self.actionPreset1.setChecked(True)
	if self.settings.value("preset_2", False) == "true":
		self.frame_3.hide()
		self.actionPreset2.setChecked(True)
	if self.settings.value("preset_3", False) == "true":
		self.frame.hide()
		self.actionPreset3.setChecked(True)
	if self.settings.value("preset_4", False) == "true":
		self.frame_2.hide()
		self.actionPreset4.setChecked(True)

	if self.settings.value("frameless_window", False) == "true":
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.actionFrameless.setChecked(True)
		self.show()
	if self.settings.value("movable_window", True) == "true":
		self.actionMovable.setChecked(True)
	if self.settings.value("on_top_window", False) == "true":
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.actionOn_Top.setChecked(True)
		self.show()