from load.generic_pyspark import GenericPySparkLoad
from load.jdbc import JDBCLoad

load_mapping = {"GenericPySparkLoad": GenericPySparkLoad, "JDBCLoad": JDBCLoad}
