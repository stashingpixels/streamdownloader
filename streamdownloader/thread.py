import threading

class DownloadThread(threading.Thread):
    def __init__(self, stream, file):
        threading.Thread.__init__(self)
        self.stream = stream
        self.file = file
        self.totalSize = 0
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
            with open(self.file, "wb") as f:
                self.downloadTo(f)
        except TypeError:
            self.downloadTo(self.file)

    def downloadTo(self, file):
        streamFile = self.stream.open()
        bufferSize = 8192
        data = b""

        while not self._cancel.is_set():
            if self._pause.is_set():
                self._resume.clear()
                self._resume.wait()
                self._pause.clear()
                continue

            data = streamFile.read(bufferSize)
            dataSize = len(data)

            if dataSize == 0:
                break

            file.write(data)

            # Use another variable because += is not thread-safe
            newTotalSize = self.totalSize + dataSize
            self.totalSize = newTotalSize

        streamFile.close()
