from load.base_load import AbstractLoad
from pyspark.sql import SparkSession


class GenericPySparkLoad(AbstractLoad):
    """This is a generic class meant to easen the process of reading static files in spark such as
    CSV, JSON, Parquet etc
    """

    def __init__(self, spark: SparkSession, path: str, **kwargs):
        self.spark = spark
        self.path = path
        self.options = kwargs

    def load(self):
        return self.spark.read.load(self.path, **self.options)
