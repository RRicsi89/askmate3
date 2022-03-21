from datetime import datetime
import connections


def convert_timestamps(dictionaries):
    timestamps = []
    for dictionary in dictionaries:
        for key, value in dictionary.items():
            if key == "submission_time":
                timestamps.append(datetime.fromtimestamp(int(value)))
    return timestamps
