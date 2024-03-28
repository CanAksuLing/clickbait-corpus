import newspaper
import json


def build_source(site_url):
    source = newspaper.build(site_url, language="tr")
    return source


def download_articles(news_list):
    newspaper.news_pool.set(news_list, threads_per_source=9)
    newspaper.news_pool.join()


def test_article(article: newspaper.article.Article) -> bool:
    # download_and_parse_article(article)
    if article.is_parsed:
        has_title = isinstance(article.title, str)
        has_description = isinstance(article.meta_description, str)
        has_text = isinstance(article.text, str)
        has_url = isinstance(article.url, str)
        has_img_url = isinstance(article.meta_img, str)
        has_date = isinstance(article.meta_data["dateModified"], str)
        not_media_news = article.is_media_news is False

        return has_title & has_description & has_text &\
            has_url & has_img_url & has_date & not_media_news &\
            article.is_valid_body()
    else:
        article.parse()
        test_article(article)


def get_metadata(article: newspaper.article.Article, publisher: str) -> dict:
    article.parse()
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


def main():
    hurriyet = build_source(NEWS_SITES['hurriyet'])
    sozcu = build_source(NEWS_SITES['sozcu'])
    milliyet = build_source(NEWS_SITES['milliyet'])
    haberturk = build_source(NEWS_SITES['haberturk'])
    yenicag = build_source(NEWS_SITES['yenicag'])
    cumhuriyet = build_source(NEWS_SITES['cumhuriyet'])
    haberlercom = build_source(NEWS_SITES['haberler.com'])
    haber7 = build_source(NEWS_SITES['haber7'])
    ntv = build_source(NEWS_SITES['ntv'])
    ensonhaber = build_source(NEWS_SITES['ensonhaber'])

    print("Sources built")

    news_sites = [hurriyet, sozcu, milliyet,
                  haberturk, yenicag, cumhuriyet,
                  haberlercom, haber7, ntv,
                  ensonhaber]

    download_articles(news_sites)

    print("Articles downloaded")

    for source in news_sites:
        for article in source.articles:
            if test_article(article):
                article_data = get_metadata(article,
                                            f'{source=}'.split('=')[0])
                with open('./news-data.json', 'a+') as file:
                    old_data = json.load(file)
                    old_data.append(article_data)
                    json.dump(old_data)
            else:
                continue


# 13 most visited Turkish news sites
# https://web.archive.org/web/20240326141026/https://tr.b2press.com/haber-siteleri
# mynet, sabah and onedio were skipped
# because newspaper3k couldn't retrieve
# the necessary metadata
# 2024-03-24
NEWS_SITES = {
    "hurriyet": "https://www.hurriyet.com.tr",        # #1  96/100
    # "mynet": "https://www.mynet.com",               # #2  0/100 will skip
    "sozcu": "https://www.sozcu.com.tr",              # #3  95/100
    "milliyet": "https://www.milliyet.com.tr",        # #4  93/100
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
