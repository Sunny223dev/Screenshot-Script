import pyautogui
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import random
import string
import os
from PyQt5.QtGui import QGuiApplication, QImage, QPixmap
from PyQt5.QtWidgets import QApplication
import sys
import io
import keyboard
import time
import threading

pyqt_app = QApplication(sys.argv)

# checks if ss folder is real if not create one
def check_screenshot_folder():
    directory = os.path.join(os.getcwd(), "screenshots")
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

# make images have rdm file name
def own_file_name(directory, extension="png"):
    while True:
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + f".{extension}"
        full_path = os.path.join(directory, filename)
        if not os.path.exists(full_path):
            return full_path

# auto copy image to clipboard 
def auto_copy_image_to_clipboard(image_path):
    image = Image.open(image_path)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    byte_data = buffer.getvalue()
    qimage = QImage.fromData(byte_data)
    clipboard = QGuiApplication.clipboard()
    clipboard.setPixmap(QPixmap.fromImage(qimage))
    print(f"Image was copied to your clipboard: {image_path}")

# add corner image
def add_corner_image(image, border_size=2, border_color='white'):
    img_with_border = Image.new("RGBA", (image.width + border_size * 2, image.height + border_size * 2), (255, 255, 255, 0))
    img_with_border.paste(image, (border_size, border_size))
    draw = ImageDraw.Draw(img_with_border)
    draw.rectangle([(border_size//2, border_size//2), 
                    (img_with_border.width - border_size//2, img_with_border.height - border_size//2)], 
                   outline=border_color, width=border_size)
    return img_with_border

# take ss and be able to draw a box around where you want to select
class ScreenshotScript:
    def __init__(self, root):
        self.root = root
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)

    def on_mouse_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, cur_x, cur_y, outline='black', width=2.3)

    def on_button_release(self, event):
        end_x, end_y = event.x, event.y
        self.take_screenshot(self.start_x, self.start_y, end_x, end_y)

    def take_screenshot(self, start_x, start_y, end_x, end_y):
        self.root.withdraw()
        time.sleep(0.1)

        # adjust capture coordinates based on the screen resolution and cursor position
        x1 = self.root.winfo_rootx() + start_x
        y1 = self.root.winfo_rooty() + start_y
        x2 = self.root.winfo_rootx() + end_x
        y2 = self.root.winfo_rooty() + end_y

        # take the ss using pyautogui
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        # save the ss
        directory = check_screenshot_folder()
        screenshot_path = own_file_name(directory)
        screenshot.save(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")

        # auto copy the ss to the clipboard
        auto_copy_image_to_clipboard(screenshot_path)

        # display the ss in corner
        display_corner_image(screenshot_path)

# display corner image
def display_corner_image(image_path):
    img_window = tk.Toplevel(root)
    img_window.overrideredirect(True)
    img = Image.open(image_path)
    max_size = (300, 300)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)  
    img_with_border = add_corner_image(img)
    img_width, img_height = img_with_border.size
    window_width, window_height = img_width, img_height
    screen_width = img_window.winfo_screenwidth()
    screen_height = img_window.winfo_screenheight()
    img_window.geometry(f"{window_width}x{window_height}+{screen_width-window_width-10}+{screen_height-window_height-40}")
    photo = ImageTk.PhotoImage(img_with_border)
    img_label = tk.Label(img_window, image=photo, bg='black')
    img_label.image = photo
    img_label.pack()
    img_window.after(1560, img_window.destroy)

def snip_it():
    screenshot_window = tk.Toplevel(root)
    screenshot_window.attributes("-alpha", 0.2)  
    screenshot_window.attributes("-fullscreen", True)
    screenshot_window.attributes("-topmost", True)
    screenshot_window.focus_force()
    ScreenshotScript(screenshot_window)

# listen for F2 key and start ss
def listen_f2():
    keyboard.add_hotkey('f2', snip_it)
    keyboard.wait('esc')

root = tk.Tk()
root.withdraw()
f2_listener_thread = threading.Thread(target=listen_f2, daemon=True)
f2_listener_thread.start()
root.mainloop()
