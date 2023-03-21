import os
from flask import request, make_response
import re


def create_new_dag():
    payload = request.json
    keys = ["origin", "destination", "date"]
    if len(set(payload) - set(keys)) != 0:
        return "Error, payload content differs from expected"
    with open('dag_template.txt') as f:
        lines = f.readlines()
    current_number = get_last_dag_number() + 1
    lines = customize_template(lines, payload, current_number)
    write_file(lines, current_number)
    return "New Airflow routine successfully created"


def change_scraper_command(lines, payload):
    origin, destination, date = payload["origin"], payload["destination"], payload["date"]
    command_line = [i for i in lines if re.search("command", i)][0]
    index = lines.index(command_line)
    lines[index] = command_line.format(origin=origin, destination=destination, date=date)
    return lines


def get_last_dag_number():
    all_files = os.listdir(os.getcwd())
    dag_files = [i for i in all_files if re.search("dag(?!_template)", i)]
    dag_files.sort()
    try:
        number = int(dag_files[-1].split(".")[0][-1])
    except:
        number = 0
    return number


def change_dag_name(lines, number):
    dag_name_lines = [i for i in lines if re.search("scraper_dag", i)]
    dag_name_line = dag_name_lines[0]
    index = lines.index(dag_name_line)
    lines[index] = dag_name_line.format(number=number)
    return lines


def customize_template(lines, payload, number):
    lines = change_scraper_command(lines, payload)
    lines = change_dag_name(lines, number)
    return lines


def write_file(lines, number):
    f = open(f"dag_file{number}.py", "w")
    for line in lines:
        f.write(line)
    f.close()