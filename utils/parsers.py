from utils.db_requests import *


def step_letter(letter: str, index: int):
    return chr(ord(letter) + index)


def step_number(number: str, step: int):
    return str(int(number) + step)


def parse_callback_data(callback_data):
    callback_data = callback_data.partition("?")[2]

    callback_data = callback_data.partition("&id=")
    id = callback_data[2]

    callback_data = callback_data[0].partition("&field=")
    field = callback_data[2]

    callback_data = callback_data[0].partition("table=")
    table = callback_data[2]

    return table, field, id


def parse_button(start: int = 0, middle: int = 0, end: int = 0) -> int:
    sizes = []

    if start != 0:
        sizes.append(start)

    if middle % 2 != 0 and middle != 0:
        sizes.append(1)
        middle -= 1

    while middle > 0:
        sizes.append(2)
        middle -= 2

    if end != 0:
        sizes.append(end)

    return sizes


def parse_FK_field(table):
    if table in ["quizes", "speakers"]:
        return "event_id"
    if table == "variants":
        return "quiz_id"

    return None


def parse_next_cell(table, FK_field, FK_id):
    data = get_max_cell(
        table,
        FK_field,
        FK_id,
    )
    try:
        cell = data["cell"]
        if table == "quizes":
            return f"{step_letter(cell[:1], 2)}1"
        if table == "speakers":
            return f"{step_letter(cell[:1], 1)}1"
        if table == "variants":
            return f"{cell[:1]}{step_number(cell[1:], 1)}"
    except:
        if table == "quizes":
            return "A1"
        if table == "speakers":
            return "B1"
        if table == "variants":
            cell = get_by_id("quizes", FK_id)["cell"]
            return f"{step_letter(cell[:1], 1)}2"
