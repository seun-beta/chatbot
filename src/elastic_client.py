from elasticsearch import Elasticsearch

from src.config import (ELASTIC_SEARCH_HOST, ELASTIC_SEARCH_PASSWORD,
                        ELASTIC_SEARCH_USER)

elastic_search_client = Elasticsearch(
    hosts=[ELASTIC_SEARCH_HOST],
    basic_auth=[ELASTIC_SEARCH_USER, ELASTIC_SEARCH_PASSWORD],
    verify_certs=False,
)
