import json
from datetime import datetime
from statuses_enum import Statuses
from validators import validator


class Chatbot:
    def __doc__(self):
        intro_str = "Chatbot." + \
                    "\n" + "method:" + \
                    "\n" + "use start method to get congratulate the user and get start" + \
                    "\n" + "use scan(document) method to send a document as response to requirement" \
                           "and get next requirement. " + \
                    "\n" + "in_progress prop is True if the dialogue continues."
        doc_str = "version 3.0"
        return intro_str + '\n' + doc_str

    def __init__(self, requirements, completed_requirements=[], conversation=None):
        """
            requirements - Array containing all the "id"s of the requirements
        """
        self._status = Statuses.chatting  # //chatbot status

        self._completed_requirements: [] = completed_requirements
        self._remaining_requirements: [] = requirements  # Array containing all the "id"s of the
        self._fail_attempt = 0  # the number of attempted to upload file

        if conversation:
            self._conversation = conversation
        else:
            self._conversation = f"conversation/" \
                                 f"{datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S-%f')}.txt"

    @property
    def in_progress(self):
        """:returns True when dialogue continues"""
        return self._status != Statuses.end

    @property
    def remaining_requirements(self):
        """:returns the current remaining requirements """
        return self._remaining_requirements

    @property
    def done_requirements(self):
        """:returns the current upload requirements """

    @property
    def upload_attempt(self):
        return self._fail_attempt

    def start(self):
        """
        :returns the start message
        """
        if not self._completed_requirements:
            messages = [GENERAL_RESPONSES['congratulate']]

            with open(self._conversation, 'x') as f:
                f.write(f'conversation start: {datetime.now()}\n\n')

        else:
            messages = [GENERAL_RESPONSES['welcome_back']]
            with open(self._conversation, 'a') as f:
                f.write('\n\n ************************ \n\n'
                        f'conversation re-start: {datetime.now()}\n\n')
        messages.append(self.get_next_requirement())
        return messages

    def get_next_requirement(self):
        """:returns next requirement"""

        # check if the conversation end
        if len(self._remaining_requirements) > 0:
            current_requirement = self._remaining_requirements[0]
            if current_requirement in INSTANCES:  # make sure that the current requirement is valid requirement
                retval = INSTANCES[current_requirement]['message']
            else:
                self._remaining_requirements.remove(current_requirement)
                retval = self.get_next_requirement()
            self._fail_attempt = 0
            self._status = Statuses.waiting
        else:
            self._status = Statuses.end
            retval = GENERAL_RESPONSES['all_done']
        return retval

    def next(self, response):
        """
        :param response: the file user upload as the desired requirement
        :returns response messages
        """

        if len(self._remaining_requirements) > 0:
            self._status = Statuses.chatting
            requirement = self._remaining_requirements[0]
            current = INSTANCES[requirement]
            error = self._is_valid(current, response)

            if error is None:
                self._fail_attempt = 0
                retval = [self._get_success_message(current)]

                self._completed_requirements.append(requirement)
                self._remaining_requirements.remove(requirement)
                retval.append(self.get_next_requirement())
                self.log_response(current, response)
            else:  # response is invalid

                if self._fail_attempt < MAX_ATTEMPT:  # response is invalid and there more attempts
                    self._fail_attempt += 1
                    retval = [self._get_fail_message(current, error)]
                else:  # response is invalid and there no any more attempts
                    self._status = Statuses.end
                    retval = [self._get_fail_message(current, error)]
        else:  # no more requirements
            retval = [self.get_next_requirement()]
        return retval

    def log_response(self, current, response):
        line = f"{current['name']}: {response}\n"
        with open(self._conversation, 'a') as file:
            file.write(line)

    @staticmethod
    def _is_valid(current, response):
        valid_result = None
        if current.get('validators'):
            for validator_id in current['validators']:
                valid_result = validator(validator_id, response)
                if valid_result:
                    break
        return valid_result

    @staticmethod
    def _get_success_message(current):
        message = current.get("success-messages")
        if not message:
            message = GENERAL_RESPONSES['success']
        return message

    def _get_fail_message(self, current, error):
        message = None
        error_messages = current.get("error-messages")
        if error_messages is not None:
            message = self._find_error(error_messages, error)
            if not message:
                message = self._find_error(error_messages, 'default')
        if not message:
            message = GENERAL_RESPONSES['failed']
        return message

    @staticmethod
    def _find_error(error_messages, error):
        for error_message in error_messages:
            if error_message["key"] == error:
                message = error_message["message"]
                return message
        return None


# static variables
pointer = open("chat_instances.json", 'r', encoding="utf-8")
json_data = json.load(pointer)
INSTANCES = json_data['instances']  # chat messages: all the options for "requirements" (as json)
GENERAL_RESPONSES = json_data['static']  # general responses: all the general  messages
MAX_ATTEMPT = 3  # the max number of attempted to upload file
pointer.close()


