import logging
import os
from sqlite3 import IntegrityError

import pandas as pd
import requests
from sqlalchemy.exc import IntegrityError

from src.config.env import EnvConfig as Conf
from src.dataset.database import TabayyunDB

logging.basicConfig(
    format=Conf.LOG_FORMAT, level=Conf.LOG_LEVEL
)
result = []


def get_mafindo_data(api_key: str, limit: int) -> list:
    logging.info("Getting data from MAFINDO API..")
    mafindo_data = []
    url = 'https://yudistira.turnbackhoax.id/api/antihoax'
    data = {'key': api_key, 'limit': limit}
    try:
        req = requests.post(url, data=data)
        for response in req.json():
            mafindo_data.append(
                [response['id'],
                 response['authors'],
                 response['status'],
                 response['classification'],
                 response['title'],
                 response['content'],
                 response['fact'],
                 response['references'],
                 response['source_issue'],
                 response['source_link'],
                 response['picture1'],
                 response['picture2'],
                 response['tanggal'],
                 response['tags'],
                 response['conclusion']
                 ])
    except requests.RequestException as exp:
        logging.error(exp)
    return mafindo_data


def start(limit: int = 10):
    api_key = os.environ['MAFINDO_API_KEY']
    mafindo_data = get_mafindo_data(api_key, limit)

    engine = TabayyunDB(sqlite_db=Conf.BOT_DB).db_engine
    mafindo_df = pd.DataFrame(mafindo_data,
                              columns=['id', 'authors', 'status', 'classification', 'title', 'content', 'fact',
                                       'reference_link', 'source_issue', 'source_link', 'picture1', 'picture2',
                                       'tanggal',
                                       'tags', 'conclusion'])

    for i, _ in enumerate(mafindo_df.iterrows()):
        try:
            mafindo_df.iloc[[i]].to_sql('mafindo_tbl', con=engine, if_exists='append', index=False, chunksize=100)
        except IntegrityError:
            logging.warning("%s already exist, skip the row!", mafindo_df.iloc[i]['id'])
            continue


if __name__ == '__main__':
    start("tabayyun.db")
