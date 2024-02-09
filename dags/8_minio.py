from datetime import datetime, timedelta

from airflow import DAG
    # old version is sensors.s3_key need to change to sensors.s3 because latest airfow no longer available
    # search from airflow doc : https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/sensors/s3/index.html
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor


default_args = {
    'owner': 'cardthp',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

    # sensor when you upload file to bucket result to log success
with DAG(
    dag_id='8_minio',
    start_date=datetime(2024, 2, 7),
    schedule_interval='@daily',
    default_args=default_args
) as dag:
    task1 = S3KeySensor(
        task_id='sensor_minio_s3',
        bucket_name='airflow',
        bucket_key='data.csv',
        aws_conn_id='minio_conn',
        mode='poke',    # poke mode is sensor
        poke_interval=5,
        timeout=30
    )