from src.config import ELASTIC_SEARCH_INDEX_NAME
from src.elastic_client import elastic_search_client


def delete_index():
    if elastic_search_client.indices.exists(index=ELASTIC_SEARCH_INDEX_NAME):
        elastic_search_client.indices.delete(index=ELASTIC_SEARCH_INDEX_NAME)
        print(f"Index '{ELASTIC_SEARCH_INDEX_NAME}' deleted successfully.")
    else:
        print(f"Index '{ELASTIC_SEARCH_INDEX_NAME}' does not exist.")


if __name__ == "__main__":
    delete_index()
