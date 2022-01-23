from sink.base_sink import AbstractSink
from pyspark.sql import SparkSession
from utils.decode import decode_b64


class JDBCSink(AbstractSink):
    def __init__(self, spark: SparkSession, conn_uri: str, table: str, **kwargs):
        self.spark = spark
        self.conn_uri = decode_b64(conn_uri)
        self.table = table

    def create_database(self):
        pass

    def sink(self, df):
        df.write.mode("overwrite").format("jdbc").option("url", self.conn_uri).option(
            "dbtable", f"{self.table}"
        ).save()
