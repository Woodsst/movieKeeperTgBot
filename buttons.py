from aiogram import Router, types, Bot, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from google_tabl_work import SheetWork
from id_check import AccessMiddleware
from movie import movie_valid, Movie
from enum import Enum
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class BotEvent(Enum):
    add_movie = 0
    add_movie_watched_mark = 1
    add_movie_block_mark = 2
    none = 3

def get_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Добавить фильм"),
                KeyboardButton(text="Не просмотренные")
            ],
            [
                KeyboardButton(text="Отметить - просмотрено"),
                KeyboardButton(text="Отметить - забраковано")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт меню"
    )

class ButtonsEvent:
    """Класс обработчик нажатия кнопок"""

    ADD_MOVIE_ANSWER: str = "Введите название фильма"
    GET_FILM_LIST_ANSWER: str = "Формирую список"

    def __init__(self, router: Router, sheet: SheetWork, bot: Bot, settings, kinopoisk):
        self.kinopoisk = kinopoisk
        self.settings = settings
        self.bot = bot
        self.router = router
        self.sheet = sheet
        self.status: BotEvent = BotEvent.none
        self.router.message.middleware(AccessMiddleware(self.settings.USERS))
        self.builder = InlineKeyboardBuilder()

        self.router.callback_query(F.data.startswith("film_"))(self.handle_add_watch_mark_callback)
        self.router.callback_query(F.data.startswith("blockfilm_"))(self.handle_add_block_mark_callback)
        self.router.message(lambda _: self.status != BotEvent.none)(self.user_message)
        self.router.message(lambda message: message.text == "Добавить фильм")(self.add_movie)
        self.router.message(lambda message: message.text == "Не просмотренные")(self.list_movies)
        self.router.message(lambda message: message.text == "Отметить - просмотрено")(self.add_watch_mark)
        self.router.message(lambda message: message.text == "Отметить - забраковано")(self.add_block_mark)

    async def user_message(self, message: types.Message):
        """Обработка запросов в зависимости от состояния определяемого нажатием кнопок"""
        match self.status:
            case BotEvent.add_movie:
                link = await self.kinopoisk.get_movie_link(message.text)
                movie = message.text
                if movie := movie_valid(movie, link):
                    self.sheet.add_movie(movie)
                    await self.send_message_about_add_movie(message, movie)
                self.status = BotEvent.none

    async def add_movie(self, message: types.Message):
        await message.answer(self.ADD_MOVIE_ANSWER)
        self.status = BotEvent.add_movie

    async def list_movies(self, message: types.Message):
        await message.answer(self.GET_FILM_LIST_ANSWER)
        films: list = self.sheet.get_not_watch_movie_list()
        if len(films) > 0:
            await message.answer("".join(films))
        self.status = BotEvent.none

    async def add_watch_mark(self, message: types.Message):
        await self.inline_button_create_for_get_watch_mark(message)

    async def add_block_mark(self, message: types.Message):
        await self.inline_button_create_for_block_movie(message)

    async def send_message_about_add_movie(self, message: types.Message, movie: Movie):
        for user in self.settings.USERS:
            if user != message.from_user.id:
                await self.bot.send_message(
                    chat_id=user,
                    text=f"Поступило предложение добавить в просмотр фильм {movie.name}, {movie.link}")

    def get_film_list(self):
        films = self.sheet.get_not_watch_movie_list()
        film_names = []
        i = 0
        while True:
            film: str = films[i].split(":")[1]
            film.strip()
            film_names.append(film)
            i += 4
            if i >= len(films):
                break
        return film_names

    async def inline_button_create_for_get_watch_mark(self, message: types.Message):
        self.builder = InlineKeyboardBuilder()

        for film in self.get_film_list():
            self.builder.button(text=film, callback_data=f"film_{film}")
        self.builder.adjust(1)

        await message.answer(
            "Выберите фильм",
            reply_markup=self.builder.as_markup()
        )

    async def inline_button_create_for_block_movie(self, message: types.Message):
        self.builder = InlineKeyboardBuilder()

        for film in self.get_film_list():
            self.builder.button(text=film, callback_data=f"blockfilm_{film}")
        self.builder.adjust(1)

        await message.answer(
            "Выберите фильм",
            reply_markup=self.builder.as_markup()
        )

    async def handle_add_watch_mark_callback(self, callback: types.CallbackQuery):
        film_name = callback.data.split("_")[1]
        self.sheet.put_watch_mark(film_name.strip())
        await callback.answer(f"Фильм {film_name.strip()} отмечен как просмотренный")

    async def handle_add_block_mark_callback(self, callback: types.CallbackQuery):
        film_name = callback.data.split("_")[1]
        self.sheet.put_block_mark(film_name.strip())
        await callback.answer(f"Фильм {film_name.strip()} отмечен как забракованный")
