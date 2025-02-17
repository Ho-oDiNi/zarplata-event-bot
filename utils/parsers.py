def parse_callback_data(callback_data):
    callback_data = callback_data.partition("?")[2]

    callback_data = callback_data.partition("&id=")
    id = callback_data[2]

    callback_data = callback_data[0].partition("&field=")
    field = callback_data[2]

    callback_data = callback_data[0].partition("table=")
    table = callback_data[2]

    return table, field, id
