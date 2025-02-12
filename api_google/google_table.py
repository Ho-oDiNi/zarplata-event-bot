import pygsheets
from config.bot_config import GOOGLE_URL
from utils.db_requests import *


class GoogleTable:

    def __init__(
        self,
        credence_service_file: str = "config/google_config.json",
        googlesheet_file_url: str = GOOGLE_URL,
    ) -> None:
        self.credence_service_file = credence_service_file
        self.googlesheet_file_url = googlesheet_file_url

    def _get_googlesheet_by_url(
        self, googlesheet_client: pygsheets.client.Client, sheet_name: str
    ) -> pygsheets.Spreadsheet:
        sheets: pygsheets.Spreadsheet = googlesheet_client.open_by_url(
            self.googlesheet_file_url
        )
        return sheets.worksheet_by_title(sheet_name)

    def _get_googlesheet_client(self):
        return pygsheets.authorize(service_file=self.credence_service_file)

    #  - - - - - - - - - - - - - Вспомогательные функции - - - - - - - - - - - - - - - - #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Удобное форматирование ячейки
    def fCell(self, column, row) -> str:
        return column + str(row)

    def getNextQuestionCell(self, speaker_id):
        cell = get_by_id("speakers", speaker_id)["question_cell"]
        next_cell = cell[:1] + str(int(cell[1:]) + 1)
        update_by_id("speakers", "question_cell", speaker_id, next_cell)

        return next_cell

    #  - - - - - - - - - -  Функции Inline клавиатур  - - - - - - - - - - - - - - - - - #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def setQuestion(self, speaker_id, question):
        next_cell = self.getNextQuestionCell(speaker_id)

        googlesheet_client: pygsheets.client.Client = self._get_googlesheet_client()
        wks: pygsheets.Spreadsheet = self._get_googlesheet_by_url(
            googlesheet_client, "Вопросы спикерам"
        )
        wks.cell(next_cell).set_value(question)
