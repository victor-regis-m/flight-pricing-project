from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

scraper_dag = DAG(
    "scraper_dag",
    start_date = datetime(2023, 3, 15, tz="UTC"),
    schedule_interval="00 08 * * *",
    catchup=False,
)

origin_airport = "GRU"
destination_airport = "BER"
departure_date = "2023-09-15"
command = f"~/flight-pricing-project/scraper-files/python3 main.py {origin_airport} {destination_airport} {departure_date}"

venv_activation = "source ~/env/bin/activate"

venv = BashOperator(
    task_id='activate_venv',
    bash_command=venv_activation,
    dag=scraper_dag
)

run_this = BashOperator(
    task_id='run_transport',
    bash_command=command,
    dag=scraper_dag
)

venv >> run_this

