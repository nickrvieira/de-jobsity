from sink.base_sink import AbstractSink
from pyspark.sql import SparkSession


class JDBCSink(AbstractSink):
    def __init__(
        self, spark: SparkSession, conn_uri: str, database: str, table: str, **kwargs
    ):
        self.spark = spark

    def sink(
        self,
    ):
        pass
