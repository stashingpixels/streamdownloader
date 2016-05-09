import tkinter as tk

from tkinter import ttk

import streamdownloader.guiutils as guiutils
from streamdownloader.ResolutionDialog import ResolutionDialog

class MainWindow(ttk.Frame):
    def __init__(self, master = None):
        ttk.Frame.__init__(self, master)

        # Handle the close event
        if master is not None:
            self.master = master
            master.protocol("WM_DELETE_WINDOW", self.handleClose)

        # The url of the stream to download
        self.url = tk.StringVar()
        self.urlLabel = ttk.Label(self, text = "Stream URL:")
        self.urlLabel.grid(row = 0, column = 0, sticky = tk.W)
        self.urlEntry = ttk.Entry(self, textvariable = self.url)
        self.urlEntry.grid(row = 0, column = 1, columnspan = 2,
            sticky = (tk.W, tk.E))

        # The file to which the stream should be downloaded
        self.filePath = tk.StringVar()
        self.fileLabel = ttk.Label(self, text = "Target file:")
        self.fileLabel.grid(row = 1, column = 0, sticky = tk.W)
        self.fileEntry = ttk.Entry(self, textvariable = self.filePath)
        self.fileEntry.grid(row = 1, column = 1, sticky = (tk.W, tk.E))

        # The button to browse the target file
        self.browseButton = ttk.Button(self, text = "Browse...",
            command = self.browseFile)
        self.browseButton.grid(row = 1, column = 2, sticky = (tk.W, tk.E))

        # The button to download the stream
        self.downloadButton = ttk.Button(self, text = "Download",
            command = self.downloadVideo)
        self.downloadButton.grid(row = 2, column = 0, columnspan = 3,
            sticky = (tk.W, tk.E))

        # Label showing download progress
        self.progressLabel = ttk.Label(self, text = "Downloading...")
        self.progressLabel.grid(row = 3, column = 0, columnspan = 3)

        # Button to cancel download
        self.cancelButton = ttk.Button(self, text = "Cancel",
            command = self.cancelDownload)
        self.cancelButton.grid(row = 4, column = 0, columnspan = 3,
            sticky = (tk.W, tk.E))

        guiutils.setChildrenPadding(self, 5, 5)

        # Make column 1 expand
        self.columnconfigure(1, weight = 1)

        # Display
        self.grid(row = 0, column = 0, sticky = (tk.W, tk.E))

    def handleClose(self):
        self.master.destroy()

    def browseFile(self):
        pass

    def downloadVideo(self):
        self.dialog = ResolutionDialog(self)

    def cancelDownload(self):
        pass
