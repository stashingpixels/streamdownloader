import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
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
        self.stream = None
        self.streams_thread = thread.StreamsThread(url)
        self.streams_thread.start()
        self.master.after(self.CHECK_INTERVAL, self.check_thread)

        # Label for displaying the status of the url checking thread
        self.status_label = ttk.Label(self, text="Checking URL...")
        self.status_label.grid(row=0, column=0, columnspan=2)

        # Options for resolution
        resolutions = ["foo", "bar", "baz", "foobar", "foobaz", "foobarbaz"]
        self.resolution = tk.StringVar()

        self.ok_button = ttk.Button(self, text="Ok", command=self.ok)
        self.ok_button.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.ok_button.config(state=tk.DISABLED)

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
            self.status_label.config(text="Error while getting streams from "
                                          "this URL",
                                     foreground="red")
        elif self.streams_thread.no_plugin_error is not None:
            self.status_label.config(text="This website is currently not "
                                          "supported",
                                     foreground="red")
        else:
            self.streams = self.streams_thread.streams
            self.resolutions = list(self.streams)
            self.resolutions.sort()

            default_resolution = "best"
            if "best" not in self.resolutions:
                default_resolution = self.resolutions[0]

            self.status_label.config(text="Select resolution")
            self.ok_button.config(state=tk.NORMAL)

            self.options = ttk.OptionMenu(self, self.resolution,
                                          default_resolution,
                                          *self.resolutions)
            self.options.grid(row=1, column=0, columnspan=2,
                              sticky=(tk.W, tk.E))

    def ok(self):
        self.stream = self.streams[self.resolution.get()]
        self.destroy()

    def cancel(self):
        self.destroy()


class MainWindow(ttk.Frame):
    CHECK_INTERVAL = 500
    task = None

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

        self.download_button = ttk.Button(self, text="Download",
                                          command=self.download_video)
        self.download_button.grid(row=2, column=0, columnspan=3,
                                  sticky=(tk.W, tk.E))

        # Label showing download progress
        self.progress_label = ttk.Label(self, text="")
        self.progress_label.grid(row=3, column=0, columnspan=3)

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
        if self.task is None or self.cancel_download():
            self.master.destroy()

    def browse_file(self):
        file_path = tk.filedialog.asksaveasfilename(filetypes=[
            ("MP4 files", ".mp4")
        ])

        if file_path != "":
            if "." not in file_path:
                file_path = file_path + ".mp4"

            self.file_path.set(file_path)

    def download_video(self):
        file_path = os.path.expanduser(self.file_path.get())
        if not os.access(os.path.dirname(file_path), os.W_OK):
            tk.messagebox.showerror("Invalid file",
                                    "Cannot write to target file")
            return

        dialog = ResolutionDialog(self, self.url_entry.get())
        self.wait_window(dialog)

        stream = dialog.stream
        if stream is not None:
            self.url_entry.config(state=tk.DISABLED)
            self.file_entry.config(state=tk.DISABLED)
            self.browse_button.config(state=tk.DISABLED)
            self.download_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)
            self.progress_label.config(text="Downloading...")

            self.thread = thread.DownloadThread(stream, self.file_entry.get())
            self.thread.start()
            self.task = self.after(self.CHECK_INTERVAL, self.check_download)

    def check_download(self):
        total_size = self.thread.total_size
        size_str = "{:.2f} MiB downloaded".format(total_size / 1024 ** 2)

        if not self.thread.done:
            progress_text = "Downloading... {}".format(size_str)
            self.progress_label.config(text=progress_text)
            self.task = self.after(self.CHECK_INTERVAL, self.check_download)
        else:
            progress_text = "Download complete ({})".format(size_str)
            self.progress_label.config(text=progress_text)
            self.task = None
            self.restore_widgets()

    def restore_widgets(self):
        self.url_entry.config(state=tk.NORMAL)
        self.file_entry.config(state=tk.NORMAL)
        self.browse_button.config(state=tk.NORMAL)
        self.download_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)

    def cancel_download(self):
        if self.task is not None:
            self.thread.pause()
            message = ("Your download will be cancelled. Would you like to "
                       "delete the file as well?")
            result = tk.messagebox.askyesnocancel("Cancel download?", message)

            if result is not None:
                self.after_cancel(self.task)
                self.task = None

                self.thread.cancel()
                self.thread.join()

                self.progress_label.config(text="Download cancelled")
                self.restore_widgets()

                if result:
                    try:
                        os.remove(self.file_entry.get())
                    except OSError:
                        message = ("The file could not be deleted. You may "
                                   "remove it manually when it is no longer "
                                   "in use.")
                        tk.messagebox.showwarning("Could not delete file",
                                                  message)

                return True
            else:
                self.thread.resume()
        return False
