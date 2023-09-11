

def talk(text: str, names: dict) -> None:
    print(f'\n{names["chatbot_name"]}: {text}')

def listen(names: dict) -> str:
    print(f'\n{names["user_name"]}: ', end='')
    return input().lower()