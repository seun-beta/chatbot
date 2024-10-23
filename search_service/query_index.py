import openai
from sentence_transformers import SentenceTransformer

from src.config import ELASTIC_SEARCH_INDEX_NAME, OPENAI_API_KEY
from src.elastic_client import elastic_search_client

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

# Sentence transformer for generating embeddings for queries
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_answer(user_question):
    # Generate embedding for the user's question
    user_embedding = model.encode(user_question).tolist()

    # Elasticsearch k-NN query to find the closest matches
    search_query = {
        "size": 3,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'question_embedding') + 1.0",
                    "params": {"query_vector": user_embedding},
                },
            }
        },
    }

    # Perform the search
    result = elastic_search_client.search(
        index=ELASTIC_SEARCH_INDEX_NAME, body=search_query
    )

    # Retrieve answers from the hits
    answers = [hit["_source"] for hit in result["hits"]["hits"]]

    context = "\n".join(
        [f"Q: {answer['question']}\nA: {answer['answer']}" for answer in answers]
    )
    return context
