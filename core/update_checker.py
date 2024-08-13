import requests
import logging
from PySide6.QtCore import QThread, Signal

class UpdateChecker(QThread):
    update_checked = Signal(str, str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            response = requests.get(
                "https://api.github.com/repos/deeffest/DEEF-Lite-Media-Player/releases/latest")
            response.raise_for_status()
            
            data = response.json()
            item_version = data["name"]
            item_download = data.get("html_url")
        except requests.exceptions.RequestException as e:
            logging.error("UpdateChecker RequestException: " + str(e))
            return
        except Exception as e:
            logging.error("UpdateChecker UnexpectedError: " + str(e))
            return
        
        if response.status_code == 200:
            self.update_checked.emit(item_version, item_download)