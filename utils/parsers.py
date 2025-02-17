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
    if table == "events":
        return None
