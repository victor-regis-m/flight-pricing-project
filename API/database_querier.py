from flask import  request, jsonify
from sqlalchemy import select
from scraper_files.database_model import FlightInfo
from scraper_files.db_setup import configure
from datetime import datetime, timedelta


def query_db(json_payload):
    session = configure()
    s = session()
    if "origin" not in json_payload:
        raise "Error, origin airport is not informed"
    statement = get_statement(json_payload)
    return s.execute(statement)


def get_statement(json_payload):
    origin, date, destination = "origin", "date", "destination"
    has_date, has_destination = date in json_payload, destination in json_payload
    if has_date:
        day = datetime.fromisoformat(f'{json_payload[date]}T00:00:00')
        next_day = day + timedelta(hours=24)
        if has_destination:
            statement = select(FlightInfo) \
                .where(FlightInfo.departure_airport == json_payload["origin"] and
                       day < FlightInfo.departure_datetime < next_day and
                       FlightInfo.arrival_airport == destination)
        else:
            statement = select(FlightInfo) \
                .where(FlightInfo.departure_airport == json_payload["origin"] and
                       day < FlightInfo.departure_datetime < next_day)
    else:
        if has_destination:
            statement = select(FlightInfo) \
                .where(FlightInfo.departure_airport == json_payload["origin"] and
                       FlightInfo.arrival_airport == destination)
        else:
            statement = select(FlightInfo) \
                .where(FlightInfo.departure_airport == json_payload["origin"])
    return statement


def from_db_to_json(db_result):
    res = {"results": ""}
    rows = []
    for r in db_result:
        rows.append(
            {
             "duration": r[0].duration,
             "price": r[0].price,
             "stops": r[0].stops,
             "operator": r[0].operator,
             "departure_airport": r[0].departure_airport,
             "arrival_airport": r[0].arrival_airport,
             "departure_datetime": r[0].departure_datetime,
             "arrival_datetime": r[0].arrival_datetime,
             "query_datetime": r[0].query_datetime
             }
        )
    res["results"] = rows
    return res


def get_flight_info():
    payload = request.json
    db_result = query_db(payload)
    json_output = from_db_to_json(db_result)
    return jsonify(json_output)






