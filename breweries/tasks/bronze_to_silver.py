from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType, IntegerType
import json

from breweries.utils.utils import Util
from pyspark.sql import SparkSession

def bronze_to_silver(input_json, output_path, **args):

    util = Util()

    with open(input_json, 'r') as f:
        json_data = json.load(f)

    brewery_schema = StructType([
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("brewery_type", StringType(), True),
        StructField("address_1", StringType(), True),
        StructField("address_2", StringType(), True),
        StructField("address_3", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state_province", StringType(), True),
        StructField("postal_code", StringType(), True),
        StructField("country", StringType(), True),
        StructField("longitude", StringType(), True),
        StructField("latitude", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("website_url", StringType(), True),
        StructField("state", StringType(), True),
        StructField("street", StringType(), True)
    ])

    df = util.spark.createDataFrame(json_data, schema=brewery_schema)
    df.show()
    df.write.mode("overwrite").partitionBy('state_province').parquet(output_path)