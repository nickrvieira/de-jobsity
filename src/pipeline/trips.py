from load.base_load import AbstractLoad
from sink.base_sink import AbstractSink
from pyspark.sql.types import DoubleType
from utils.logger import get_logger_instance

from pyspark.sql.functions import col, count, regexp_extract, to_timestamp


class TripsPipeline:
    def __init__(
        self, input: AbstractLoad, sink: AbstractSink, cache_on_load: bool = True
    ) -> None:
        self.input = input
        self.sink = sink
        self.cache_on_load = cache_on_load
        self.pipeline = [
            self.parse_coordinate_points("origin_coord"),
            self.parse_coordinate_points("destination_coord"),
            self.format_datetime,
            self.group_duplicates,
        ]
        self.logger = get_logger_instance()

    def format_datetime(
        self, df, column_name="datetime", pattern="yyyy-MM-dd hh:mm:ss"
    ):
        return df.withColumn(column_name, to_timestamp(col(column_name), pattern))

    def group_duplicates(self, df, column_name="count"):
        grouped_cols = (
            "region",
            "origin_lat",
            "origin_lon",
            "destination_lat",
            "destination_lon",
            "datetime",
        )
        return df.groupBy(*grouped_cols).agg(count("datasource").alias(column_name))

    def parse_coordinate_points(self, column_name):
        point_regex = r"([-]?[0-9]*[.][0-9]*)\s([-]?[0-9]*[.][0-9]*)"
        name = column_name.split("_")[0]

        def parse_dataframe(df):
            df = df.withColumn(
                f"{name}_lat",
                regexp_extract(col(column_name), point_regex, 1).cast(DoubleType()),
            )
            df = df.withColumn(
                f"{name}_lon",
                regexp_extract(col(column_name), point_regex, 2).cast(DoubleType()),
            )
            df = df.drop(col(column_name))
            return df

        return parse_dataframe

    def run(self):
        df = self.input.load()
        if self.cache_on_load:
            self.logger.info("Caching the dataframe")
            df = df.cache()
        for process in self.pipeline:
            self.logger.info("Running method in %s - %s", self, process)
            df = process(df)

        return df
