# Stream Downloader [![Build Status](https://travis-ci.org/stashingpixels/streamdownloader.svg?branch=master)](https://travis-ci.org/stashingpixels/streamdownloader)
A small program for downloading livestreams and videos.

## Prerequisites
### Installing Python
In order to use Stream Downloader, you must have
Python installed.

#### Windows and Mac
You can download an installer from the [Python website](https://www.python.org)
(you need to install version 3 or above). Make sure to add Python to your path
if the installer asks you to. Otherwise you may need to do this manually.

#### Linux
If your distribution doesn't come with Python 3, you should be able to install
it using your package manager. For example, on Ubuntu, this is done by typing
the following at the command line:

```
sudo apt-get install python3
```

You might also need to install the python3-tk package:

```
sudo apt-get install python3-tk
```

Note that you will most likely need to replace the `python` and `pip` commands
with `python3` and `pip3`.

### Installing livestreamer
Once Python is installed and in your path, you need to install [livestreamer](http://docs.livestreamer.io/). This is done by opening the
command line and typing:

```
pip install livestreamer
```

**Windows**: You can open the command line by pressing the Windows key
and the `R` key at the same time, typing `cmd` in the window that pops up and
clicking on the OK button or pressing enter.

## Installing Stream Downloader
In order to use Stream Downloader, just clone this repository or download it
and decompress it in a directory of your choice.

## Usage
To launch Stream Downloader, just open the file `main.py` with Python. You can
also run it on the command line by typing:

```
cd "path/to/the/stream/downloader/directory"
python main.py
```
