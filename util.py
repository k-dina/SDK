from config import ENDPOINT_MAP
def datetime_to_sec(time):
    return time.day * 24 * 60 * 60 + time.hour * 60 * 60 + time.minute * 60 + time.second


def get_url(key):
    return ENDPOINT_MAP['base'] + ENDPOINT_MAP[key]
