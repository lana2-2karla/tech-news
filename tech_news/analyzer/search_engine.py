from tech_news.database import search_news


def search_by_title(title):
    news_list = search_news({"title": {"$regex": title, "$options": "i"}})
    return [(news["title"], news["url"]) for news in news_list]


def search_by_date(date_iso):
    try:
        date = date_iso.split("-")
        date_formated = f"{date[2]}/{date[1]}/{date[0]}"

        news_list = search_news({"timestamp": date_formated})
        return [(news["title"], news["url"]) for news in news_list]

    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
