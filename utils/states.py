from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    question = State()
    speaker = State()
    confirm = State()
