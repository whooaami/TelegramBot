import config
import logging

from aiogram import Bot, Dispatcher, executor, types

from filters import IsAdminFilter

# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# activate filter
dp.filters_factory.bind(IsAdminFilter)


# ban command (only for admins!)
@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("This command must be a response to the message!")
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply("User is banned!\nJustice is done.")


# remove new user joined message
@dp.message_handler(content_types=["new_chat_members"])
async def on_user_joined(message: types.Message):
    print('JOIN message removed')
    await message.delete()


# simple profanity check
@dp.message_handler()
async def filter_message(message: types.Message):
    if "Your text which `ll be deleted" in message.text:
        # profanity detected, remove
        await message.delete()


# run long-polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
