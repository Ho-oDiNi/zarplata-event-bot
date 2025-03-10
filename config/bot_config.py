from dotenv import dotenv_values
import sqlite3

# Получение токена из файла .env
config = dotenv_values("./config/.env")
API_TOKEN = config["API_TOKEN"]
GOOGLE_URL = config["GOOGLE_URL"]
ADMIN = int(config["ADMIN"])
MANAGER = int(config["MANAGER"])

# Подключение к базе данных MySQL
DB = sqlite3.connect("utils/database.db")
DB.row_factory = sqlite3.Row

IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Plansza_pasowa.svg/1920px-Plansza_pasowa.svg.png"
