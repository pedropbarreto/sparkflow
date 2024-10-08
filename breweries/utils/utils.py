from pyspark.sql import SparkSession

class Util:
    def __init__(self):
        self.spark = self.spark_init()  
    
    def spark_init(self):
        spark = SparkSession.builder\
            .master('local[*]')\
            .appName("Iniciando com Spark")\
            .getOrCreate()
        
        spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

        return spark

    def save(self, df, output_path):
        df.write.mode('overwrite').parquet(output_path)
        print(f'Saving on -> {output_path}')


    def load_parquet(self, input_path):
        df = self.spark.read.parquet(input_path)
        return df
