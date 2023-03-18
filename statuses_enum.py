from enum import Enum


class Statuses(Enum):
    def __doc__(self):
        intro_str = "enum class of Chatbot Statuses."
    # options
    chatting = "chatting"
    waiting = "waiting"
    end = "end"