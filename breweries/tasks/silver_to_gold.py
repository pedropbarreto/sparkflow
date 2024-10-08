from pyspark.sql import functions as F
from breweries.utils.utils import Util
from pyspark.sql import SparkSession

def silver_to_gold(input_path, output_path, **args):
    util = Util()

    print('printando input',input_path)
    df = util.load_parquet(input_path)
    # df = spark.read.parquet(input_path)

    df = df.groupBy(['state_province', 'brewery_type']).agg(F.count('id')).sort(['state_province', 'brewery_type'])

    df.show()
    util.save(df, output_path)
    # df.write.mode("overwrite").partitionBy('state_province').parquet(output_path)

