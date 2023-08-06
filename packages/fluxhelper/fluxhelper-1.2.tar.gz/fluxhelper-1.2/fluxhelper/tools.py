
"""
Main/General category
"""

import importlib
import random
import string
import sys
import datetime


class ObjDebug(object):

    """
    Apply this to a class and you will be able to edit the methods of that class and have it update in real time.

    Source: https://stackoverflow.com/a/15839513/12590728
    """

    def __getattribute__(self, k):
        ga = object.__getattribute__
        sa = object.__setattr__
        cls = ga(self, "__class__")
        modname = cls.__module__
        mod = __import__(modname)
        del sys.modules[modname]
        importlib.reload(mod)
        sa(self, "__class__", getattr(mod, cls.__name__))
        return ga(self, k)


class DatetimeTools:

    def formatShort(dt):
        return dt.strftime("%b %d %Y at %I:%M %p")

    def formatLong(dt):
        return dt.strftime("%B %d %Y at %I:%M %p")
    
    def inXSeconds(dt: datetime.timedelta):
        return dt.total_seconds()
    
    def inXMinutes(dt: datetime.timedelta):
        return dt.total_seconds() / 60
    
    def inXHours(dt: datetime.timedelta):
        return dt.total_seconds() / 3600
    
    def inXDays(dt: datetime.timedelta):
        return dt.total_seconds() / 86400
    
    def inXWeeks(dt: datetime.timedelta):
        return dt.total_seconds() / 604800
    
    def inXMonths(dt: datetime.timedelta):
        return dt.total_seconds() / 2592000
    
    def inXYears(dt: datetime.timedelta):
        return dt.total_seconds() / 31536000
    
    def autoInX(dt: datetime.timedelta):
        totalSeconds = dt.total_seconds()

        if totalSeconds < 60:
            return f"{DatetimeTools.inXSeconds(dt)} second(s)"
        elif totalSeconds < 3600:
            minutes = DatetimeTools.inXMinutes(dt)

            # Get remaining seconds
            seconds = int(round(totalSeconds % 60))
            if seconds == 0:
                return f"{int(minutes)} minute(s)"

            return f"{int(minutes)} minute(s) and {int(seconds)} second(s)"
        elif totalSeconds < 86400:
            hours = DatetimeTools.inXHours(dt)

            # Get remaining minutes
            minutes = int(round(totalSeconds % 3600 / 60))
            if minutes == 0:
                return f"{int(hours)} hour(s)"

            return f"{int(hours)} hour(s) and {int(minutes)} minute(s)"
        elif totalSeconds < 604800:
            days = DatetimeTools.inXDays(dt)

            # Get remaining hours
            hours = int(round(totalSeconds % 86400 / 3600))
            if hours == 0:
                return f"{int(days)} day(s)"

            return f"{int(days)} day(s) and {int(hours)} hour(s)"
        elif totalSeconds < 2592000:
            weeks = DatetimeTools.inXWeeks(dt)

            # Get remaining days
            days = int(round(totalSeconds % 604800 / 86400))
            if days == 0:
                return f"{int(weeks)} week(s)"

            return f"{int(weeks)} week(s) and {int(days)} day(s)"
        elif totalSeconds < 31536000:
            months = DatetimeTools.inXMonths(dt)

            # Get remaining weeks
            weeks = int(round(totalSeconds % 2592000 / 604800))
            if weeks == 0:
                return f"{int(months)} month(s)"

            return f"{int(months)} month(s) and {int(weeks)} week(s)"
        else:
            years = DatetimeTools.inXYears(dt)

            # Get remaining months
            months = int(round(totalSeconds % 31536000 / 2592000))
            if months == 0:
                return f"{int(years)} year(s)"

            return f"{int(years)} year(s) and {int(months)} month(s)"


def convertRange(val: float, old: tuple, new: tuple):
    """
    Converts the range of a value to a new range.

    Example
    -------
    convertRange(50, (0, 100), (0, 1))
    >> 0.5
    """

    return (((val - old[0]) * (new[1] - new[0])) / (old[1] - old[0])) + new[0]


def timeRound(t: int, r: int = 3):
    """
    Well, it's so self explanatory. (There's a reason why I did this)
    """

    return round(t, r)


def generateId(n: int, dictionary: str = None):
    """
    Generate an Id

    Parameters
    ----------
    `n` : int
        How long the id is. (Length of characters)
    `dictionary` : str
        Where to look for characters.
    """

    if not dictionary:
        dictionary = string.ascii_letters + string.digits

    return "".join(random.choices(dictionary, k=n))
