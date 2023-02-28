import uuid
from datetime import datetime


class CommonUtils:
    @classmethod
    def getID(cls):
        ids = str(uuid.uuid4()).replace("-", "")
        ids = ids[0:16]
        return ids

    @classmethod
    def getNow(cls):
        curr_time = datetime.now()
        s = curr_time.strftime("%Y-%m-%d %H:%M:%S")
        return s
