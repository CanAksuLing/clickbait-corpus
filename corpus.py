# import datetime
import newspaper
import json


def build_source(url: str) -> newspaper.Source:
    output = newspaper.build(url, language="tr", memoize_articles=False)
    return output


def download_and_parse_article(article: newspaper.article.Article) -> None:
    if article.download_state == 0:
        try:
            article.download()
        except newspaper.ArticleException:
            return None
        except Exception:
            download_and_parse_article(article)
        finally:
            download_and_parse_article(article)
    elif article.is_parsed is False:
        article.parse()


def test_metadata(article: newspaper.article.Article) -> bool:
    # download_and_parse_article(article)
    article.download()
    article.parse()
    has_title = isinstance(article.title, str)
    has_description = isinstance(article.meta_description, str)
    has_text = isinstance(article.text, str)
    has_url = isinstance(article.url, str)
    has_img_url = isinstance(article.meta_img, str)
    has_date = isinstance(article.meta_data["dateModified"], str)
    return has_title & has_description & has_text &\
        has_url & has_img_url & has_date


def get_metadata(article: newspaper.article.Article, publisher: str) -> dict:
    # download_and_parse_article(article)
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
            test_passed = validate_article(news_source.articles[i])
            if test_passed:
                number_of_passed_test += 1
            else:
                print(news_source.articles[i].url)
        print(f"{number_of_passed_test} out of {i} passed the test")
        print()


def validate_article(article: newspaper.article.Article) -> bool:
    metadata_criteria = test_metadata(article)
    download_and_parse_article(article)
    is_not_media_news = not article.is_media_news()
    validation = is_not_media_news & article.is_valid_body() &\
        metadata_criteria
    return validation


def retrieve_data(site_name, site_url) -> dict:
    data = []
    news_source = build_source(site_url)
    for article in news_source.articles:
        test_result = validate_article(article)
        if test_result:
            try:
                metadata = get_metadata(article, site_name)
            except newspaper.ArticleException:
                print("Something wrong happened. Skipping")
                continue
            finally:
                data.append(metadata)
        # else:
        #     print("An article didn't pass the test. Skipping.")
    return data


def main():
    data_to_be_output = []
    for news_site, news_site_url in NEWS_SITES.items():
        print(news_site)
        news_data = retrieve_data(news_site, news_site_url)
        data_to_be_output.append(news_data)
    with open("./headlines.json", "w") as file:
        file.write(json.dumps(data_to_be_output))


# 13 most visited Turkish news sites
# https://web.archive.org/web/20240326141026/https://tr.b2press.com/haber-siteleri
# mynet, sabah and onedio were skipped
# because newspaper3k couldn't retrieve
# the necessary metadata
# 2024-03-24
NEWS_SITES = {
    "milliyet": "https://www.milliyet.com.tr",        # #4  93/100
    "hurriyet": "https://www.hurriyet.com.tr",        # #1  96/100
    # "mynet": "https://www.mynet.com",               # #2  0/100 will skip
    "sozcu": "https://www.sozcu.com.tr",              # #3  95/100
    # "sabah": "https://www.sabah.com.tr",            # #5  1/100 will skip
    "haberturk": "https://www.haberturk.com",         # #6  98/100
    "yenicag": "https://www.yenicaggazetesi.com.tr",  # #7  100/100
    "cumhuriyet": "https://www.cumhuriyet.com.tr",    # #8  74/100
    "haberler.com": "https://www.haberler.com",       # #9  100/100
    # "onedio": "https://www.onedio.com",             # #10 0/100 will skip
    "haber7": "https://www.haber7.com",               # #11 91/100
    "ntv": "https://www.ntv.com.tr",                  # #12 100/100
    "ensonhaber": "https://www.ensonhaber.com"        # #13 98/100
}

if __name__ == '__main__':
    main()
