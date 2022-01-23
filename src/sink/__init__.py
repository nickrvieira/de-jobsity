from sink.jdbc import JDBCSink
from sink.generic_pyspark import GenericPySparkSink


sink_mapping = {"JDBCSink": JDBCSink, "GenericPySparkSink": GenericPySparkSink}
