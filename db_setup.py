# import psycopg2
import sqlalchemy
from sqlalchemy import create_engine, inspect,text
from sqlalchemy.orm import sessionmaker
from database_model import Base, FlightInfo
import json

def configure():
    db_settings = json.load(open("db_config.json"))
    database_uri = f'postgresql+psycopg2://{db_settings["user"]}:{db_settings["password"]}@{db_settings["host"]}:{db_settings["port"]}/{db_settings["database"]}'
    engine = create_engine(database_uri, max_identifier_length=127, echo=True)
    table_name = FlightInfo.__tablename__
    try:
        info = inspect(engine)
    except:
        server_uri = f'postgresql+psycopg2://{db_settings["user"]}:{db_settings["password"]}@{db_settings["host"]}:{db_settings["port"]}'
        e = sqlalchemy.create_engine(server_uri, max_identifier_length=127)
        e.connect().execution_options(isolation_level="AUTOCOMMIT").execute(text(f'create database {db_settings["database"]};'))
        info = sqlalchemy.inspect(engine)
    # add create database case
    if not info.has_table(table_name):
        Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

    # else:
    #     con = psycopg2.connect(
    #         database=db_settings["database"],
    #         user=db_settings["user"],
    #         password=db_settings["password"],
    #         host=db_settings["host"],
    #         port=db_settings["port"]
    #     )
    #     return con
