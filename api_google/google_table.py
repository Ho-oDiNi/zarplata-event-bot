from config.bot_config import GOOGLE_URL
import pygsheets

class GoogleTable:
    
    def __init__(
        self, credence_service_file:str = "config/google_config.json", googlesheet_file_url:str = GOOGLE_URL
    ) -> None:
        self.credence_service_file = credence_service_file
        self.googlesheet_file_url = googlesheet_file_url

    def _get_googlesheet_by_url(
        self, googlesheet_client: pygsheets.client.Client, sheet_name:str
    ) -> pygsheets.Spreadsheet:
        sheets: pygsheets.Spreadsheet = googlesheet_client.open_by_url(
            self.googlesheet_file_url
        )
        return sheets.worksheet_by_title(sheet_name)

    def _get_googlesheet_client(self):
        return pygsheets.authorize(
            service_file=self.credence_service_file
        )

#  - - - - - - - - - - - - - Вспомогательные функции - - - - - - - - - - - - - - - - #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Удобное форматирование ячейки
    def Cell(self, column:str, row):
        return column + str(row)

    # Количество админов
    def get_count_admins(self):
        googlesheet_client: pygsheets.client.Client = self._get_googlesheet_client()
        wks: pygsheets.Spreadsheet = self._get_googlesheet_by_url(googlesheet_client, "test")  

        cell = self.Cell("A", 2)
        count_admins = int(wks.get_value(cell))

        return count_admins  

    # Количество пользователей
    def get_count_users(self):
        googlesheet_client: pygsheets.client.Client = self._get_googlesheet_client()
        wks: pygsheets.Spreadsheet = self._get_googlesheet_by_url(googlesheet_client, "test")  

        cell = self.Cell("A", 3)
        count_users = int(wks.get_value(cell))

        return count_users

#  - - - - - - - - - -  Функции Inline клавиатур  - - - - - - - - - - - - - - - - - #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Запись нового пользователя в таблицу
    def login_agree(self, user_id, flat):
        googlesheet_client: pygsheets.client.Client = self._get_googlesheet_client()
        wks: pygsheets.Spreadsheet = self._get_googlesheet_by_url(googlesheet_client, "test") 

        row = self.get_k_users() + 2

        cell_user_id = wks.cell(f"F{row}")
        cell_user_id.set_value(user_id)

        cell_flat = wks.cell(f"G{row}")
        cell_flat.set_value(flat)

        return