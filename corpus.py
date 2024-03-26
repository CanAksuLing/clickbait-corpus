import datetime
import newspaper
# import json


def build_source(url: str) -> newspaper.Source:
    output = newspaper.build(url, language="tr", memoize_articles=False)
    return output


def download_and_parse_article(article: newspaper.article.Article) -> None:
    if article.download_state == 0:
        article.download()
        download_and_parse_article(article)
    elif article.is_parsed is False:
        article.parse()


def test_metadata(article: newspaper.article.Article) -> bool:
    download_and_parse_article(article)
    has_title = isinstance(article.title, str)
    has_description = isinstance(article.meta_description, str)
    has_text = isinstance(article.text, str)
    has_url = isinstance(article.url, str)
    has_img_url = isinstance(article.meta_img, str)
    has_date = isinstance(article.publish_date, datetime.datetime)
    return has_title & has_description & has_text &\
        has_url & has_img_url & has_date


def get_metadata(article: newspaper.article.Article, publisher: str) -> dict:
    download_and_parse_article(article)
    # metadata_date = article.meta_data["dateModified"]
    # article_date = datetime.strptime(metadata_date, '%Y-%m-%dT%H:%M:%S%z')
    output = {
        "title": article.title,
        "description": article.meta_description,
        "text": article.text,
        "url": article.url,
        "img_url": article.meta_img,
        "publishing_date": article.publish_date,
        "publisher": publisher,
    }
    return output


# 10 most visited Turkish news sites
# https://tr.b2press.com/haber-siteleri
# 2024-03-24
NEWS_SITES = {
    "hurriyet": "https://www.hurriyet.com.tr",
    "mynet": "https://www.mynet.com",  # Failed test
    "sozcu": "https://www.sozcu.com.tr",
    "milliyet": "https://www.milliyet.com.tr",
    "sabah": "https://www.sabah.com.tr",  # Failed test
    "haberturk": "https://www.haberturk.com",
    "yenicag": "https://www.yenicaggazetesi.com.tr",
    "cumhuriyet": "https://www.cumhuriyet.com.tr",
    "haberler": "https://www.haberler.com",
    "onedio": "https://www.onedio.com",  # Failed test
}
