from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

storage = MemoryStorage()

class planState(StatesGroup):
    dietaryPreference = State()
    healthGoal = State()
    # numDays = State()
    allergies = State()
    budgetConstraint = State()