from newspaper import build


def build_source(url):
    paper = build(url, language='tr', memoize_articles=False)
    return paper


# 10 most visited Turkish news sites
# https://tr.b2press.com/haber-siteleri
# 2024-03-24
news_sites = {
    "hurriyet": "https://www.hurriyet.com.tr",
    "mynet": "https://www.mynet.com",
    "sozcu": "https://www.sozu.com.tr",
    "milliyet": "https://www.milliyet.com.tr",
    "sabah": "https://www.sabah.com.tr",
    "haberturk": "https://www.haberturk.com",
    "yenicag": "https://www.yenicaggazetesi.com.tr",
    "cumhuriyet": "https://www.cumhuriyet.com.tr",
    "haberler": "https://www.haberler.com",
    "onedio": "https://www.onedio.com",
}

