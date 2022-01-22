from abc import ABCMeta, abstractmethod


class AbstractLoad(metaclass=ABCMeta):
    @abstractmethod
    def load(
        self,
    ):
        ...
