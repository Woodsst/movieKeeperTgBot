from typing import List

from google.oauth2.service_account import Credentials
import gspread

from movie import Movie

class SheetWork:

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SERVICE_ACCOUNT_FILE = "movies-462907-3905ade8cbd4.json"
    SPREADSHEET_ID = "1b_IzPr74VufP3nEASYKin1hMG1lkZbFI1ZRQvEj2Xdo"

    def __init__(self) -> None:

        self.creds = Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open_by_key(self.SPREADSHEET_ID).sheet1

    def add_movie(self, movie: Movie) -> None:
        """Ожидается Лист с данынми фильма формата:
        Фильм: str,
        Дата добавления:datatime,
        imdb: str,
        Статус просмотра: bool,
        Забраковано: bool """
        self.sheet.append_row( movie.get_to_table_record_format() )

    def get_not_watch_movie_list(self) -> List:
        """получение не просмотренных фильмов, отсчитываются первые 3 столбца"""
        all_data = self.sheet.get_all_records()
        result = []
        for i in all_data:
            if i.get("Статус просмотра") == "False" and i.get("Забраковано") == "None":
                stop = 0
                for j in i.items():
                    result.append(f"{j[0]}: {j[1]} ")
                    stop += 1
                    if stop == 3: break
                result.append("\n\n")
        return result

    def put_watch_mark(self, movie_name: str) -> bool:
        all_data = self.sheet.get_all_records()
        for row, value in enumerate(all_data, start=2):
            if value.get("Статус просмотра") == "False" and value.get("Фильм") == movie_name:
                self.sheet.update_cell(row, 4, "'True")
                return True
        return False

    def put_block_mark(self, movie_name: str) -> bool:
        all_data = self.sheet.get_all_records()
        for row, value in enumerate(all_data, start=2):
            if value.get("Забраковано") == "None" and value.get("Фильм") == movie_name:
                self.sheet.update_cell(row, 5, "'True")
                return True
        return False
