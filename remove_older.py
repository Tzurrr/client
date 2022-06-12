import datetime
import os

def remove(array: list):
    for i in array:
        if (datetime.datetime.utcnow() - i[1]) > datetime.timedelta(0, 0, 0, 0, 1, 0, 0):
            array.remove(i)
            try:
                os.remove(i[0])
            except Exception:
                pass
    return array
