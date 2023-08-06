from abc import ABC, abstractmethod


class BaseWriter(ABC):
    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def write(self, report: dict) -> None:
        pass
