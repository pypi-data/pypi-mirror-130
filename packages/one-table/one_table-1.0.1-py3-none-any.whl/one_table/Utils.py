from datetime import datetime


def get_iso_8601_date():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
