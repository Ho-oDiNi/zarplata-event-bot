from config.bot_config import DB, ADMIN


# Переделать под параматизированнные запросы
def db_get_table(table):
    cursor = DB.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    cursor.close()

    return data


# Переделать тк id растет
def db_set_user(tg_id):
    cursor = DB.cursor()
    query = f"""
        INSERT IGNORE INTO `users` (`tg_id`, `conference_id`) 
        VALUES ({tg_id}, {get_current_conference()['id']})
        ON DUPLICATE KEY UPDATE
        `conference_id` = {get_current_conference()['id']}
        """
    cursor.execute(query)
    DB.commit()
    cursor.close()


def get_array_id(data):
    array_id = []
    for row in data:
        array_id.append(row["id"])

    return array_id


def get_management_id():
    return ADMIN


def get_conference_speakers():
    cursor = DB.cursor(dictionary=True)
    cursor.execute(
        f"""
        SELECT `name`, `tg_id` 
        FROM `speakers` 
        WHERE `conference_id` = {get_current_conference()['id']}
        """
    )
    data = cursor.fetchall()
    cursor.close()

    return data


def get_current_conference():
    cursor = DB.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT * 
        FROM `conferences` 
        WHERE `is_current` = 1
        """
    )
    data = cursor.fetchone()
    cursor.close()

    return data
