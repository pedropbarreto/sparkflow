from pyspark.sql import functions as F
from breweries.utils.utils import Util
from pyspark.sql import SparkSession

def data_quality(input_path, output_path, **args):
    util = Util()

    print('printando input', input_path)
    df = util.load_parquet(input_path)

    (df
    .withColumn('missing_address', F.when(F.col('address_1').isNull(), True).otherwise(False))
    .withColumn('missing_phone', F.when(F.col('phone').isNull(), True).otherwise(False))
    .withColumn('missing_website_url', F.when(F.col('website_url').isNull(), True).otherwise(False))
    .sort(['missing_address', 'missing_website_url', 'missing_phone'],ascending=False)
    .select(['id', 'name','missing_address', 'missing_phone', 'missing_website_url'])
    .filter((F.col('missing_address')==True) | (F.col('missing_phone')==True) | (F.col('missing_website_url')==True))
    )

    util.save(df, output_path)