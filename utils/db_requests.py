from config.bot_config import DB


def set_user(tg_id):
    cursor = DB.cursor()
    query = f"""
        INSERT OR REPLACE INTO users (tg_id, event_id, is_passed)
        VALUES({tg_id}, {get_current_event()['id']}, 0)
        """
    cursor.execute(query)
    DB.commit()
    cursor.close()


def get_event_speakers(event_id):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        SELECT *
        FROM `speakers` 
        WHERE `event_id` = {event_id}
        """
    )
    data = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in data] if data else None


def get_event_users(event_id):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        SELECT *
        FROM `users` 
        WHERE `event_id` = {event_id}
        """
    )
    data = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in data] if data else None


def get_current_event():
    cursor = DB.cursor()
    cursor.execute(
        """
        SELECT * 
        FROM events 
        WHERE date BETWEEN DATE('now', '-1 day') AND DATE('now', '+2 day')
        LIMIT 1
        """
    )
    data = cursor.fetchone()
    cursor.close()

    return dict(data) if data else None


def get_by_id(table, id):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        SELECT *
        FROM `{table}` 
        WHERE `id` = {id}
        """
    )
    data = cursor.fetchone()
    cursor.close()

    return dict(data) if data else None


def update_by_id(table, field, id, value):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        UPDATE `{table}`
        SET `{field}` = '{value}'
        WHERE `id` = {id}
        """
    )
    cursor.close()
    DB.commit()


def delete_by_id(table, id):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        DELETE FROM  `{table}`
        WHERE `id` = {id}
        """
    )
    cursor.close()
    DB.commit()


def copy_quiz_by_id(current_event_id, copyed_event_id):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        -- Шаг 1: Копируем quizes
        INSERT INTO `quizes` (`name`, `content`, `cell`, `img`, `event_id`)
        SELECT `name`, `content`, `cell`, `img`, {current_event_id}
        FROM `quizes`
        WHERE `event_id` = {copyed_event_id};
        """
    )
    cursor.close()
    DB.commit()

    cursor = DB.cursor()
    cursor.execute(
        f"""
        -- Шаг 2: Создаем временную таблицу для сопоставления quiz_id
        CREATE TEMP TABLE temp_quiz_mapping (
            old_quiz_id INTEGER,
            new_quiz_id INTEGER
        );
        """
    )
    cursor.close()
    DB.commit()

    cursor = DB.cursor()
    cursor.execute(
        f"""
        -- Шаг 3: Заполняем временную таблицу соответствий
        INSERT INTO temp_quiz_mapping (old_quiz_id, new_quiz_id)
        SELECT q1.id AS old_quiz_id, q2.id AS new_quiz_id
        FROM quizes q1
        JOIN quizes q2 ON q1.name = q2.name
        WHERE q1.event_id = {copyed_event_id} AND q2.event_id = {current_event_id};
        """
    )
    cursor.close()
    DB.commit()

    cursor = DB.cursor()
    cursor.execute(
        f"""
        -- Шаг 4: Копируем variants и привязываем их к новым quizes
        INSERT INTO `variants` (`name`, `quiz_id`, `cell`)
        SELECT v.name, tqm.new_quiz_id, v.cell
        FROM `variants` v
        JOIN temp_quiz_mapping tqm ON v.quiz_id = tqm.old_quiz_id;
    """
    )
    cursor.close()
    DB.commit()

    cursor = DB.cursor()
    cursor.execute(
        f"""
        -- Шаг 5: Удаляем временную таблицу
        DROP TABLE temp_quiz_mapping;
        """
    )
    DB.commit()
    cursor.close()


def insert_row(table, field, value):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        INSERT INTO {table} (`{field}`) VALUES ('{value}')
        """
    )
    id = cursor.lastrowid
    cursor.close()
    DB.commit()

    return id


def get_next_quiz(current_id=None):
    cursor = DB.cursor()
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

    return dict(data) if data else None


def get_event_quizes(id):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        SELECT *
        FROM `quizes` 
        WHERE `event_id` = {id}
        """
    )
    data = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in data] if data else None


def get_quiz_variants(id):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        SELECT *
        FROM `variants` 
        WHERE `quiz_id` = {id}
        """
    )
    data = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in data] if data else None


def get_speaker_questions(id):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        SELECT *
        FROM `questions` 
        WHERE `speaker_id` = {id}
        """
    )
    data = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in data] if data else None


def get_nearest_events():
    cursor = DB.cursor()
    cursor.execute(
        """
        SELECT * 
        FROM `events` 
        ORDER BY `date` ASC
        """
    )
    data = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in data] if data else None


def increment_variant(id):
    result = get_by_id("variants", id)["result"]
    update_by_id("variants", "result", id, result + 1)


# Обьединить в функции get_by_FK()
def get_by_tg_id(tg_id):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        SELECT *
        FROM `users` 
        WHERE `tg_id` = {tg_id}
        """
    )
    data = cursor.fetchone()
    cursor.close()

    return dict(data) if data else None


def set_user_passed(tg_id):
    update_by_id("users", "is_passed", get_by_tg_id(tg_id)["id"], 1)


def get_msg_id(tg_id):
    return get_by_tg_id(tg_id)["msg_id"]


def set_msg_id(tg_id, msg_id):
    update_by_id("users", "msg_id", get_by_tg_id(tg_id)["id"], msg_id)


def get_max_cell(table, FK_field, FK_value):
    cursor = DB.cursor()
    cursor.execute(
        f"""
        SELECT *
        FROM `{table}`
        WHERE `{FK_field}` = {FK_value}
        ORDER BY `cell` DESC
        LIMIT 1
        """
    )
    data = cursor.fetchone()
    cursor.close()

    return dict(data) if data else None


def create_question(content, cell, speaker_id):
    question_id = insert_row("questions", "content", content)
    update_by_id("questions", "cell", question_id, cell)
    update_by_id("questions", "speaker_id", question_id, speaker_id)
