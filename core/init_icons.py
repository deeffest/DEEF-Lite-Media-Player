from PyQt5.QtGui import QIcon, QPixmap

def _init_icons(window, theme):
    icons = {
        "toolButton_5": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/replay_10_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/replay_10_white_24dp.svg", 
            "disabled_off": None,
        },
        "toolButton": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/skip_previous_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/skip_previous_white_24dp.svg", 
            "disabled_off": None,
        },
        "toolButton_2": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/pause_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{theme}/play_arrow_white_24dp.svg", 
            "disabled": f"{window.current_dir}/resources/icons/disabled/pause_white_24dp.svg", 
            "disabled_off": f"{window.current_dir}/resources/icons/disabled/play_arrow_white_24dp.svg",
        },
        "toolButton_3": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/skip_next_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/skip_next_white_24dp.svg", 
            "disabled_off": None,
        },
        "toolButton_6": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/forward_10_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/forward_10_white_24dp.svg", 
            "disabled_off": None,
        },
        "toolButton_9": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/stop_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/stop_white_24dp.svg", 
            "disabled_off": None,
        },            
        "toolButton_4": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/volume_up_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{theme}/volume_off_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },

        "actionOpen_file": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/file_open_white_24dp.svg",
            "normal_off": None,
            "disabled": None, 
            "disabled_off": None,
        },
        "actionOpen_File_URL": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/link_white_24dp.svg",
            "normal_off": None,
            "disabled": None, 
            "disabled_off": None,
        },
        "actionOpen_Folder": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/folder_open_white_24dp.svg",
            "normal_off": None,
            "disabled": None, 
            "disabled_off": None,
        },
        "actionProperties": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/info_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled/info_white_24dp.svg",
            "disabled_off": None,
        },
        "actionClose": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/cancel_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled/cancel_white_24dp.svg",
            "disabled_off": None,
        },
        "actionExit_2": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/exit_to_app_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },

        "menuPresets": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/list_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },
        "menuWindow_Flags": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/computer_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },
        "actionFullscreen": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/fullscreen_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{theme}/close_fullscreen_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },
        "actionSettings": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/settings_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },

        "actionPrevious_2": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/skip_previous_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled/skip_previous_white_24dp.svg",
            "disabled_off": None,
        },
        "actionNext_2": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/skip_next_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled/skip_next_white_24dp.svg",
            "disabled_off": None,
        },
        "actionGo_To": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/schedule_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled/schedule_white_24dp.svg",
            "disabled_off": None,
        },

        "menuOptions": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/list_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },
        "actionSave_As": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/save_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled/save_white_24dp.svg",
            "disabled_off": None,
        },
        "actionShuffle": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/shuffle_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled/shuffle_white_24dp.svg",
            "disabled_off": None,
        },
        "actionClear": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/close_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled/close_white_24dp.svg",
            "disabled_off": None,
        },

        "actionCheck_for_updates": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/update_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },
        "actionReport": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/bug_report_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },
        "actionDonate": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/favorite_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },
        "actionAbout": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/help_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },

        "actionPlay_Pause": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/pause_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{theme}/play_arrow_white_24dp.svg", 
            "disabled": f"{window.current_dir}/resources/icons/disabled/pause_white_24dp.svg", 
            "disabled_off": f"{window.current_dir}/resources/icons/disabled/play_arrow_white_24dp.svg",
        },
        "actionStop": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/stop_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/stop_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionRepeat": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/repeat_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{theme}/repeat_on_white_24dp.svg", 
            "disabled": None, 
            "disabled_off": None,
        },
        "actionRewind": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/replay_10_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/replay_10_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionForward": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/forward_10_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/forward_10_white_24dp.svg", 
            "disabled_off": None,
        },
        "menuSpeed": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/speed_white_24dp.svg",
            "normal_off": None, 
            "disabled": None, 
            "disabled_off": None,
        },            
        "actionUp_3": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/keyboard_arrow_up_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/keyboard_arrow_up_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionDown_3": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/keyboard_arrow_down_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/keyboard_arrow_down_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionReset_Speed": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/1x_mobiledata_white_24dp.svg",
            "normal_off": None, 
            "disabled": None, 
            "disabled_off": None,
        },
        "menuVolume": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/equalizer_white_24dp.svg",
            "normal_off": None, 
            "disabled": None, 
            "disabled_off": None,
        },
        "actionUp_2": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/keyboard_arrow_up_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/keyboard_arrow_up_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionDown_2": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/keyboard_arrow_down_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled/keyboard_arrow_down_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionMute_Unmute_2": {
            "normal": f"{window.current_dir}/resources/icons/{theme}/volume_up_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{theme}/volume_off_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },
    }
    for action_name, icon_paths in icons.items():
        action = getattr(window, action_name, None)
        if action:
            icon = QIcon()
            if icon_paths.get("normal"):
                icon.addPixmap(QPixmap(icon_paths["normal"]), QIcon.Normal, QIcon.Off)
            if icon_paths.get("normal_off"):
                icon.addPixmap(QPixmap(icon_paths["normal_off"]), QIcon.Normal, QIcon.On)
            if icon_paths.get("disabled"):
                icon.addPixmap(QPixmap(icon_paths["disabled"]), QIcon.Disabled, QIcon.Off)
            if icon_paths.get("disabled_off"):
                icon.addPixmap(QPixmap(icon_paths["disabled_off"]), QIcon.Disabled, QIcon.On)
            action.setIcon(icon)
        else:
            print(f"Action {action_name} not found in the Window class.")