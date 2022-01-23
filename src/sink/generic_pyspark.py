from sink.base_sink import AbstractSink


class GenericPySparkSink(AbstractSink):
    """This is a generic class meant to easen the process of sinking static files from spark such as
    CSV, JSON, Parquet etc
    """

    def __init__(self, path: str, **kwargs):
        super(GenericPySparkSink, self).__init__()
        self.path = path
        self.options = kwargs

    def sink(self, df):
        return df.write.save(self.path, **self.options)
