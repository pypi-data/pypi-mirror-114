""" Configuration """
import logging
import os


class EnvConfig:
    BOT_DB = os.environ.get('BOT_DATABASE')
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST')
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '0.0.0.0')
    WEBHOOK_PORT = os.environ.get('WEBHOOK_PORT', 8443)
    MAFINDO_API_KEY = os.environ.get('MAFINDO_API_KEY')
    LOG_LEVEL = os.environ.get('BOT_LOG_LEVEL', logging.INFO)
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
