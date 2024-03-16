![icon-0](https://github.com/deeffest/DEEF-Lite-Media-Player/assets/117280555/176ed8a3-86d5-4e9d-8663-12050e924032)

# DEEF-Lite-Media-Player

A simple App for playing media files on your Windows PC, written in [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) and its QMediaPlayer.

Supported media formats (the list is frequently updated): \
 `mp3`, `wav`, `ogg`, `flac`, `aac`, `wma`, `m4a`, `opus`, `webm`, `mp4`, `avi`, `mov`, `m3u`, `3gpp`, and `mkv`

## Screenshots

![image](https://github.com/deeffest/DEEF-Lite-Media-Player/assets/117280555/05e5619c-e225-4ebc-8b70-f2e62a59a920)

## Start using

1. Download and install [LAV Filters](https://github.com/Nevcairiel/LAVFilters/releases/download/0.78/LAVFilters-0.78-Installer.exe) 
2. Download and install `DLMPlayer-Setup.exe` from the releases page: https://github.com/deeffest/DEEF-Lite-Media-Player/releases

>To use DLMPlayer without LAV Filters, you need to set Windows Media Foundation as "Preferred multimedia plugin" in the "Player"    settings, instead of the default DirectShow._

## Use DLMPlayer as default media player in Windows

1. Locate the DLMPlayer.exe program on your computer. Make sure you know the exact file path (C:\Program Files\DEEF Lite Media Player\DLMPlayer.exe).

2. Right-click on an media file (e.g., MP4, MP3) that you want to open with DLMPlayer.exe.

3. From the context menu, select "Open with" and then click on "Choose another app."

4. A window will appear with a list of available apps. If DLMPlayer.exe is listed, select it. If it's not listed, click on the option "More apps" at the bottom of the list.

5. In the "Choose an app" window, scroll down and click on the link "Look for another app on this PC."

6. Navigate to the file path where DLMPlayer.exe is located. Select DLMPlayer.exe and click "Open."

7. Windows will now open the selected image file with DLMPlayer.exe. Additionally, DLMPlayer.exe will be added to the list of available apps for opening image files by default.

8. Repeat steps 2-7 for other media file types if you want DLMPlayer.exe to be the default viewer for those file types as well.

---

Now, whenever you double-click on an media file, Windows will open it using DLMPlayer.exe by default!
