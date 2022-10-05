import requests
import time
from parsel import Selector
from tech_news.database import create_news


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
        links = selector.css(".entry-thumbnail a::attr(href)").getall()
        return links


def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    return selector.css(".next::attr(href)").get()


def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    info_news = {
        "url": selector.css("link[rel=canonical]::attr(href)").get(),
        "title": selector.css("h1.entry-title::text").get().strip(),
        "timestamp": selector.css("li.meta-date::text").get(),
        "writer": selector.css(".author ::text").get(),
        "comments_count": len(selector.css("ol.comment-list").getall()) or 0,
        "summary": "".join(
            selector.css(".entry-content > p:nth-of-type(1) ::text").getall()
        ).strip(),
        "tags": selector.css("a[rel=tag]::text").getall(),
        "category": selector.css("span.label::text").get(),
    }
    return info_news


def get_tech_news(amount):
    url = "https://blog.betrybe.com"

    info_news_list = []

    while len(info_news_list) < amount:
        html_page = fetch(url)
        links = scrape_novidades(html_page)

        for link in links:
            # if len(info_news_list) == amount:
            #     break
            html_new_page = fetch(link)
            info_new_page = scrape_noticia(html_new_page)
            info_news_list.append(info_new_page)

        url = scrape_next_page_link(html_new_page)

    create_news(info_news_list[:amount])
    return info_news_list[:amount]
