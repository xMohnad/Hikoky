from hikoky.scrapers.sources.teamx import home_teamx, manga_teamx, chapter_teamx
from hikoky.scrapers.sources._3asq import home_3asq, manga_3asq, chapter_3asq

source_handlers = {
    "teamx": {
        "url": "https://www.teamxnovel.com/",
        "home_page": home_teamx,
        "manga_page": manga_teamx,
        "chapter_page": chapter_teamx
    },
    "3asq": {
        "url": "https://3asq.org/manga/",
        "home_page": home_3asq,
        "manga_page": manga_3asq,
        "chapter_page": chapter_3asq
    }
}

SECRET_KEY = 'your_secret_key_here'