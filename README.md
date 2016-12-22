# m3truid
Android stores your playlists in a SQLite database located at `/data/data/com.android.providers.media/databases/external.db`
m3truid is a Python application that converts playlists stored in this database into standard *.m3u files.


1. Pull external.db
---

**If you have a rooted phone:**
- [Enable USB debugging mode](https://www.recovery-android.com/enable-usb-debugging-on-android.html) on your phone
- Install Android Debug Bridge on your PC (unofficial [minimal ADB](http://forum.xda-developers.com/showthread.php?t=2317790) or full official [Android SDK command line tools](https://developer.android.com/studio/index.html#downloads))
- Connect your Android phone to your PC
- Run from a command prompt:

```
adb root
adb pull /data/data/com.android.providers.media/databases/external.db
```

**If you don't have a rooted phone:**
- Adapt these steps with [this solution](http://stackoverflow.com/a/17177091/2227298).

2. Install dependencies
---

- Install [Python](https://www.python.org/downloads/) or [ActivePython](http://www.activestate.com/activepython/downloads) on your PC.
  - Choose to add Python to your PATH environment variable
- From a command prompt, run:

 ```
 pip install slugify
 ```
 
3. Download & Run
---

- Download [`m3truid.py`](https://github.com/kriswebdev/m3truid/releases/download/v0.1/m3truid.py)
- Run `python m3truid.py` or double-click on the `m3truid.py` file.
- Press ENTER to accept the suggested values.
- The M3U files contain relative paths to the media files. Store the M3U in the base folder that will be prompted.
- Only audio files are supported.

Enjoy!
