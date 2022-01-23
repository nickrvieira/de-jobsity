from abc import ABCMeta, abstractmethod
from pyspark.sql import SparkSession


class AbstractLoad(metaclass=ABCMeta):
    def __init__(self, spark: SparkSession):
        self.spark = spark

    @abstractmethod
    def load(
        self,
    ):
        ...
