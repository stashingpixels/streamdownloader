import unittest
from streamdownloader import thread


class MockFile:
    def __init__(self):
        self.size = 0

    def write(self, data):
        self.size += len(data)


class MockStreamFile:
    def __init__(self, size):
        self.position = 0
        self.size = size

    def read(self, buffer_size):
        previous_position = self.position
        self.position = min(self.position + buffer_size, self.size)
        return "a" * (self.position - previous_position)

    def close(self):
        pass


class MockStream:
    def __init__(self, size):
        self.size = size

    def open(self):
        return MockStreamFile(self.size)


class TestDownloadThread(unittest.TestCase):
    TIMEOUT = 3

    def setUp(self):
        self.stream = MockStream(40 * 1024)
        self.file = MockFile()
        self.thread = thread.DownloadThread(self.stream, self.file)

    def test_starting_size(self):
        self.assertEqual(0, self.thread.total_size)

    def test_terminates(self):
        self.thread.start()
        self.thread.join(self.TIMEOUT)
        self.assertFalse(self.thread.is_alive())

    def test_downloads_everything(self):
        self.thread.start()
        self.thread.join(self.TIMEOUT)
        self.assertEqual(self.stream.size, self.file.size)

    def test_pause_resume_works(self):
        # Pause before starting the thread or it might finish before the event
        # is sent
        self.thread.pause()
        self.thread.start()
        self.thread.join(1)
        self.assertTrue(self.thread.is_alive())

        current_size = self.file.size
        self.thread.join(1)
        self.assertEqual(current_size, self.file.size)

        self.thread.resume()
        self.thread.join(self.TIMEOUT)
        self.assertEqual(self.stream.size, self.file.size)
        self.assertFalse(self.thread.is_alive())

    # Calling pause when the thread is already paused should have no effect
    def test_no_double_pause(self):
        self.thread.pause()
        self.thread.start()
        self.thread.pause()
        self.thread.resume()
        self.thread.join(self.TIMEOUT)
        self.assertFalse(self.thread.is_alive())

    # Calling resume before pausing the thread should have no effect
    def test_no_pre_resume(self):
        self.thread.resume()
        self.thread.pause()
        self.thread.start()
        self.thread.join(self.TIMEOUT)
        self.assertTrue(self.thread.is_alive())
        self.thread.resume()
        self.thread.join(self.TIMEOUT)
        self.assertFalse(self.thread.is_alive())

    def test_cancel_works(self):
        self.thread.cancel()
        self.thread.start()
        self.thread.join(self.TIMEOUT)
        self.assertFalse(self.thread.is_alive())
        self.assertEqual(0, self.file.size)

    def test_cancel_when_paused_works(self):
        self.thread.pause()
        self.thread.start()
        self.thread.cancel()
        self.thread.join(self.TIMEOUT)
        self.assertFalse(self.thread.is_alive())
        self.assertEqual(0, self.file.size)
