from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator

import requests
import os, sys
from datetime import datetime

sys.path.insert(1, "opt/airflow/dags/")

from breweries.tasks import extract
from breweries.tasks import bronze_to_silver
from breweries.tasks import silver_to_gold
from breweries.tasks import data_quality

default_args = {
    "owner": "data_eng_team",
    "retries": 2,
    "start_date": datetime(2022,1,1)
}

dag = DAG(
    dag_id= 'BREWERIES_PIPELINE',
    schedule_interval='0 4 * * *',
    catchup=False,
    default_args = default_args
)

start_dag = EmptyOperator(
    task_id='start_dag',
    dag=dag
)

extraction_task = PythonOperator(
    task_id='extraction_task',
    python_callable=extract.extraction_task,
    op_kwargs={
        "output_path": 'bronze/breweries'
    },
    dag=dag
)

bronze_to_silver = PythonOperator(
    task_id='bronze_to_silver',
    python_callable=bronze_to_silver.bronze_to_silver,
    op_kwargs={
        "input_path": 'bronze/breweries',
        "output_path": 'silver/breweries'
    },
    dag=dag
)

silver_to_gold = PythonOperator(
    task_id='silver_to_gold',
    python_callable=silver_to_gold.silver_to_gold,
    op_kwargs={
        "input_path": 'silver/breweries',
        "output_path": 'gold/breweries'
    },
    dag=dag
)

data_quality = PythonOperator(
    task_id='data_quality',
    python_callable=data_quality.data_quality,
    op_kwargs={
        "input_path": 'silver/breweries',
        "output_path": 'gold/data_quality',
    },
    dag=dag
)


start_dag >> extraction_task >> [bronze_to_silver, data_quality] >> silver_to_gold