from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    question = State()
    speaker_id = State()


class Survey(StatesGroup):
    quizId = State()


class Admin(StatesGroup):
    requestId = State()
    requestField = State()
    requestTable = State()

    massMailing = State()
    addPhoto = State()
    addDocument = State()

    createRow = State()
    changeRow = State()
    deleteRow = State()

    changeFileId = State()
    copyQuiz = State()
