from config import token
from aiogram import Bot, Dispatcher, types, executor
import message as msg
import kb
from aiogram.dispatcher.filters import Text
import states
import asyncio
import json
import aiohttp
import functions
from db import db

bot = Bot(token)
dp = Dispatcher(bot, storage=states.storage)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(msg.welcome, reply_markup=kb.start)

@dp.message_handler(Text('About Us'))
async def about_us(message: types.Message):
    await message.reply(msg.about_us)

@dp.message_handler(Text('Contact Us'))
async def contact_us(message: types.Message):
    await message.reply(msg.contact_us)

@dp.message_handler(Text(kb.create_name))
async def create_personalized(message: types.Message):
    if db.check_if_already_exists(message.from_user.id) == False:
        await message.reply("What is your dietary preference?\n\nFor example: vegan, omnivore, paleo.", reply_markup=kb.dPreference)
        await states.planState.dietaryPreference.set()
    else:
        await message.reply("You already have a plan.\n\nPlease stick to it.")

@dp.message_handler(state=states.planState.dietaryPreference)
async def dPreference_state(message: types.Message, state: states.FSMContext):
    if await functions.checkMainMenu(message, state):
        await message.reply("What is your health goal?\n\nFor example: weight loss, muscle gain, maintenance.", reply_markup=kb.healthGoal)
        async with state.proxy() as data:
            data['dietaryPreference'] = message.text
        await states.planState.next()

@dp.message_handler(state=states.planState.healthGoal)
async def health_goal_state(message: types.Message, state: states.FSMContext):
    if await functions.checkMainMenu(message, state):
        await message.reply("Do you have any allergies?\n\nIf you have more than one allergy, then write your allergies seperated by space", reply_markup=kb.allergies)
        async with state.proxy() as data:
            data['healthGoal'] = message.text
        await states.planState.next()

@dp.message_handler(state=states.planState.allergies)
async def allergies_state(message: types.Message, state: states.FSMContext):
    if await functions.checkMainMenu(message, state):
        await message.reply("Budget constraint for the diet plan. It can be an optional numeric value? (in $)", reply_markup=kb.mainMenu)
        async with state.proxy() as data:
            if message.text == 'skip':
                data['allergies'] = []
            else:
                data['allergies'] = message.text.split(' ')
        await states.planState.next()

@dp.message_handler(state=states.planState.budgetConstraint)
async def budget_constraint_state(message: types.Message, state: states.FSMContext):
    if await functions.checkMainMenu(message, state):
        waiting = await message.reply("Generating personalised healthy diet plan...")
        await message.answer_chat_action('typing')
        async with state.proxy() as data:
            data['budgetConstraint'] = message.text
            await state.finish()
            data['numDays'] = 7
            data['user'] = 'John Doe'
            dataJson = json.dumps(dict(data))
            r = await functions.send_request('http://217.18.63.178:3000/getOverview', dataJson)
            r = json.loads(r)
            await message.reply(r['overview'], reply_markup=kb.start)
            await waiting.delete()
            data_for_db = (message.from_user.id, data['dietaryPreference'], data['healthGoal'], data['numDays'], str(data['allergies']), data['budgetConstraint'])
            db.insert_to_diets(data_for_db)
            await message.answer(msg.get_more_info, parse_mode='HTML')
        await state.finish()

@dp.message_handler(Text(kb.start_my_name))
async def diet_plan(message: types.Message):
    if db.check_if_already_exists(message.from_user.id):
        dayNum = 1
        try:
            readyData = db.get_diets_plan_by_day(dayNum=dayNum, user_id=message.from_user.id)
        except:
            readyData = False
        if readyData:
            await message.reply(readyData[1], parse_mode='HTML', reply_markup=kb.next_prev(dayNum))
        else:
            try:
                waiting = await message.reply("Please wait...\n\nGenerating your healthy diet plan Day 1")
                await message.answer_chat_action('Typing')
                dataJson = db.get_data_by_userid(message.from_user.id)
                r = await functions.send_request('http://217.18.63.178:3000/getDay/' + str(dayNum), dataJson)
                r = json.loads(r)
                answer_from_gpt = ''
                for answer in r['diet']:
                    if answer['time']:
                        answer_from_gpt += "<b>" + answer['time'] + '</b>\n'
                    if answer['food']:
                        for food in answer['food']:
                            answer_from_gpt += '- ' + food + '\n'
                db.insert_diets_plan(data=(message.from_user.id, answer_from_gpt,dayNum ))
                await message.reply(answer_from_gpt, parse_mode='HTML', reply_markup=kb.next_prev(dayNum))
                await waiting.delete()
            except:
                await message.reply(msg.error)
    else:
        await message.reply("You have not created personal plan, yet!")




@dp.message_handler(Text(kb.mainMenuName))
async def main_menu(message: types.Message, state: states.FSMContext):
    await message.reply(kb.mainMenuName, reply_markup=kb.start)
    await state.finish()


@dp.callback_query_handler()
async def callback_handler_of_bot(callback: types.CallbackQuery):
    dayNum = int(callback.data)
    print(dayNum)
    if db.check_if_already_exists(callback.from_user.id):
        try:
            readyData = db.get_diets_plan_by_day(dayNum=dayNum, user_id=callback.from_user.id)
        except:
            readyData = False
        if readyData:
            await callback.message.edit_text(text=readyData[1], parse_mode='HTML', reply_markup=kb.next_prev(dayNum))
        else:
            try:
                waiting = await callback.answer("Please wait... \nGenerating your healthy diet plan")
                waiting2 = await bot.send_message(text="Please wait... \nGenerating your healthy diet plan", chat_id=callback.from_user.id)
                await callback.message.answer_chat_action('Typing')
                dataJson = db.get_data_by_userid(callback.from_user.id)
                r = await functions.send_request('http://217.18.63.178:3000/getDay/' + str(dayNum), dataJson)
                r = json.loads(r)
                answer_from_gpt = ''
                for answer in r['diet']:
                    if answer['time']:
                        answer_from_gpt += "<b>" + answer['time'] + '</b>\n'
                    if answer['food']:
                        for food in answer['food']:
                            answer_from_gpt += '- ' + food + '\n'
                db.insert_diets_plan(data=(callback.from_user.id, answer_from_gpt,dayNum ))
                await callback.message.edit_text(text=answer_from_gpt, parse_mode='HTML', reply_markup=kb.next_prev(dayNum))
                await waiting2.delete()
            except:
                try:
                    await callback.message.answer(msg.error)
                except:
                    await callback.answer(msg.error)




@dp.message_handler()
async def whatever(message: types.Message):
    await message.reply(msg.error + '\n\nPls, start the bot again by using /start command.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)