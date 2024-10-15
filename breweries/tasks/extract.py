from pyspark.sql import functions as F
from pyspark.sql import SparkSession

import requests
import json
import os



def extraction_task(output_json, **args):

    url = "https://api.openbrewerydb.org/breweries"

    os.makedirs(os.path.dirname(output_json), exist_ok=True)

    response = requests.get(url)

    breweries = response.json()

    with open(output_json, 'w') as f:
        json.dump(breweries, f, indent=4)
