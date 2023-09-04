import datetime

def convert_to_datetime(timestamp_to_convert):
    timestamp = datetime.datetime.strptime(timestamp_to_convert, "%Y-%m-%dT%H:%M:%S.%fZ")
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S")