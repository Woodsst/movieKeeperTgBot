from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command

import buttons
import asyncio

from google_tabl_work import SheetWork
from settings import s
from kinopoisk_api import Kinopoisk

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    if message.from_user.id in s.USERS:
        await message.answer(
            "Привет! Я Бот хранитель кино! буду автоматически заливать фильмы которые вы запланировали посмотреть"
            "в гугл таблицу, из неё же буду читать запланированные вами фильмы и просмотренные",
            reply_markup=buttons.get_main_kb())


async def main() -> None:
    bot = Bot(token=s.TOKEN)
    ss = SheetWork()
    bott = buttons.ButtonsEvent(router=Router(), sheet=ss, bot=bot, settings=s, kinopoisk=Kinopoisk(s))
    dp.include_router(bott.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
