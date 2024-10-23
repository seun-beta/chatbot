import httpx
from langchain.tools import Tool


def fetch_account_balance(account_number):
    response = httpx.get(
        f"http://127.0.0.1:8000/api/accounts/by-account-number/{account_number}/"
    )
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch account balance."}


# Tool to fetch recent transactions
def fetch_recent_transactions(account_number):
    response = httpx.get(
        f"http://127.0.0.1:8000/api/transactions/by-account-number/{account_number}/"
    )
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch transactions."}


def fetch_customer_info(account_number):
    response = httpx.get(f"http://127.0.0.1:8000/api/customers/{account_number}/")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch customer information."}


fetch_balance_tool = Tool(
    name="fetch_account_balance",
    func=lambda account_number: fetch_account_balance(account_number),
    description="Fetches the account balance for the given account number.",
)

fetch_transactions_tool = Tool(
    name="fetch_recent_transactions",
    func=lambda account_number: fetch_recent_transactions(account_number),
    description="Fetches recent transactions for the given account number.",
)

fetch_customer_info_tool = Tool(
    name="fetch_customer_info",
    func=lambda account_number: fetch_customer_info(account_number),
    description="Fetches customer information for the given account number.",
)
