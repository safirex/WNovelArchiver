
from win10toast import ToastNotifier
from pystray import *#Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw



class SysTrayUI:
    def __init__(self):

        self.icon_path = "icon.png"

        self.toaster = ToastNotifier()
        self.menu_items = [
            MenuItem("Download",lambda: self.download()),
            MenuItem("Update",lambda: self.update()),
            MenuItem("Test Notification", lambda: self.toaster.show_toast("Test",threaded=True)),
            MenuItem("Exit", lambda: self.icon.stop()),
        ]

    def create_image(self):
        width = 32
        height = 32
        color1 = "white"
        color2 = "black"

        # Generate an image and draw a pattern
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            (width // 2, 0, width, height // 2),
            fill=color2)
        dc.rectangle(
            (0, height // 2, width // 2, height),
            fill=color2)

        return image
    def run(self):
        self.menu = Menu(*self.menu_items)
        self.icon = Icon("Test Name", menu=self.menu)
        self.icon.icon = self.create_image();

        self.icon.run()

    def update(self):
        self.toaster.show_toast("Update start",threaded=True)
        archive_updater.archiveUpdate()
        self.toaster.show_toast("Update finished",threaded=True)
    def download(self):
        self.toaster.show_toast("Download start",threaded=True)
        archive_updater.download()
        self.toaster.show_toast("Download finished",threaded=True)


import archive_updater
def setup():
    tray=SysTrayUI()
    tray.run()
