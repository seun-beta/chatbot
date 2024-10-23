import json

from openai import OpenAI
from elasticsearch.helpers import bulk


from src.config import ELASTIC_SEARCH_INDEX_NAME, OPENAI_API_KEY
from src.elastic_client import elastic_search_client

client = OpenAI()


def load_data():
    with open("data/handbook.json") as handbook:
        return json.load(handbook)


def index_faqs():
    faq_data = load_data()

    actions = []
    for faq in faq_data:
        question_embedding = (
            client.embeddings.create(
                input=faq["question"], model="text-embedding-3-small"
            )
            .data[0]
            .embedding
        )

        action = {
            "_index": ELASTIC_SEARCH_INDEX_NAME,
            "_source": {
                "question": faq["question"],
                "answer": faq["answer"],
                "question_embedding": question_embedding,
            },
        }
        actions.append(action)

    # Bulk index into Elasticsearch
    bulk(elastic_search_client, actions)
    print(f"Indexed {len(actions)} FAQs successfully.")


if __name__ == "__main__":
    index_faqs()
