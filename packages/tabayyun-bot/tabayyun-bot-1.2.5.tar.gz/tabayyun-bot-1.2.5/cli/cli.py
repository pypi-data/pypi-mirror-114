"""" Command line interface for the bot"""
import logging
import os
import sys

import click
import colorama
from pyfiglet import figlet_format
from termcolor import colored

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_dir)

from src.config.env import EnvConfig as Conf

logging.basicConfig(
    format=Conf.LOG_FORMAT, level=Conf.LOG_LEVEL
)
colorama.init()


@click.command()
@click.option('--poll', is_flag=True, help='Start the bot with polling method')
@click.option('--crawl', is_flag=True, help='Start news crawling')
@click.option('--start', is_flag=True, help='Start the bot webhook')
@click.option('--update', is_flag=True, help='Update database')
def handle_commands(poll, crawl, start, update):
    """Main method for handling commands through CLI"""
    if not Conf.BOT_DB or not Conf.BOT_TOKEN:
        stdout("ERROR: please set BOT_DATABASE and BOT_TOKEN to start the bot! ", color="red")
        return
    bot_db = Conf.BOT_DB
    stdout("\nTabayyun Bot", color="blue", figlet_flag=True)
    if poll:
        stdout("Starting polling messages...", color="green")
        try:
            from src.view import telegram_bot
            telegram_bot.start_bot()
            stdout("Server completed", color="green")
        except Exception as exc:
            stdout("Starting server failed! : {}".format(exc), color="red")

    if crawl:
        crawling_page = int(input("Masukan jumlah artikel yang mau di download : "))
        try:
            from src.service import crawler
            from src.dataset.database import TabayyunDB
            stdout("Applying schema...", color="yellow")
            stdout(f"Using database {bot_db}", color="yellow")
            db_conn = TabayyunDB(sqlite_db=Conf.BOT_DB)
            db_conn.apply_schema()
            stdout("Start crawling...", color="yellow")
            crawler.start(crawling_page)
            stdout("Crawling completed!", color="green")
        except Exception as exc:
            stdout("Crawling failed! : {}".format(exc), color="red")

    if start:
        if not Conf.WEBHOOK_URL:
            stdout("ERROR: WEBHOOK_URL needs to be set for starting webhook server! ", color="red")
        if not Conf.WEBHOOK_HOST:
            stdout("WARNING: WEBHOOK_HOST is not set, set default value : 0.0.0.0", color="yellow")
        if not Conf.WEBHOOK_PORT:
            stdout("WARNING: WEBHOOK_PORT is not set, set default value : 8443", color="yellow")
        else:
            stdout(f"WEBHOOK_URL : {os.environ['WEBHOOK_URL']}", color="yellow")
        stdout("Starting Tabayyun webhook server...", color="green")
        from src.view import telegram_webhook
        telegram_webhook.start()
        try:
            from src.view import telegram_webhook
            telegram_webhook.start()
        except Exception as e:
            stdout("Starting server failed! : {}".format(e), color="red")


def stdout(string: str, color: str, font: str = "slant", figlet_flag: bool = False):
    """ A helper method to print logs to stdout """
    if not figlet_flag:
        logging.info(colored(string, color))
    else:
        logging.info(colored(figlet_format(string, font=font), color))


if __name__ == "__main__":
    handle_commands()
