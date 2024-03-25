import json
from datetime import datetime

import newspaper


def build_source(url: str):
    output = newspaper.build(url, language="tr", memoize_articles=False)
    return output


def download_and_parse_article(article:newspaper.article.Article):
    article.download()
    article.parse()
    return 0


def test_metadata(article:newspaper.article.Article):
    download_and_parse_article(article)
    metadata = article.meta_data
    has_title = isinstance(article.title, str)
    has_description = isinstance(article.meta_description, str)
    has_text = isinstance(article.text, str)
    has_url = isinstance(article.url, str)
    has_img_url = isinstance(article.meta_img, str)
    has_date = 'dateModified' in metadata
    return has_title & has_description & has_text &\
        has_url & has_img_url & has_date


def get_data(article: newspaper.article.Article, publisher: str):
    download_and_parse_article(article)
    metadata_date = article.meta_data["dateModified"]
    article_date = datetime.strptime(metadata_date, '%Y-%m-%dT%H:%M:%S%z')
    output = {
        "title": article.title,
        "description": article.meta_description,
        "text": article.text,
        "url": article.url,
        "img_url": article.meta_img,
        "publishing_date": article_date,
        "publisher": publisher,
    }
    return output


# 10 most visited Turkish news sites
# https://tr.b2press.com/haber-siteleri
# 2024-03-24
news_sites = {
    "hurriyet": "https://www.hurriyet.com.tr",
    "mynet": "https://www.mynet.com", # Failed test
    "sozcu": "https://www.sozcu.com.tr",
    "milliyet": "https://www.milliyet.com.tr",
    "sabah": "https://www.sabah.com.tr", # Failed test
    "haberturk": "https://www.haberturk.com",
    "yenicag": "https://www.yenicaggazetesi.com.tr",
    "cumhuriyet": "https://www.cumhuriyet.com.tr",
    "haberler": "https://www.haberler.com",
    "onedio": "https://www.onedio.com", # Failed test
}

for site, url in news_sites.items():
    match site:
        case "mynet" | "sabah" | "onedio":
            print("Skipped")
        case _:
            print("All good!")

