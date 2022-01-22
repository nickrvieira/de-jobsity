import json

from argparse import ArgumentParser
from ast import literal_eval
from base64 import decode

from pyspark.sql import SparkSession
from utils.logger import get_logger_instance

from load.generic_pyspark import GenericPySparkLoad
from sink.jdbc_pyspark import JDBCSink
from pipeline.trips import TripsPipeline

logger = get_logger_instance()


def decode_b64(value):
    pass


logger.info("Starting Up Script")
# argument_parser = ArgumentParser()
# argument_parser.add_argument("--source-path", required=True)
# argument_parser.add_argument("--read-options", required=True, type=json.load)
# argument_parser.add_argument("--db-conn-uri", required=True)
# argument_parser.add_argument("--destination-database", required=True)
# argument_parser.add_argument("--destination-table", required=True)
# argument_parser.add_argument("--filtered-table-name", required=False)
# argument_parser.add_argument("--boundary-box", required=False, type=literal_eval)
# argument_parser.add_argument("--region-filter", required=False)

# args, _ = argument_parser.parse_known_args()


spark = SparkSession.builder.getOrCreate()

load = GenericPySparkLoad(
    spark=spark,
    path="/home/nick/repos/test-jobsity/source_data/trips.csv",
    **{"format": "csv", "header": "true"},
)

sink = JDBCSink(spark=spark, conn_uri="lala", database="blabla", table="lala")

df = TripsPipeline(load, sink).run()

df.show()
df.printSchema()
