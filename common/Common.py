import uuid


class CommonUtils:
    @classmethod
    def getID(cls):
        ids = str(uuid.uuid4()).replace("-", "")
        ids = ids[0:16]
        return ids
