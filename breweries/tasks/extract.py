from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType, IntegerType
from pyspark.sql import functions as F
import requests
from breweries.utils.utils import Util
from pyspark.sql import SparkSession



def extraction_task(output_path, **args):

    util = Util()
    url = "https://api.openbrewerydb.org/breweries"

    response = requests.get(url)

    breweries = response.json()

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

    df = util.spark.createDataFrame(breweries, schema=brewery_schema)
    df.show()
    util.save(df, output_path)



