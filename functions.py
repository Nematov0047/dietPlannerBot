import json

import aiohttp

import kb
async def checkMainMenu(message, state):
        if message.text == kb.mainMenuName:
            await message.reply(kb.mainMenuName, reply_markup=kb.start)
            await state.finish()
        else:
            return True
async def send_request(url, data):
    headers = {'Content-type':'application/json'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data, headers=headers) as response:
            return await response.text()
        #return await session.get(url, data=data, headers=headers)
