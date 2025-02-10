from config.bot_config import DB


# Переделать под параматизированнные запросы
def get_table(table):
    cursor = DB.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    cursor.close()

    return data


# Переделать тк id растет
def set_user(tg_id):
    cursor = DB.cursor()
    query = f"""
        INSERT IGNORE INTO `users` (`tg_id`, `event_id`) 
        VALUES ({tg_id}, {get_current_event()['id']})
        ON DUPLICATE KEY UPDATE
        `event_id` = {get_current_event()['id']}
        """
    cursor.execute(query)
    DB.commit()
    cursor.close()


def get_event_speakers():
    cursor = DB.cursor(dictionary=True)
    cursor.execute(
        f"""
        SELECT *
        FROM `speakers` 
        WHERE `event_id` = {get_current_event()['id']}
        """
    )
    data = cursor.fetchall()
    cursor.close()

    return data


def get_current_event():
    cursor = DB.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT * 
        FROM `events` 
        WHERE `date` BETWEEN CURDATE() - INTERVAL 1 DAY AND CURDATE() + INTERVAL 2 DAY;
        """
    )
    data = cursor.fetchone()
    cursor.close()

    return data


def get_field_by_id(field, field_id):
    cursor = DB.cursor(dictionary=True)
    cursor.execute(
        f"""
        SELECT *
        FROM `{field}` 
        WHERE `id` = {field_id}
        """
    )
    data = cursor.fetchone()
    cursor.close()

    return data
