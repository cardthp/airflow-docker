from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'cardthp',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='4_catchup',
    default_args=default_args,
    start_date=datetime(2024, 1, 31),
    schedule_interval='@daily',
    catchup=False # True : run missed DAG between the start_date and the current date / False : run only date that be operated
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo Hey'
    )