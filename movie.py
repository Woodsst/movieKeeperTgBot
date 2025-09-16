import datetime

from pydantic import BaseModel


class Movie(BaseModel):
    """
    Модель фильма
    """
    date: datetime.date
    name: str
    link: str
    watch_status: bool | None = None
    block: bool | None = None

    def get_to_table_record_format(self):
        return [self.name,
             str(self.date),
             self.link,
             str(self.watch_status),
             str(self.block),]

def movie_valid(movie: str, link: str) -> Movie | bool:
    try:
        return Movie(date=datetime.date.today(), name=movie, link=link, watch_status=False)
    except Exception:
        return False
