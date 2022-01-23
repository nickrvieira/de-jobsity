from abc import ABCMeta, abstractmethod
from utils.logger import get_logger_instance

from sink.base_sink import AbstractSink
from load.base_load import AbstractLoad


class BasePipeline(metaclass=ABCMeta):
    def __init__(
        self, input: AbstractLoad, output: AbstractSink, cache_on_load: bool = True
    ) -> None:
        self.input = input
        self.output = output
        self.cache_on_load = cache_on_load
        self.logger = get_logger_instance()

    @abstractmethod
    def pipeline(self):
        ...

    def run(self):
        self.logger.info("Starting Pipeline %s", __name__)
        df = self.input.load()
        if self.cache_on_load:
            self.logger.info("Caching the dataframe")
            df = df.cache()
        for process in self.pipeline:
            self.logger.info(
                "Running method in %s - %s", self.__class__.__name__, process.__name__
            )
            df = process(df)

        self.logger.info("Finishing Pipeline %s - Starting sinking", __name__)

        self.logger.info("Dataframe with following schema: %s", df.dtypes)
        self.output.sink(df)
        self.logger.info("Sink with success")
