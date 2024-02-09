from datetime import datetime, timedelta

from airflow.decorators import dag, task

    # @task is decorator that used to define a task. Each decorated function represents a task that can be executed by Airflow.
default_args = {
    'owner': 'cardthp',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(dag_id='3_dag_api', 
     default_args=default_args, 
     start_date=datetime(2024, 1, 31), 
     schedule_interval='@daily')
def hello_world_etl():

    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Thanaphat',
            'last_name': 'Karoonwattana'
        }

    @task()
    def get_age():
        return 19

    @task()
    def greet(first_name, last_name, age):
        print(f"Hey! My name is {first_name} {last_name} "
              f"and I am {age} years old!")
    
    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], 
          last_name=name_dict['last_name'],
          age=age)

greet_dag = hello_world_etl()