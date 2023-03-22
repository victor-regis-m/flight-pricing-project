from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

scraper_dag = DAG(
    "scraper_dag",
    start_date = pendulum.datetime(2023, 3, 15, tz="UTC"),
    schedule_interval="00 08 * * *",
    catchup=False,
)

origin_airport = "GRU"
destination_airport = "BER"
departure_date = "2023-09-15"
command = f"python3 /home/ubuntu/flight-pricing-project/scraper_files/main.py {origin_airport} {destination_airport} {departure_date}"

venv_activation = "source ~/env/bin/activate"

final_command = f"{venv_activation} && {command}"


task = BashOperator(
    task_id='full_task',
    bash_command=final_command,
    dag=scraper_dag
)

task
