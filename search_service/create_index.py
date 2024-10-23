from src.config import ELASTIC_SEARCH_INDEX_NAME
from src.elastic_client import elastic_search_client

index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
    },
    "mappings": {
        "properties": {
            "question": {"type": "text"},
            "answer": {"type": "text"},
            "question_embedding": {"type": "dense_vector", "dims": 1536},  #
        }
    },
}



def create_index(): 
    if not elastic_search_client.indices.exists(index=ELASTIC_SEARCH_INDEX_NAME):
        elastic_search_client.indices.create(
            index=ELASTIC_SEARCH_INDEX_NAME, body=index_settings
        )
        print(f"Index '{ELASTIC_SEARCH_INDEX_NAME}' created successfully.")
    else:
        print(f"Index '{ELASTIC_SEARCH_INDEX_NAME}' already exists.")


if __name__ == "__main__":
    create_index()
