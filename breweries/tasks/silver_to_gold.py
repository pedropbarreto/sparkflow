from pyspark.sql import functions as F
from pyspark.sql import SparkSession

from breweries.utils.utils import Util

def silver_to_gold(input_path, output_path, **args):
    util = Util()

    print('printando input',input_path)
    df = util.load_parquet(input_path)

    df = (df
            .groupBy(['state_province', 'brewery_type'])
            .agg(F.count('id').alias('count_per_type_location'))
            .sort(['brewery_type', 'state_province'])
        )

    df.show()
    util.save(df, output_path)

