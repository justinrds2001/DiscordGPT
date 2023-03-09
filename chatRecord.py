from typing import Dict, List

RecordType = Dict[str, List[Dict[str, str]]]

class Record:
    __instance = None
    __record: RecordType = {}

    def __init__(self):
        if Record.__instance is not None:
            raise Exception("Cannot instantiate more than one Record")
        else:
            Record.__instance = self

    @staticmethod
    def get_instance():
        if Record.__instance is None:
            Record()
        return Record.__instance

    def delete_record(self, key):
        del self.__record[key]

    def add_message(self, channelId, message: str):
        self.__record.setdefault(channelId, []).append({"role": "user", "content": message})

    def get_record(self, channelId):
        return self.__record[channelId]
    