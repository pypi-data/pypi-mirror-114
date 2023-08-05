import logging

from src.config.env import EnvConfig as Conf
from src.dataclasses.model import BotUser
from src.dataclasses.model import Chat
from src.dataset.database import TabayyunDB
from src.service import crawler
from src.service.text_similarity import get_cosine_sim

logging.basicConfig(
    format=Conf.LOG_FORMAT, level=Conf.LOG_LEVEL
)


class Server:
    """ The API server """

    def handler(self, chat: Chat):
        """ Method for handing chats"""
        # get text similarity
        similarity = get_cosine_sim(chat.str_message)

        # process reply
        reply: str
        if similarity.get('conclusion'):
            fact = similarity['fact']
            classification = similarity['classification'].upper()
            conclusion = similarity['conclusion']
            references = "\n".join(similarity['references'])
            reply = f"Kategori : {classification} \n\nFakta : \n{fact} \n\nKesimpulan :\n{conclusion} \n\nArtikel terkait:\n{references}"
            if len(reply) > 4096:
                reply = f"Kategori : {classification} \n\nKesimpulan :\n{conclusion} \n\nArtikel terkait:\n{references}"

        elif similarity.get('references'):
            fact = similarity['fact']
            references = "\n".join(similarity['references'])
            reply = f"Konten : \n{chat.str_message} \n\nAnalisa :\n{fact} \n\nArtikel terkait:\n{references}"
        else:
            fact = "Tidak ditemukan artikel terkait konten tersebut"
            content = chat.str_message \
                if len(chat.str_message) < 1000 else f"{chat.str_message[:1000]}....(Sampai akhir)"
            reply = f"Konten : \n{content} \n\nAnalisa : \n{fact}"

        # log users
        user = BotUser(
            user_id=chat.sender_id,
            name=chat.sender
        )
        self.log_users(user)

        return reply

    @staticmethod
    def magic_keyword(keyword: str):
        magic_reply: str
        logging.info("Magic keyword : %s", keyword)
        if keyword == "!crawl":
            try:
                logging.info("Start adhoc crawling..")
                crawler.start()
                magic_reply = "Successfully crawled 10 articles"
                logging.debug("Clearing lru_cache..")
                get_cosine_sim.cache_clear()
            except Exception as ex:
                magic_reply = f"Error crawling message : {ex}"
        else:
            magic_reply = "No such magic!"
        return magic_reply

    @staticmethod
    def log_users(user: BotUser):
        """ method for storing users to db"""
        from datetime import datetime
        chat_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log: list = [user.user_id, user.name, chat_timestamp]
        try:
            logging.info("Storing user %s", log)
            conn = TabayyunDB(Conf.BOT_DB)
            conn.connection.execute('INSERT INTO bot_user VALUES (?,?,?)', log)
        except Exception as e:
            logging.error("Error when inserting bot user : %s", e)
