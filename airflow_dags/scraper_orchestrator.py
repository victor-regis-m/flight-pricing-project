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
command = f"python3 main.py {origin_airport} {destination_airport} {departure_date}"

venv_activation = "source ~/env/bin/activate"

files_directory = "cd ~/flight-pricing-project/scraper_files/"

venv = BashOperator(
    task_id='activate_venv',
    bash_command=venv_activation,
    dag=scraper_dag
)

change_dir = BashOperator(
    task_id='change_dir',
    bash_command=files_directory,
    dag=scraper_dag
)


scraper = BashOperator(
    task_id='run_scraper',
    bash_command=command,
    dag=scraper_dag
)

venv.set_downstream(change_dir)
change_dir.set_downstream(scraper)

