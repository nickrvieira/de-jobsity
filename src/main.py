import json

from argparse import ArgumentParser
from ast import literal_eval

from pyspark.sql import SparkSession
from utils.logger import get_logger_instance

from load import load_mapping
from sink import sink_mapping
from pipeline import pipeline_mapping

logger = get_logger_instance()


logger.info("Starting Up Script")
argument_parser = ArgumentParser()
argument_parser.add_argument("--load-config", required=True, type=json.loads)
argument_parser.add_argument("--sink-config", required=True, type=json.loads)
argument_parser.add_argument("--pipeline", required=True, type=json.loads)
args, _ = argument_parser.parse_known_args()


spark = SparkSession.builder.getOrCreate()

load = load_mapping[args.load_config["load_type"]](
    spark=spark,
    path=args.load_config["input_path"],
    **args.load_config["options"],
)


sink = sink_mapping[args.sink_config["sink_type"]](
    spark=spark, **args.sink_config["options"]
)
print(args.pipeline)

pipeline_name = args.pipeline["pipeline_name"]
logger.info(
    "Booting Pipeline Object %s - Load: %s - Out: %s", pipeline_name, load, sink
)
df = pipeline_mapping[pipeline_name](
    input=load, output=sink, **args.pipeline.get("options", {})
).run()


logger.info("Sucessful - Exiting")
