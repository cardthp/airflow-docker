import csv
import logging
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


default_args = {
    'owner': 'cardthp',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

    # ds_nodash as YYYYMMDD / ds as YYY-MM-DD
def postgres_to_s3(ds_nodash, next_ds_nodash):
    # step 1: query data from postgresql db and save into text file
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()  # connect with database
    cursor = conn.cursor()  # allows you to execute SQL queries and fetch results
    cursor.execute("select * from orders where date >= %s and date < %s",
                   (ds_nodash, next_ds_nodash))
    
        # NamedTemporaryFile is temporary text file 
    with NamedTemporaryFile(mode='w', suffix=f"{ds_nodash}") as f:
    # with open(f"dags/get_orders_{ds_nodash}.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()   # It ensures that all the data written to the temporary file / clean disk
        cursor.close()
        conn.close()
        logging.info("Saved orders data in text file: %s", f"dags/get_orders_{ds_nodash}.txt")

    # step 2: upload text file into S3
        s3_hook = S3Hook(aws_conn_id="minio_conn")
        s3_hook.load_file(
            filename=f.name,
            key=f"orders/{ds_nodash}.txt",
            bucket_name="airflow",
            replace=True
        )
        logging.info("Orders file %s has been pushed to S3!", f.name)


with DAG(
    dag_id="9_postgres_hooks",
    default_args=default_args,
    start_date=datetime(2024, 2, 7),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id="postgres_to_s3",
        python_callable=postgres_to_s3
    )
    task1


# PostgresHook : create table before
# create table if not exists public.orders (
#     order_id character varying,
#     date date,
#     product_name character varying,
#     quantity integer,
#     primary key (order_id)
# )

# inside cursor is  
# (...
#    ('order_id', None, None, None, None, None, None),
#  ('customer_name', None, None, None, None, None, None),
#  ('order_date', None, None, None, None, None, None),
#  ...)
