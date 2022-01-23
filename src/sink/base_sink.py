from abc import ABCMeta, abstractmethod


class AbstractSink(metaclass=ABCMeta):
    @abstractmethod
    def sink(self):
        ...
