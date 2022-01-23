from load.base_load import AbstractLoad
from utils.decode import decode_b64


class JDBCLoad(AbstractLoad):
    """This is a generic class meant to easen the process of reading static files in spark such as
    CSV, JSON, Parquet etc
    """

    def __init__(self, conn_uri, table=None, query=None, **kwargs):
        super(JDBCLoad, self).__init__(kwargs.pop("spark"))
        self.conn_uri = decode_b64(conn_uri)
        self.table = table
        self.query = query

        if table and query:
            raise ValueError("You should provide either a table or query, not both")

    def load(self):
        spark_read = self.spark.read.format("jdbc").option("url", self.conn_uri)

        if self.table:
            df = spark_read.option("dbtable", f"{self.table}").load()
        else:
            df = spark_read.option("query", self.query).load()

        return df
