import pandas as pd
from fake_useragent import UserAgent
import random
import requests
import bs4
from multiprocessing import Pool
import codecs
from functools import reduce
import functools

def rotate(some_list):
    return some_list[1:] + some_list[:1]

def parse_page(sm_link, proxy_list):
    req = 0
    random.shuffle(proxy_list)
    for k in range(20):
        random.shuffle(proxy_list)
        ua = UserAgent()
        agent = ua.random
        try:
            req = requests.get(sm_link, headers={'User-Agent': agent}, proxies=proxy_list[0])
        except requests.exceptions.RequestException as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            if (req.status_code == 200):
                break


    if (type(req) is int): # если ни один запрос не удался
        print('err1: ', sm_link)
        return []
    elif (req.status_code != 200) : # если получили запрос с ошибкой
        print('err2: ', sm_link)
        return []
    else:
        parser = bs4.BeautifulSoup(req.text, 'lxml')
        x = parser.findAll('a', attrs={'class': 'review-btn review-read-link'})
        print('done: ', sm_link)
        with codecs.open('responses.txt', 'a', 'utf-8') as output_file:
            for item in x:
                output_file.write("%s\n" % item)
        return (plus, minus)


if __name__ == '__main__':
    url_smartphones = ['http://otzovik.com/technology/communication/cellular_phones/' + str(n) for n in range(1, 209)]

    smartphone_links = []
    for url in url_smartphones:
        req = requests.get(url)
        parser = bs4.BeautifulSoup(req.text, 'lxml')
        x = parser.findAll('a', attrs={'class': 'reviews-counter'})
        for item in x:
            smartphone_links.append(item['href'])

    proxies = pd.read_csv('proxies.csv', sep='\t', dtype=str)
    proxy_list = []
    for i in range(len(proxies)):
        address = proxies["IP Address"].values[i] + ':' + proxies["Port"].values[i]
        proxy_list.append({"http": 'http://' + address, "https": 'https://' + address})

    review_links = []
    random.shuffle(proxy_list)

    p = Pool(100)
    url_list = smartphone_links

    map_results = p.map(functools.partial(parse_page, proxy_list=proxy_list), url_list)
    reduce_results = reduce(lambda x, y: x + y, map_results)

    with codecs.open('responses.txt', 'a', 'utf-8') as output_file:
        output_file.write('\n'.join(reduce_results))