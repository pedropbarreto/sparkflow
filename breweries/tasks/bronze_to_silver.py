from pyspark.sql import functions as F
from breweries.utils.utils import Util
from pyspark.sql import SparkSession

def bronze_to_silver(input_path, output_path, **args):

    util = Util()
    print('printando input',input_path)
    df = util.load_parquet(input_path) 
    df.show()
    df.write.mode("overwrite").partitionBy('state_province').parquet(output_path)