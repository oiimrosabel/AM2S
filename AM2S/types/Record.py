class Record:
    def __set__(self, _, __):
        raise Exception("Read-only value")
