from .singleton import SingletonMeta


class Storage(metaclass=SingletonMeta):

    def write_data_to_disk(self, table, data):
        pass

    def read_data_from_block(self, table, data):
        pass
