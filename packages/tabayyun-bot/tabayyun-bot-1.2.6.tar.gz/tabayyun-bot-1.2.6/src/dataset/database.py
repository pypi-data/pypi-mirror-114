import logging

import pandas as pd
from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import SingletonThreadPool

# Global Variables
BASE = declarative_base()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MafindoNews(BASE):
    __tablename__ = "mafindo_tbl"
    id = Column(Integer, primary_key=True)
    authors = Column(Integer)
    status = Column(Integer)
    classification = Column(String(100))
    title = Column(Text)
    content = Column(Text)
    fact = Column(Text)
    reference_link = Column(Text)
    source_issue = Column(Text)
    source_link = Column(Text)
    picture1 = Column(String(500))
    picture2 = Column(String(100))
    tanggal = Column(String(12))
    tags = Column(String(500))
    conclusion = Column(Text)


class BotUser(BASE):
    __tablename__ = "bot_user"
    user_id = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    chat_timestamp = Column(String, primary_key=True)


class TabayyunDB:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html

    def __init__(self, sqlite_db):
        logging.debug("Set SQLite as the DB engine")
        self.db_engine = create_engine(f'sqlite:///{sqlite_db}', poolclass=SingletonThreadPool)
        self.connection = self.db_engine.connect()
        self.apply_schema()

    def apply_schema(self):
        logging.debug("Applying schemas..")
        BASE.metadata.create_all(self.db_engine)

    def execute_query(self, query=''):
        if query == '':
            return
        with self.connection as conn:
            try:
                conn.execute(query)
            except Exception as e:
                logging.error(e)

    def get_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        logging.debug(query)
        with self.connection as conn:
            try:
                result_df = pd.read_sql(query, conn)
            except Exception as e:
                logging.error(e)
        return result_df


if __name__ == "__main__":
    TabayyunDB('tabayyun.db').apply_schema()
