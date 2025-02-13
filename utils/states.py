from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    question = State()
    speaker_id = State()


class Survey(StatesGroup):
    quizId = State()
