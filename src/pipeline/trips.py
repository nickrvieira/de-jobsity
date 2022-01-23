from pyspark.sql.types import DoubleType
from pyspark.sql.functions import col, count, regexp_extract, to_timestamp

from pipeline.base_pipeline import BasePipeline


class Trips(BasePipeline):
    def __init__(self, **kwargs) -> None:
        super(Trips, self).__init__(**kwargs)

    @property
    def pipeline(self):
        return [
            self.parse_coordinate_points("origin_coord"),
            self.parse_coordinate_points("destination_coord"),
            self.format_datetime,
            self.group_duplicates,
        ]

    def format_datetime(
        self, df, column_name="datetime", pattern="yyyy-MM-dd HH:mm:ss"
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
