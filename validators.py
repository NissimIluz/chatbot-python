import re
import string


def israel_id(o_id):
    if len(o_id) != 9:
        return False
    try:
        id_list = list(map(int, o_id))
    except:
        return False

    counter = 0
    for i in range(9):
        id_list[i] *= (i % 2) + 1
        if id_list[i] > 9:
            id_list[i] -= 9
        counter += id_list[i]

    if counter % 10 == 0:
        return True
    else:
        return False


validators = {
    "number": lambda value: re.match(RegularExpression.number, value),
    "phone": lambda value: re.match(RegularExpression.phone, value),
    "he-text": lambda value: re.match(RegularExpression.he, value),
    "email": lambda value: re.match(RegularExpression.email, value),
    "max-length": lambda value, max_length: len(value) <= int(max_length),
    "min-length": lambda value, min_length: len(value) >= int(min_length),
    "israel-id": israel_id,
    "pattern": lambda value, pattern: re.match(pattern, value)
}


class RegularExpression:
    phone = f'^' \
            f'[+][{string.digits}]{{10,15}}|' \
            f'[+][{string.digits}]{{3}}-[{string.digits}]{{10,15}}|' \
            f'[+][{string.digits}]{{3}}-[{string.digits}]{{2}}-[{string.digits}]{{5-10}}|' \
            f'[{string.digits}]{{10}}|' \
            f'[{string.digits}]{{3}}-[{string.digits}]{{7}}' \
            f'$'
    number = f'^[{string.digits}]*$'
    he = "^[א-ת .,?!0-9]{0,150}$"
    email = '(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'


def validator(validator_id, value):
    parm = validator_id.split('@')
    validator_name = parm[0]
    if validators[validator_name]:
        if len(parm[1:]):
            is_valid = validators[validator_name](value, *parm[1:])
        else:
            is_valid = validators[validator_name](value)
    else:
        is_valid = True
    if is_valid:
        return None
    else:
        return validator_name

