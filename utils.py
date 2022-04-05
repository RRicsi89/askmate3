import datetime
import uuid
import time


def generate_uuid():
    uu_id = uuid.uuid4()
    return str(uu_id)


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

