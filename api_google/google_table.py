import pygsheets

from pygsheets.datarange import DataRange
from config.bot_config import GOOGLE_URL
from utils.db_requests import *
from utils.parsers import *


class GoogleTable:
    def __init__(
        self,
        credence_service_file: str = "config/google_config.json",
        googlesheet_file_url: str = GOOGLE_URL,
    ) -> None:
        self.credence_service_file = credence_service_file
        self.googlesheet_file_url = googlesheet_file_url
        self.googlesheet_client: pygsheets.client.Client = (
            self._get_googlesheet_client()
        )
        self.wksSurvey: pygsheets.Spreadsheet = self._get_googlesheet_by_url(
            self.googlesheet_client, "Результаты опроса"
        )
        self.wksSpeakers: pygsheets.Spreadsheet = self._get_googlesheet_by_url(
            self.googlesheet_client, "Вопросы спикерам"
        )

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
        question = get_max_cell("questions", "speaker_id", speaker_id)

        if question is not None:
            cell = question["cell"]
            next_cell = f"{cell[:1]}{step_number(cell[1:], 1)}"
        else:
            speaker_cell = get_by_id("speakers", speaker_id)["cell"]
            next_cell = f"{speaker_cell[:1]}2"

        return next_cell

    #  - - - - - - - - - -  Функции Inline клавиатур  - - - - - - - - - - - - - - - - - #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def setQuestion(self, speaker_id, question):
        next_cell = self.getNextQuestionCell(speaker_id)
        create_question(question, next_cell, speaker_id)
        self.wksSpeakers.cell(next_cell).set_value(question)

    def updateSurvey(self, variant_id):
        variant = get_by_id("variants", variant_id)
        self.wksSurvey.cell(variant["cell"]).set_value(variant["result"])

    def changeSpeakerWks(self, event_id):
        self.wksSpeakers.clear(start="B1", end="H30")

        event_speakers = get_event_speakers(event_id)
        for speaker in event_speakers:
            self.wksSpeakers.cell(speaker["cell"]).set_value(speaker["name"])

            speaker_questions = get_speaker_questions(speaker["id"])
            for quiestion in speaker_questions:
                if quiestion:
                    self.wksSpeakers.cell(quiestion["cell"]).set_value(
                        quiestion["content"]
                    )

    def changeQuestionWks(self, event_id):
        self.wksSurvey.clear()

        event_quizes = get_event_quizes(event_id)
        for quiz in event_quizes:
            self.wksSurvey.cell(quiz["cell"]).set_value(quiz["name"])
            self.wksSurvey.cell(f"{step_letter(quiz["cell"][:1], 1)}1").set_value(
                "Результаты"
            )

            quiz_variants = get_quiz_variants(quiz["id"])
            for variant in quiz_variants:
                if variant:
                    self.wksSurvey.cell(
                        f"{step_letter(variant["cell"][:1], -1)}{variant["cell"][1:]}"
                    ).set_value(variant["name"])
                    self.wksSurvey.cell(variant["cell"]).set_value(variant["result"])

    def changeTable(self, event_id):
        self.changeSpeakerWks(event_id)
        self.changeQuestionWks(event_id)
