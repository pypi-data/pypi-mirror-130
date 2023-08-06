
"""
Tools for OS related stuff.
"""

import json
import os
import threading
import time
import sys
from .exceptions import *
from typing import Callable

if sys.platform == "win32":
    from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


def thread(target: Callable, *args):
    """
    Just another shortcut for starting threads.
    """

    return threading.Thread(target=target, args=args, daemon=True).start()


def loadJson(path: str):
    """
    Loads json from path

    Returns
    -------
    `tuple(data or exception, True or False)` :
        First item is the json data from the path if it succeeds, else it's an exception. Same thing goes for the second tuple.
    """

    try:
        with open(path) as f:
            return json.load(f), True
    except Exception as e:
        return e, False


def dumpJson(path: str, data: dict):
    """
    Dump data to json path.

    Returns
    -------
    `tuple(path or exception, True or False)` :
        First item in tuple is a path if dumping succeeds, else it's an exceptions. Same thing goes for the second tuple
    """

    try:
        with open(path, "w+") as f:
            json.dump(data, f, indent=4)
        return path, True
    except Exception as e:
        return e, False


def joinPath(path: str, cwd: str = os.getcwd()):
    """
    Helper function to make using os.path.join(os.gecwd()) a lot easier

    Ex: 
    joinPath(["modules", "modules.py"])
    joinPath("modules/modules.py")

    Returns: a string path
    """

    if type(path) != list:
        path = path.split("/")
    if cwd:
        path.insert(0, cwd)  # Adds the cwd at the very beginning of the list
    # The "*" basically unpacks the list into arguments/parameters the path.join function can accept
    return os.path.join(*path)


def setVolume(value: float, process: str = None, smooth: bool = True):
    """
    Allows you to set the volume of all processed. If proccess if provided it will change the volume only in that process or 
    if process startswith "!", then it will change the volume for all other processes except that.
    """

    if sys.platform != "win32":
        raise NotAvailable

    sessions = AudioUtilities.GetAllSessions()

    # For some reason 1.0 is not actually 100% but rather something like 90%
    if value == 1.0:
        value = 1.10

    def _smooth(volume):
        """
        Smooths the volume change.
        From what I can tell, this is not an efficient way of doing it, 
        but I'm going to stick to it for now.
        """

        current = volume.GetMasterVolume()

        while True:
            if value < current:
                current -= 0.05
                if current > value:
                    try:
                        volume.SetMasterVolume(current, None)
                    except:
                        pass
                    time.sleep(0.003)
                else:
                    break
            else:
                current += 0.05
                if current < value:
                    try:
                        volume.SetMasterVolume(current, None)
                    except:
                        pass
                    time.sleep(0.003)
                else:
                    break

    def _start(v):
        if smooth:
            thread(_smooth, v)
        else:
            v.SetMasterVolume(value, None)

    for ses in sessions:
        if ses.Process:

            volume = ses._ctl.QueryInterface(ISimpleAudioVolume)
            if not process:
                _start(volume)
            else:

                """
                If process is provided, it will either only change the volume on that process 
                or change the volume on all processes except that process.
                """

                if process.startswith("!"):
                    process_ = process[1:]
                    if ses.Process.name() != process_:
                        _start(volume)
                else:
                    if ses.Process.name() == process:
                        _start(volume)


def getVolume(process: str = None):
    """
    Return the highest volume. Check setVolume for parameters. (too lazy)
    """

    volumes = []
    sessions = AudioUtilities.GetAllSessions()

    for ses in sessions:

        if ses.Process:
            volume = ses._ctl.QueryInterface(ISimpleAudioVolume)
            volume = volume.GetMasterVolume()

            if not process:
                volumes.append(volume)
            else:
                if process.startswith("!"):
                    process_ = process[1:]
                    if ses.Process.name() != process_:
                        volumes.append(volume)
                else:
                    if ses.Process.name() == process:
                        volumes.append()

    if not volumes:
        return 1.0
    return max(volumes)
