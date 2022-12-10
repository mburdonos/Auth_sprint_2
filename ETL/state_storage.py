import abc
import json
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as out_data:
            json.dump(state, out_data)

    @property
    def retrieve_state(self) -> dict:
        with open(self.file_path, 'r') as in_data:
            return json.load(in_data)


class StateFile:
    def __init__(self, storage: JsonFileStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        data = {key: value}
        self.storage.save_state(data)

    def get_state(self, key: str) -> Any:
        try:
            data = self.storage.retrieve_state
        except FileNotFoundError:
            return None
        return data.get(key)
