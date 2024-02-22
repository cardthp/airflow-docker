"""
Downloads the csv file from the URL. Creates a new table in the Postgres server.
Reads the file as a dataframe and inserts each record to the Postgres table. 
"""
import psycopg2
import os
import traceback
import logging
import pandas as pd
import urllib.request

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')


postgres_host = os.environ.get('POSTGRES_HOST')
postgres_database = os.environ.get('POSTGRES_DB')
postgres_user = os.environ.get('POSTGRES_USER')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_port = os.environ.get('POSTGRES_PORT')
# dest_folder = os.environ.get('dest_folder')

# postgres_database = 'airflow'
# postgres_user = 'airflow'
# postgres_password = 'airflow'
# postgres_host = 'postgres'  # Name of the PostgreSQL service in the docker-compose.yaml
# postgres_port = 5432  # Default PostgreSQL port

# postgres_host = os.environ.get('postgres_host')
# postgres_database = os.environ.get('postgres_database')
# postgres_user = os.environ.get('postgres_user')
# postgres_password = os.environ.get('postgres_password')
# postgres_port = os.environ.get('postgres_port')
# dest_folder = os.environ.get('dest_folder')


try:
    conn = psycopg2.connect(
        host=postgres_host,
        database=postgres_database,
        user=postgres_user,
        password=postgres_password,
        port=postgres_port
    )
    cur = conn.cursor()
    logging.info('Postgres server connection is successful')
except Exception as e:
    traceback.print_exc()
    logging.error("Couldn't create the Postgres connection")


def create_postgres_table():
    """
    Create the Postgres table with a desired schema
    """
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS churn_modelling (RowNumber INTEGER PRIMARY KEY, CustomerId INTEGER, 
        Surname VARCHAR(50), CreditScore INTEGER, Geography VARCHAR(50), Gender VARCHAR(20), Age INTEGER, 
        Tenure INTEGER, Balance FLOAT, NumOfProducts INTEGER, HasCrCard INTEGER, IsActiveMember INTEGER, EstimatedSalary FLOAT, Exited INTEGER)""")
        
        logging.info(' New table churn_modelling created successfully to postgres server')
    except:
        logging.warning(' Check if the table churn_modelling exists')


def write_csv_to_postgres_main():
    # download_file_from_url(url, dest_folder)
    create_postgres_table()
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    # download_file_from_url(url, dest_folder)
    create_postgres_table()
    conn.commit()
    cur.close()
    conn.close()