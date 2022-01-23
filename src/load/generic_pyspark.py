from load.base_load import AbstractLoad


class GenericPySparkLoad(AbstractLoad):
    """This is a generic class meant to easen the process of reading static files in spark such as
    CSV, JSON, Parquet etc
    """

    def __init__(self, path: str, **kwargs):
        super(GenericPySparkLoad, self).__init__(kwargs.pop("spark"))
        self.path = path
        self.options = kwargs

    def load(self):
        return self.spark.read.load(self.path, **self.options)
