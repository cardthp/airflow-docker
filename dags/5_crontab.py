from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'cardthp',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id="5_crontab",
    start_date=datetime(2024, 1, 31),
    schedule_interval='0 3 * * Tue-Fri'
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command="echo Hey dag with cron expression!"
    )
    task1