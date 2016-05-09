import tkinter as tk
from tkinter import ttk

import streamdownloader.guiutils as guiutils

class ResolutionDialog(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

        # Label for displaying the status of the url checking thread
        self.statusLabel = ttk.Label(self, text = "Checking URL...")
        self.statusLabel.grid(row = 0, column = 0, columnspan = 2)

        # Options for resolution
        resolutions = ["foo", "bar", "baz", "foobar", "foobaz", "foobarbaz"]
        self.resolution = tk.StringVar()
        self.options = ttk.OptionMenu(self, self.resolution, resolutions[0],
            *resolutions)
        self.options.grid(row = 1, column = 0, columnspan = 2,
            sticky = (tk.W, tk.E))

        # Ok button
        self.okButton = ttk.Button(self, text = "Ok", command = self.ok)
        self.okButton.grid(row = 2, column = 0, sticky = (tk.W, tk.E))

        # Cancel button
        self.cancelButton = ttk.Button(self, text = "Cancel",
            command = self.cancel)
        self.cancelButton.grid(row = 2, column = 1, sticky = (tk.W, tk.E))

        guiutils.setChildrenPadding(self, 5, 5)

        # Expand column 1 and 2 equally
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        # Expand rows
        for i in range(0, 3):
            self.rowconfigure(i, weight = 1)

        # Configure self
        w = 300
        h = 100

        self.geometry("%dx%d" % (w, h))
        self.grid()

        # Grab focus on creation
        self.grab_set()
        self.focus()

    def ok(self):
        self.destroy()

    def cancel(self):
        self.destroy()
