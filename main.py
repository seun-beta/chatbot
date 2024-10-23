from fastapi import FastAPI
from pydantic import BaseModel

from src.api_logic import (
    fetch_balance_tool,
    fetch_customer_info_tool,
    fetch_transactions_tool,
)
from src.classify_query import (
    ask_for_account_number,
    classify_query,
    extract_account_number,
)
from src.rag import handle_fcmb_query

app = FastAPI()


@app.get("/")
async def healthcheck():
    return {"data": "PONG!"}


class Query(BaseModel):
    query: str


@app.post("/query")
def root(query: Query):
    response = handle_user_query(query.query)
    return {"data": response}


def handle_user_query(user_query):
    query_type = classify_query(user_query)

    account_number = extract_account_number(user_query)

    if query_type == "fetch_balance":
        if not account_number:
            return ask_for_account_number()
        balance_data = fetch_balance_tool.func(account_number)
        if "error" not in balance_data:
            return f"Your account balance is {balance_data['balance']}."
        else:
            return balance_data["error"]

    elif query_type == "fetch_transactions":
        if not account_number:
            return ask_for_account_number()
        transactions = fetch_transactions_tool.func(account_number)
        if "error" not in transactions:
            transaction_list = "\n".join(
                [f"Amount: {t['amount']}, Date: {t['timestamp']}" for t in transactions]
            )
            return f"Here are your recent transactions:\n{transaction_list}"
        else:
            return transactions["error"]

    elif query_type == "fetch_customer_info":
        if not account_number:
            return ask_for_account_number()
        customer_info = fetch_customer_info_tool.func(account_number)
        if "error" not in customer_info:
            return f"Customer Name: {customer_info['first_name']} {customer_info['last_name']}, Address: {customer_info['address']}"
        else:
            return customer_info["error"]

    else:
        return handle_fcmb_query(user_query)
