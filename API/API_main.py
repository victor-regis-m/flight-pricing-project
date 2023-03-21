from flask import Flask
from database_querier import get_flight_info
from script_creator import create_new_dag


app = Flask(__name__)


@app.route('/get_flight_info/', methods=['GET'])
def flight_querier():
    return get_flight_info()


@app.route('/create_new_monitoring/', methods=['POST'])
def script_creator():
    return create_new_dag()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)