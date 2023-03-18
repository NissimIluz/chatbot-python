# Chatbot

## How to update:
To update the bot messages, enter to chat 'instances. Jason' and executes the requested changes
## Setup & Installtion

Make sure you have the version of python

clone the repository
```bash
git clone <repo-url>
```

## Running The App
for running The App
After clone run, use:
```bash
main.py
```


## config

use the chatbot constructor to create new chatbot. pass to the constructor array of all messages ids.


you can edit the messages including message validator by edit ```src\chatbot\chat instances.json.```


for example: 
```
    "message_name": {
        "name": "message name",
        "message": "message ",
        "validators": [
            "validator1",
            "validators2",
            "validators3"
        ],
        /*  optional */
        "success_messages": "after success message",
        "error_messages": [
            {
                "key": "error key - validator name",
                "message": "error message"
            }
        ]
    }
```


validators: number, phone, he-text, email, max-length@number, min-length@number, israel-id, pattern@regular_expression


dont forget the pass the new message the to constructor after adding messages src\chatbot\chat instances.json.
