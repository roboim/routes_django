import asyncio
import logging
import os
import sys

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from answer_dict import answer_db
from dotenv import load_dotenv

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = str(os.getenv('BOT_TELEGRAM_TOKEN'))
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        # await message.send_copy(chat_id=message.chat.id)
        for key, value in answer_db.items():
            if key in message.text.lower():
                await message.answer(value)
                action = value.find('*ожидайте*')

                # Запрос маршрутов НЕ асинхронно
                response = requests.get(
                    'http://127.0.0.1:8000/api/v1/bearroutes/?bot=True',
                )
                answer_json = response.json()
                answer_message = ''
                for key_info, value_info in answer_json['info'].items():
                    answer_message += str(key_info) + ':' + str(value_info) + ' '
                await message.answer(answer_message)
                answer_message = ''
                for key_info, value_info in answer_json['top_routes'].items():
                    answer_message += str(value_info) + ' '
                await message.answer(answer_message)

    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        pass


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    print('Bot_started_bear_routes')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
