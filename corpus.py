

def main():
    pass


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
