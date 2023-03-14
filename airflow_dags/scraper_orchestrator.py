from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

scraper_dag = DAG(
    "scraper_dag",
    start_date = datetime(2023, 3, 4, tz="UTC"),
    schedule_interval="00 08 * * *",
    catchup=False,
)

origin_airport = "GRU"
destination_airport = "BER"
departure_date = "2023-09-15"
command = f"python3 main.py {origin_airport} {destination_airport} {departure_date}"
run_this = BashOperator(
    task_id='run_transport', bash_command=command, dag=scraper_dag)