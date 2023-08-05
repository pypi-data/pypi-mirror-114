import logging
from functools import lru_cache
from warnings import simplefilter

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config.env import EnvConfig as Config
from src.dataset.database import TabayyunDB

logging.basicConfig(format=Config.LOG_FORMAT, level=Config.LOG_LEVEL)
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)


def get_dataset():
    conn = TabayyunDB(Config.BOT_DB)
    df = conn.get_data(table="mafindo_tbl")
    return df


@lru_cache()
def get_vectors(text1, text2):
    vectorizer = CountVectorizer(text1, text2)
    vectorizer.fit([text1, text2])
    return vectorizer.transform([text1, text2]).toarray()


@lru_cache()
def get_cosine_sim(text: str):
    ds = get_dataset()
    fact = "ARTIKEL TIDAK DITEMUKAN"
    link = []
    for _, row in ds.iterrows():
        vectors_content = get_vectors(text.lower(), row['content'].lower())
        if len(text.split()) > 2:
            similarity_content = cosine_similarity(vectors_content)
            vectors_tittle = get_vectors(text.lower(), row['title'].lower())
            similarity_tittle = cosine_similarity(vectors_tittle)
            if similarity_tittle[0][1] > 0.70 or similarity_content[0][1] > 0.70:
                return {"fact": row['fact'], "classification": row['classification'],
                        "conclusion": row['conclusion'], "references": [row['reference_link']]}

        if text.lower() in row['content'].lower():
            fact = "Ditemukan beberapa artikel terkait topik tersebut" \
                if len(set(link)) > 1 else "Ditemukan artikel terkait topik tersebut"
            link.append(f"{row['title']} - {row['reference_link']}")

    logging.info("get_cosine_sim.cache_info : %s", get_cosine_sim.cache_info())
    return {"fact": fact, "references": link}


if __name__ == '__main__':
    # Test sample message
    msg = """[SALAH] Racikan Air Kelapa Muda, Jeruk Nipis, Garam, dan Madu dapat Membunuh Virus Covid-19"""
    get_cosine_sim(msg)
