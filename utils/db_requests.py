from config.bot_config import DB


def get_table(table):
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


def get_by_id(table, id):
    cursor = DB.cursor(dictionary=True)
    cursor.execute(
        f"""
        SELECT *
        FROM `{table}` 
        WHERE `id` = {id}
        """
    )
    data = cursor.fetchone()
    cursor.close()

    return data


def update_by_id(table, field, id, value):
    cursor = DB.cursor(dictionary=True)
    cursor.execute(
        f"""
        UPDATE `{table}`
        SET `{field}` = '{value}'
        WHERE `id` = {id}
        """
    )
    cursor.close()
    DB.commit()

    return


def get_next_quiz(current_id=None):
    cursor = DB.cursor(dictionary=True)
    query = f"""
        SELECT *
        FROM `quizes` 
        WHERE `event_id` = {get_current_event()['id']} 
        """
    if current_id != None:
        query += f"AND `id` > {current_id} "

    query += f"LIMIT 1"

    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()

    return data


def get_quiz_variants(id):
    cursor = DB.cursor(dictionary=True)
    cursor.execute(
        f"""
        SELECT *
        FROM `variants` 
        WHERE `quiz_id` = {id}
        """
    )
    data = cursor.fetchall()
    cursor.close()

    return data


def increment_variant(id):
    result = get_by_id("variants", id)["result"]
    update_by_id("variants", "result", id, result + 1)


def get_current_variants():
    cursor = DB.cursor(dictionary=True)
    cursor.execute(
        f"""
        SELECT *
        FROM variants
        JOIN quizes ON variants.quiz_id = quizes.id
        WHERE quizes.event_id = {get_current_event()['id']}
        """
    )
    data = cursor.fetchall()
    cursor.close()

    return data
