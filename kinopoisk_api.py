from aiohttp import ClientSession

class Kinopoisk:
    """Работа с апи кинопоиска"""
    def __init__(self, settings):
        self.settings = settings
        self.url = settings.KINOPOISK_SEARCH_URL
        self.x_api_key = settings.KINOPOISK_X_API_KEY
        self.headers = {
            "X-API-KEY": self.x_api_key,
            "Content-Type": "application/json"
        }
        self.kinopoisk_movie_url = "https://www.kinopoisk.ru/film"

    async def get_movie_link(self, movie_name: str) -> str:
        async with ClientSession() as session:
            async with session.get(self.url + movie_name, headers=self.headers) as response:
                data = await response.json()
                movie_id = data.get("docs")[0].get("id")
                link = f"{self.kinopoisk_movie_url}/{movie_id}/"
        return link
