def classify_query(user_query):
    api_keywords = {
        "balance": "fetch_balance",
        "transactions": "fetch_transactions",
        "customer info": "fetch_customer_info",
    }

    for keyword, action in api_keywords.items():
        if keyword in user_query.lower():
            return action

    return "faq"


def extract_account_number(user_query):
    words = user_query.split()
    for word in words:
        if word.isdigit() and len(word) == 10:
            return word
    return None


def ask_for_account_number():
    return "I need your account number to proceed. Please provide your account number."
