import sys
import webbrowser

def _init_connect(self):
    self.player.stateChanged.connect(self.check_media_state)
    self.player.mediaStatusChanged.connect(self.check_media_status)
    self.player.positionChanged.connect(self.update_media_position)
    self.player.durationChanged.connect(self.update_media_duration)
    self.player.error.connect(self.handle_media_errors)
    self.horizontalSlider_2.valueChanged.connect(self.change_media_volume)
    self.toolButton_2.clicked.connect(self.play_pause_media)
    self.toolButton_4.clicked.connect(self.toggle_media_mute)   
    self.toolButton_5.clicked.connect(self.rewind_media)
    self.toolButton_6.clicked.connect(self.forward_media) 
    self.actionOpen_file.triggered.connect(self.open_file_dialog)
    self.actionOpen_File_URL.triggered.connect(self.open_media_dialog)
    self.actionExit_2.triggered.connect(self.exit_app)   
    self.actionFullscreen.triggered.connect(self.open_fullscreen)
    self.toolButton_9.clicked.connect(self.stop_media)
    self.actionPlay_Pause.triggered.connect(self.play_pause_media)
    self.actionStop.triggered.connect(self.stop_media)
    self.actionOpen_Folder.triggered.connect(self.open_folder_dialog)
    self.actionRepeat.triggered.connect(self.toggle_media_repeat)
    self.actionRewind.triggered.connect(self.rewind_media)
    self.actionForward.triggered.connect(self.forward_media)
    self.actionUp_3.triggered.connect(self.increase_playback_speed)
    self.actionDown_3.triggered.connect(self.decrease_playback_speed)
    self.actionReset_Speed.triggered.connect(self.reset_playback_speed)
    self.actionUp_2.triggered.connect(self.increase_media_volume)
    self.actionDown_2.triggered.connect(self.decrease_media_volume)
    self.actionMute_Unmute_2.triggered.connect(self.toggle_media_mute)
    self.actionClose.triggered.connect(self.close_media)
    self.toolButton.clicked.connect(self.open_previous_media)
    self.toolButton_3.clicked.connect(self.open_next_media)
    self.actionPrevious_2.triggered.connect(self.open_previous_media)
    self.actionNext_2.triggered.connect(self.open_next_media)
    self.tool_btn_previous.clicked.connect(self.open_previous_media)
    self.tool_btn_next.clicked.connect(self.open_next_media)
    self.tool_btn_play_pause.clicked.connect(self.play_pause_media)
    self.actionGo_To.triggered.connect(self.open_go_to_dialog)
    self.actionProperties.triggered.connect(self.open_properties_dialog)
    self.actionClear.triggered.connect(self.playlist_cleaner)
    self.actionShuffle.triggered.connect(self.shuffle_playlist)
    self.actionSave_As.triggered.connect(self.save_playlist_as_m3u)
    self.actionPreset4.triggered.connect(self.click_on_preset4)
    self.actionPreset3.triggered.connect(self.click_on_preset3)
    self.actionPreset2.triggered.connect(self.click_on_preset2)
    self.actionPreset1.triggered.connect(self.click_on_preset1)
    self.actionFrameless.triggered.connect(self.handle_frameless_window)
    self.actionMovable.triggered.connect(self.handle_movable_window)
    self.actionOn_Top.triggered.connect(self.handle_on_top_window)
    self.actionSettings.triggered.connect(self.open_settings_dialog)
    self.actionCheck_for_updates.triggered.connect(self.check_for_updates)
    self.actionReport.triggered.connect(lambda: webbrowser.open_new_tab("https://github.com/deeffest/DEEF-Lite-Media-Player/issues/new/choose"))
    self.actionDonate.triggered.connect(lambda: webbrowser.open_new_tab("https://donationalerts.com/r/deeffest"))
    self.actionAbout.triggered.connect(self.open_about_dialog)

    self.horizontalSlider.mousePressEvent = self.on_slider_pressed
    self.horizontalSlider.mouseMoveEvent = self.on_slider_moved
    self.horizontalSlider.enterEvent = self.on_slider_enter
    self.horizontalSlider_2.mousePressEvent = self.on_volume_slider_pressed
    self.horizontalSlider_2.mouseMoveEvent = self.on_volume_slider_moved