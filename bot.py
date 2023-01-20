import config
import time
import logging 
from aiogram import Bot, Dispatcher, executor, types
import config2
from filtres import IsAdminFilter
from config2 import Database

db = Database('file.db')
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=["start","help"])
async def start(message:types.Message):
    await message.answer("Привет!")
    
    @dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
    async def cmd_ban(message: types.Message):
        if not message.reply_to_message:
                 await message.reply("Error")
        return
    await message.bot.delete_message(chat_id=config.GROUP_ID, user_id=message.message_id)
    await message.bot.kick_chat_memeber(chat_id=config.GROUP_ID, user_id=message.reply_to_message.user)
                
    await message.reply_to_message.reply("Welcome to the Ban =)")
    
@dp.message_handler(is_admin=True, commands=["mute"])
async def mute(message:types.Message):
    if str(message.from_user.id) == config.ADMIN_ID:
        if not message.reply_to_message:
            await message.reply("Error")
            return
        mute_min = int(message.text[5:]) 
        db.add_mute(message.reply_to_message.from_user.id, mute_min)
        await message.delete()
        await message.reply_to_message.reply("Good luck! mute {mute_min} minutes")
        
        if not db.examination(message.from_user.id):
            db.add(message.from_user.id)
            if not db.mute(message.from_user.id):
              print("/")
            else:
                await message.delete()
              
                

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


