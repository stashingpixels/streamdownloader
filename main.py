import tkinter as tk
from streamdownloader import gui

if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight = 1)
    root.rowconfigure(0, weight = 1)
    root.title("Stream Downloader")

    x = 400
    y = 200
    w = 400
    h = 200

    root.geometry("%dx%d+%d+%d" % (w, h, x, y))

    mainWindow = gui.MainWindow(root)
    root.mainloop()
