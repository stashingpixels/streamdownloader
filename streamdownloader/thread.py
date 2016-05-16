import threading

import livestreamer


class StreamsThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.done = False
        self.plugin_error = None
        self.no_plugin_error = None
        self.streams = None

    def run(self):
        try:
            streams = livestreamer.streams(self.url)
            self.streams = streams
        except livestreamer.NoPluginError as no_plugin_error:
            self.no_plugin_error = no_plugin_error
        except livestreamer.PluginError as plugin_error:
            self.plugin_error = plugin_error

        self.done = True


class DownloadThread(threading.Thread):
    def __init__(self, stream, output_file):
        threading.Thread.__init__(self)
        self.stream = stream
        self.output_file = output_file
        self.total_size = 0
        self._pause = threading.Event()
        self._resume = threading.Event()
        self._cancel = threading.Event()

    def cancel(self):
        if self._pause.is_set():
            self._resume.set()

        self._cancel.set()

    def pause(self):
        self._resume.clear()
        self._pause.set()

    def resume(self):
        self._pause.clear()
        self._resume.set()

    def run(self):
        try:
            with open(self.output_file, "wb") as f:
                self.download_to(f)
        except TypeError:
            self.download_to(self.output_file)

    def download_to(self, output_file):
        stream_file = self.stream.open()
        buffer_size = 8192
        data = b""

        while not self._cancel.is_set():
            if self._pause.is_set():
                self._resume.clear()
                self._resume.wait()
                self._pause.clear()
                continue

            data = stream_file.read(buffer_size)
            data_size = len(data)

            if data_size == 0:
                break

            output_file.write(data)

            # Use another variable because += is not thread-safe
            new_total_size = self.total_size + data_size
            self.total_size = new_total_size

        stream_file.close()
