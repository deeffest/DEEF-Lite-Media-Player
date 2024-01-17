#init_icons.py
from PyQt5.QtGui import QIcon, QPixmap

def _init_icons(window, icon_folder, theme=None):
    icons = {
        "toolButton_5": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/replay_10_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/replay_10_white_24dp.svg", 
            "disabled_off": None,
        },
        "toolButton": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/skip_previous_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/skip_previous_white_24dp.svg", 
            "disabled_off": None,
        },
        "toolButton_2": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/pause_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/play_arrow_white_24dp.svg", 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/pause_white_24dp.svg", 
            "disabled_off": f"{window.current_dir}/resources/icons/disabled_icons/play_arrow_white_24dp.svg",
        },
        "toolButton_3": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/skip_next_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/skip_next_white_24dp.svg", 
            "disabled_off": None,
        },
        "toolButton_6": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/forward_10_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/forward_10_white_24dp.svg", 
            "disabled_off": None,
        },
        "toolButton_9": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/stop_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/stop_white_24dp.svg", 
            "disabled_off": None,
        },            
        "toolButton_4": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/volume_up_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/volume_off_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },

        "actionOpen_file": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/file_open_white_24dp.svg",
            "normal_off": None,
            "disabled": None, 
            "disabled_off": None,
        },
        "actionOpen_File_URL": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/link_white_24dp.svg",
            "normal_off": None,
            "disabled": None, 
            "disabled_off": None,
        },
        "actionOpen_Folder": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/folder_open_white_24dp.svg",
            "normal_off": None,
            "disabled": None, 
            "disabled_off": None,
        },
        "actionProperties": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/info_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/info_white_24dp.svg",
            "disabled_off": None,
        },
        "actionClose": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/cancel_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/cancel_white_24dp.svg",
            "disabled_off": None,
        },
        "actionExit_2": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/exit_to_app_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },

        "menuPresets": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/list_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },
        "actionPreset1": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_outline_blank_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },
        "actionPreset2": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_outline_blank_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },
        "actionPreset3": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_outline_blank_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },
        "actionPreset4": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_outline_blank_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },
        "menuWindow_Flags": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/computer_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },
        "actionFrameless": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_outline_blank_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },
        "actionMovable": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_outline_blank_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },
        "actionOn_Top": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_outline_blank_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },
        "actionFullscreen": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/fullscreen_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/close_fullscreen_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },
        "actionSettings": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/settings_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },

        "actionPrevious_2": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/skip_previous_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/skip_previous_white_24dp.svg",
            "disabled_off": None,
        },
        "actionNext_2": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/skip_next_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/skip_next_white_24dp.svg",
            "disabled_off": None,
        },
        "actionGo_To": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/schedule_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/schedule_white_24dp.svg",
            "disabled_off": None,
        },

        "actionSave_As": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/save_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/save_white_24dp.svg",
            "disabled_off": None,
        },
        "actionShuffle": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/shuffle_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/shuffle_white_24dp.svg",
            "disabled_off": None,
        },
        "actionClear": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/close_white_24dp.svg",
            "normal_off": None,
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/close_white_24dp.svg",
            "disabled_off": None,
        },
        "actionAutoPlay": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_outline_blank_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/check_box_white_24dp.svg",
            "disabled": None, 
            "disabled_off": None,
        },

        "actionCheck_for_updates": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/update_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },
        "actionReport": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/bug_report_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },
        "actionDonate": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/favorite_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },
        "actionAbout": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/help_white_24dp.svg",
            "normal_off": None,
            "disabled": None,
            "disabled_off": None,
        },

        "actionPlay_Pause": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/pause_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/play_arrow_white_24dp.svg", 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/pause_white_24dp.svg", 
            "disabled_off": f"{window.current_dir}/resources/icons/disabled_icons/play_arrow_white_24dp.svg",
        },
        "actionStop": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/stop_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/stop_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionRepeat": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/repeat_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/repeat_on_white_24dp.svg", 
            "disabled": None, 
            "disabled_off": None,
        },
        "actionRewind": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/replay_10_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/replay_10_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionForward": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/forward_10_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/forward_10_white_24dp.svg", 
            "disabled_off": None,
        },
        "menuSpeed": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/speed_white_24dp.svg",
            "normal_off": None, 
            "disabled": None, 
            "disabled_off": None,
        },            
        "actionUp_3": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/keyboard_arrow_up_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/keyboard_arrow_up_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionDown_3": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/keyboard_arrow_down_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/keyboard_arrow_down_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionReset_Speed": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/1x_mobiledata_white_24dp.svg",
            "normal_off": None, 
            "disabled": None, 
            "disabled_off": None,
        },
        "menuVolume": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/equalizer_white_24dp.svg",
            "normal_off": None, 
            "disabled": None, 
            "disabled_off": None,
        },
        "actionUp_2": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/keyboard_arrow_up_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/keyboard_arrow_up_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionDown_2": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/keyboard_arrow_down_white_24dp.svg",
            "normal_off": None, 
            "disabled": f"{window.current_dir}/resources/icons/disabled_icons/keyboard_arrow_down_white_24dp.svg", 
            "disabled_off": None,
        },
        "actionMute_Unmute_2": {
            "normal": f"{window.current_dir}/resources/icons/{icon_folder}/volume_up_white_24dp.svg",
            "normal_off": f"{window.current_dir}/resources/icons/{icon_folder}/volume_off_white_24dp.svg",
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