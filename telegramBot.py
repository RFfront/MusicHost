import json
from aiogram import Bot, Dispatcher, executor, types
import logging
from TGtoken import tgtok
import re

# Validate URL
url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
re.match(url_pattern, 'https://uibakery.io') # Returns Match object
re.match(url_pattern, 'https:/uibakery.io') # Returns None

# Extract URL from a string
url_extract_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
re.findall(url_extract_pattern, 'You can view more details at https://uibakery.io or just ping via email.') # returns ['https://uibakery.io']

logging.basicConfig(level=logging.INFO)
cb =[]
def coolBoysLoad():
    global cb
    with open('cb.json','r',encoding='utf-8') as f:
        cb = json.load(f)
        
def saveCoolBoy():
    global cb
    with open('cb.json','w',encoding='utf-8') as f:
        json.dump(cb,f)
    
# Initialize bot and dispatcher
bot = Bot(token=tgtok)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("need login")
    
@dp.message_handler(commands=['login'])
async def send_welcome(message: types.Message):
    global logine
    await message.reply('booba')

@dp.message_handler()
async def echo(message: types.Message):
    logging.info(message.from_id)
    logging.info(re.findall(url_extract_pattern,message.text))
    logging.info(message.text)
    
    await message.answer(message.text)
    
if __name__ == '__main__':
    coolBoysLoad()
    executor.start_polling(dp, skip_updates=True)