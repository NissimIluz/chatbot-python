from chatbot import Chatbot


def print_messages(messages):
    for message in messages:
        print(message)


if __name__ == '__main__':
    chatbot = Chatbot(['first-name', 'last-name', 'phone', 'workplace', 'id', 'address', 'studies', 'hobbies', 'additional'])
    print_messages(chatbot.start())
    while chatbot.in_progress:
        response = input().strip()
        print_messages(chatbot.next(response))
