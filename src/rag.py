from openai import OpenAI

from search_service.query_index import retrieve_answer

openai_client = OpenAI()


few_shot_examples = """
Q: How do I check my account balance?
A: To check your account balance, log in to the FCMB mobile app, navigate to 'Account Summary,' and you will see your current balance displayed.

Q: How do I apply for a loan?
A: You can apply for a loan by logging into the FCMB mobile app or online banking portal, navigating to the 'Loans' section, and following the steps to apply.

Q: How do I transfer money between accounts?
A: To transfer money between your FCMB accounts, log in to the FCMB mobile app or online banking, navigate to the 'Transfers' section, and follow the prompts to initiate the transfer.
"""


def augment_with_gpt4(faq_context, user_query):

    prompt = f"""
You are an AI assistant for FCMB, a Nigerian bank. Your task is to provide clear and concise answers to customer queries based on the following FAQ data:

{few_shot_examples}

Additionally, here is some related FAQ data that may help you answer the user's question:
{faq_context}

Answer the following question based on the above information: {user_query}
"""

    # Call GPT-4 API to generate an augmented response
    response = openai_client.Completion.create(
        engine="gpt-4-0", prompt=prompt, max_tokens=300, temperature=0.2
    )

    return response.choices[0].text.strip()


def handle_fcmb_query(user_query):

    faq_context = retrieve_answer(user_query)

    final_response = augment_with_gpt4(faq_context, user_query)

    return final_response
