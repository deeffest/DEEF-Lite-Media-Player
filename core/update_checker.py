import requests
import logging
from PySide6.QtCore import QThread, Signal

class UpdateChecker(QThread):
    update_checked = Signal(str, str, bool)
    update_checked_failed = Signal(str, bool)

    def __init__(self, manual_check=False):
        super().__init__()
        self.manual_check = manual_check

    def run(self):
        try:
            response = requests.get(
                "https://api.github.com/repos/deeffest/DEEF-Lite-Media-Player/releases/latest")
            response.raise_for_status()
            
            data = response.json()
            item_version = data["tag_name"]
            item_download = data.get("html_url")

            if response.status_code == 200:
                self.update_checked.emit(item_version, item_download, self.manual_check)
        except Exception as e:
            logging.error(f"Failed to check for updates: {str(e)}")            
            self.update_checked_failed.emit(str(e), self.manual_check)