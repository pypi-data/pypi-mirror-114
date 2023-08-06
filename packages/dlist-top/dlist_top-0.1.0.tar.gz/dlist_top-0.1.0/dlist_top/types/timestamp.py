from datetime import datetime

class Timestamp(datetime):
    @classmethod
    def parse(cls, unix):
        return datetime.utcfromtimestamp(unix / 1000)
