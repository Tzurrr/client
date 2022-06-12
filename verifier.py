import datetime
import os

def verify(first_half_arr: list, second_half_arr: list):
    for i in first_half_arr:
        for j in second_half_arr:
            if os.path.splitext(i[0])[0] == os.path.splitext(j[0])[0][:-1] + "a":
                first_file_creation_time = i[1]
                second_file_creation_time = j[1]
                distance = first_file_creation_time - second_file_creation_time
                minute_time = datetime.timedelta(0, 0, 0, 0, 1, 0, 0)
                if distance <= minute_time:
                    return True
        return False
