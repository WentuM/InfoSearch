from string import Formatter
import requests

BASE_URL = 'https://www.liveinternet.ru/rating/today.tsv?;page={page}'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

LOADS_PACKAGE_NAME = 'loads'
TASK1_PACKAGE_NAME = 'task1'

index_file = open(TASK1_PACKAGE_NAME + '/' + "index.txt", "w", encoding="utf-8")


def print_hi(name):
    sites_count = 0
    i = 0
    while sites_count < 100:
        try:
            i += 1
            print('page ' + str(i))
            url = get_url_for_page(i)
            pages_response = requests.get(url, headers=HEADERS)
            urls = list(
                map(lambda item: 'http://' + item.split("\t")[1].replace("/", ""),
                    pages_response.text.split("\n")[1:30]))
            print(urls)
        except Exception:
            continue
        try:
            for url in urls:
                page_response = requests.get(url, headers=HEADERS)
                filename = TASK1_PACKAGE_NAME + '/' + LOADS_PACKAGE_NAME + '/' + "выкачка-" + url.replace('/',
                                                                                                          '') + ".txt"
                vikachka_file = open(filename, "w", encoding="utf-8")
                vikachka_file.write(page_response.text)
                vikachka_file.close()
                index_file.write(str(sites_count) + '.' + url + "\n")
                sites_count += 1

        except Exception:
            continue

    index_file.close()


def get_url_for_page(page: int) -> str:
    return Formatter().format(BASE_URL, page=str(page))


if __name__ == '__main__':
    print_hi('PyCharm')
