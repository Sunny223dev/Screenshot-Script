# 📸 Screenshot Script
Screenshot Script made in Python using Tkinter and PyQt5. The script first checks if there is a "screenshots" folder in the project directory; if not, it creates one. When you press the F2 button on your keyboard, the screenshot screen opens, allowing you to draw around the area you want to capture. Once you're done selecting, the screenshot will automatically copy to your clipboard for easy sharing. All screenshots are also saved in the "screenshots" folder.

# 📦 Required Installations
- Image Proccessing - `pip install pillow`
- To Take Screenshots - `pip install pyautogui`
- Clipboard Copy - `pip install pyqt5`
- For Hotkey - `pip install keyboard`

# ⚠️ Known Issues
- Can't screenshot on other monitors; only the main one.
- Screen doesn't freeze when taking a screenshot.
- Can hold F2, and it will spam the screenshot screen.
