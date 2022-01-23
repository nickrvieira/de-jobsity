from pipeline.base_pipeline import BasePipeline
from load.jdbc import JDBCLoad
from dataclasses import dataclass
from pyspark.sql.functions import col, weekofyear, sum, avg
from pyspark.sql import DataFrame


@dataclass
class Coordinate:
    lat: float
    lon: float


class TripsAggregated(BasePipeline):
    """This pipeline calculates the average weekly travel of a filtered region/box

    It is important to notice that, since we do not have a left join there with a calendar table, I only calculate
    the average of those weeks that had at least one travel

    """

    def __init__(
        self,
        region=None,
        p1=None,
        p2=None,
        region_col="region",
        lat_cols=["origin_lat", "destination_lat"],
        lon_cols=["origin_lon", "destination_lon"],
        **kwargs
    ) -> None:
        super(TripsAggregated, self).__init__(**kwargs)
        self.region = region
        self.p1 = Coordinate(*p1) if p1 else None
        self.p2 = Coordinate(*p2) if p2 else None
        self.region_col = region_col
        self.lat_cols = lat_cols
        self.lon_cols = lon_cols

    @property
    def pipeline(self):
        return [self.filter_area, self.groupby_week, self.average_all_weeks]

    def filter_coordinates(self, df, col_name, coordinates):
        return df.filter(
            (col(col_name) < max(*coordinates)) & (col(col_name) > min(*coordinates))
        )

    def filter_area(self, df: DataFrame) -> DataFrame:

        if self.region:
            df = df.filter(col(self.region_col) == self.region)
        if self.p1 and self.p2:
            for lat_col in self.lat_cols:
                df = self.filter_coordinates(df, lat_col, [self.p1.lat, self.p2.lat])
            for lon_col in self.lon_cols:
                df = self.filter_coordinates(df, lon_col, [self.p1.lon, self.p2.lon])
        return df

    def groupby_week(self, df):
        return df.groupBy(weekofyear(("datetime"))).agg(
            sum("count").alias("total_trips_per_week")
        )

    def average_all_weeks(self, df):
        return df.agg(avg("total_trips_per_week").alias("weekly_avg_trips"))
