CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    content TEXT,
    img TEXT,
    date DATETIME
);

-- Таблица questions
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    cell TEXT,
    speaker_id INTEGER,
    FOREIGN KEY (speaker_id) REFERENCES speakers(id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Таблица quizes
CREATE TABLE quizes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    content TEXT,
    cell TEXT,
    img TEXT,
    event_id INTEGER,
    FOREIGN KEY (event_id) REFERENCES events(id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Таблица speakers
CREATE TABLE speakers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    content TEXT,
    cell TEXT,
    img TEXT,
    event_id INTEGER,
    FOREIGN KEY (event_id) REFERENCES events(id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Таблица users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER NOT NULL UNIQUE,
    event_id INTEGER,
    is_passed INTEGER DEFAULT 0,
    msg_id INTEGER,
    FOREIGN KEY (event_id) REFERENCES events(id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Таблица variants
CREATE TABLE variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    quiz_id INTEGER,
    cell TEXT,
    result INTEGER DEFAULT 0,
    FOREIGN KEY (quiz_id) REFERENCES quizes(id) ON UPDATE CASCADE ON DELETE CASCADE
);