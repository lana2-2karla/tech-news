import requests
import time
from parsel import Selector


def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(
            url, {"user-agent": "Fake user-agent"}, timeout=3
        )
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.ReadTimeout:
        return None


def scrape_novidades(html_content):
    if html_content == "":
        return []
    else:
        selector = Selector(text=html_content)
        links = selector.css(
            ".entry-thumbnail a::attr(href)"
        ).getall()
        return links


def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    return selector.css(".next::attr(href)").get()


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
