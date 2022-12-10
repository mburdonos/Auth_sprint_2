from abc import abstractmethod


class Storage:
    @abstractmethod
    def save_to_storage(self):
        pass

    @abstractmethod
    def get_all_raw(self, filters: dict):
        pass

    @abstractmethod
    def delete_raw(self, filters: dict):
        pass
