import tkinter as tk
from tkinter import ttk

from streamdownloader import thread


def set_children_padding(object, padding_x, padding_y):
    for child in object.winfo_children():
        child.grid_configure(padx=padding_x, pady=padding_y)


class ResolutionDialog(tk.Toplevel):
    CHECK_INTERVAL = 100

    def __init__(self, master, url):
        tk.Toplevel.__init__(self, master)

        self.url = url
        self.streams_thread = thread.StreamsThread(url)
        self.streams_thread.start()
        self.master.after(self.CHECK_INTERVAL, self.check_thread)

        # Label for displaying the status of the url checking thread
        self.status_label = ttk.Label(self, text="Checking URL...")
        self.status_label.grid(row=0, column=0, columnspan=2)

        # Options for resolution
        resolutions = ["foo", "bar", "baz", "foobar", "foobaz", "foobarbaz"]
        self.resolution = tk.StringVar()

        # Ok button
        self.ok_button = ttk.Button(self, text="Ok", command=self.ok)
        self.ok_button.grid(row=2, column=0, sticky=(tk.W, tk.E))

        # Cancel button
        self.cancel_button = ttk.Button(self, text="Cancel",
                                        command=self.cancel)
        self.cancel_button.grid(row=2, column=1, sticky=(tk.W, tk.E))

        set_children_padding(self, 5, 5)

        # Expand column 1 and 2 equally
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Expand rows
        for i in range(0, 3):
            self.rowconfigure(i, weight=1)

        # Configure self
        w = 300
        h = 100

        self.geometry("%dx%d" % (w, h))
        self.grid()

        # Grab focus on creation
        self.grab_set()
        self.focus()

    def check_thread(self):
        if not self.streams_thread.done:
            self.master.after(self.CHECK_INTERVAL, self.check_thread)
        elif self.streams_thread.plugin_error is not None:
            self.status_label.config(text="Could not get streams from this URL")
        elif self.streams_thread.no_plugin_error is not None:
            self.status_label.config(text="This URL is currently not supported")
        else:
            self.streams = self.streams_thread.streams
            self.resolutions = list(self.streams)

            self.status_label.config(text="Select resolution")

            self.options = ttk.OptionMenu(self, self.resolution,
                                          self.resolutions[0],
                                          *self.resolutions)
            self.options.grid(row=1, column=0, columnspan=2,
                              sticky=(tk.W, tk.E))

    def ok(self):
        self.destroy()

    def cancel(self):
        self.destroy()


class MainWindow(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        # Handle the close event
        if master is not None:
            self.master = master
            master.protocol("WM_DELETE_WINDOW", self.handle_close)

        # The url of the stream to download
        self.url = tk.StringVar()
        self.url_label = ttk.Label(self, text="Stream URL:")
        self.url_label.grid(row=0, column=0, sticky=tk.W)
        self.url_entry = ttk.Entry(self, textvariable=self.url)
        self.url_entry.grid(row=0, column=1, columnspan=2,
                            sticky=(tk.W, tk.E))

        # The file to which the stream should be downloaded
        self.file_path = tk.StringVar()
        self.file_label = ttk.Label(self, text="Target file:")
        self.file_label.grid(row=1, column=0, sticky=tk.W)
        self.file_entry = ttk.Entry(self, textvariable=self.file_path)
        self.file_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # The button to browse the target file
        self.browse_button = ttk.Button(self, text="Browse...",
                                        command=self.browse_file)
        self.browse_button.grid(row=1, column=2, sticky=(tk.W, tk.E))

        # The button to download the stream
        self.download_button = ttk.Button(self, text="Download",
                                          command=self.download_video)
        self.download_button.grid(row=2, column=0, columnspan=3,
                                  sticky=(tk.W, tk.E))

        # Label showing download progress
        self.progress_label = ttk.Label(self, text="Downloading...")
        self.progress_label.grid(row=3, column=0, columnspan=3)

        # Button to cancel download
        self.cancel_button = ttk.Button(self, text="Cancel",
                                        command=self.cancel_download)
        self.cancel_button.grid(row=4, column=0, columnspan=3,
                                sticky=(tk.W, tk.E))

        set_children_padding(self, 5, 5)

        # Make column 1 expand
        self.columnconfigure(1, weight=1)

        # Display
        self.grid(row=0, column=0, sticky=(tk.W, tk.E))

    def handle_close(self):
        self.master.destroy()

    def browse_file(self):
        pass

    def download_video(self):
        self.dialog = ResolutionDialog(self, self.url_entry.get())

    def cancel_download(self):
        pass
