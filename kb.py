from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = ReplyKeyboardMarkup(resize_keyboard=True)
create_name = 'Create personalised Dietary plan'
start_b1 = KeyboardButton(create_name)
start_b2 = KeyboardButton('Contact Us')
start_b3 = KeyboardButton('About Us')
start_my_name = 'My Dietary plan'
start_b4 = KeyboardButton(start_my_name)
start.add(start_b1).add(start_my_name).add(start_b2, start_b3)

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenuName = 'Main Menu'
mainMenub1 = KeyboardButton(mainMenuName)
mainMenu.add(mainMenub1)

dPreference = ReplyKeyboardMarkup(resize_keyboard=True)
dPreferenceb1 = 'vegan'
dPreferenceb2 = 'omnivore'
dPreferenceb3 = 'paleo'
dPreferenceb4 = 'keto'
dPreference.add(dPreferenceb1, dPreferenceb2).add(dPreferenceb3, dPreferenceb4).add(mainMenub1)

healthGoal = ReplyKeyboardMarkup(resize_keyboard=True)
healthGoalb1 = 'weight loss'
healthGoalb2 = 'muscle gain'
healthGoalb3 = 'maintenance'
healthGoal.add(healthGoalb1, healthGoalb2).add(healthGoalb3).add(mainMenub1)

allergies = ReplyKeyboardMarkup(resize_keyboard=True)
allergiesb1 = 'skip'
allergies.add(allergiesb1).add(mainMenub1)

def next_prev(current_page):
    ikb = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton('Day ' + str(current_page + 1), callback_data=current_page + 1)
    b2 = InlineKeyboardButton('Day ' + str(current_page - 1), callback_data=current_page - 1)
    if current_page == 1:
        return ikb.add(b1)
    elif current_page == 7:
        return ikb.add(b2)
    else:
        return ikb.insert(b2).insert(b1)
