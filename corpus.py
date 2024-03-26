# import datetime
import newspaper
import json


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
    has_date = isinstance(article.meta_data["dateModified"], str)
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
        "publishing_date": article.meta_data["dateModified"],
        "publisher": publisher,
    }
    return output


def test():
    for site_url in NEWS_SITES.values():
        news_source = build_source(site_url)
        print(site_url)
        number_of_passed_test = 0
        for i in range(101):
            test_passed = str(test_metadata(news_source.articles[i]))
            if test_passed == "True":
                # print(test_passed)
                number_of_passed_test += 1
            else:
                # print(f"{test_passed} {news_source.articles[i].url}")
                pass
        print(f"{number_of_passed_test} out of {i} passed the test")
        print()


def retrieval_test():
    data = []
    for site_name, site_url in NEWS_SITES.items():
        match site_name:
            case "mynet" | "sabah" | "onedio":
                continue
            case _:
                news_source = build_source(site_url)
                for i in range(101):
                    try:
                        metadata = get_metadata(news_source.articles[i],
                                                site_name)
                    except Exception:
                        print("Something wrong happened. Skipping")
                        continue
                    else:
                        data.append(metadata)
    with open("./test_data.json", "w") as file:
        file.write(json.dumps(data, indent=4))


# 13 most visited Turkish news sites
# https://web.archive.org/web/20240326141026/https://tr.b2press.com/haber-siteleri
# mynet, sabah and onedio were skipped
# because newspaper3k couldn't retrieve
# the necessary metadata
# 2024-03-24
NEWS_SITES = {
    "hurriyet": "https://www.hurriyet.com.tr",        # #1  96/100
    "mynet": "https://www.mynet.com",                 # #2  0/100 will skip
    "sozcu": "https://www.sozcu.com.tr",              # #3  95/100
    "milliyet": "https://www.milliyet.com.tr",        # #4  93/100
    "sabah": "https://www.sabah.com.tr",              # #5  1/100 will skip
    "haberturk": "https://www.haberturk.com",         # #6  98/100
    "yenicag": "https://www.yenicaggazetesi.com.tr",  # #7  100/100
    "cumhuriyet": "https://www.cumhuriyet.com.tr",    # #8  74/100
    "haberler": "https://www.haberler.com",           # #9  100/100
    "onedio": "https://www.onedio.com",               # #10 0/100 will skip
    "haber7": "https://www.haber7.com",               # #11 91/100
    "ntv": "https://www.ntv.com.tr",                  # #12 100/100
    "ensonhaber": "https://www.ensonhaber.com"        # #13 98/100
}
