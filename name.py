import ner


def names_original():
    return {"chatbot_name": "Alex",
            "user_name": "User"}

# Get string from name where it could include "my name is"
def getName(text: str) -> str:
    return ner.getNamedEntity("PERSON", text)

def nameResponse(names: list) -> str:
    from random import choice
    responses = [
        f"Great! Hi {names['user_name']}! How can I help?",
        f"Good! Hi {names['user_name']}, how can I help you?",
        f"Cool! Hello {names['user_name']}, what can I do for you?",
        f"OK! Hola {names['user_name']}, how can I help you?",
        f"OK! Hi {names['user_name']}, what can I do for you?",
        f"Hello {names['user_name']} - it is nice to meet you. What can I help you with?"]
    return choice(responses)

def get_user_name_response(name: str) -> str:
    from random import choice
    responses = [
        f"You are {name}! How can I help?",
        f"Your name is {name}, how can I help you?",
        f"They call you {name}, what can I do for you?",
        f"Your name is {name}, how can I help you?"
    ]
    return choice(responses)


def get_chatbot_name_response(name: str) -> str:
    from random import choice
    responses = [
        f"My name is {name}, how can I help?",
        f"You can call me {name}",
        f"You may call me {name}",
        f"Call me {name}"
    ]
    return choice(responses)