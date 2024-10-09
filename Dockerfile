FROM apache/airflow:2.6.3-python3.9

USER root

RUN apt-get update --allow-releaseinfo-change && \
    apt-get install -y gcc python3-dev openjdk-11-jdk git apt-transport-https ca-certificates curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

USER airflow

RUN pip install apache-airflow apache-airflow-providers-apache-spark pyspark