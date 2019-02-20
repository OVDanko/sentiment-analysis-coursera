import pandas as pd
from fake_useragent import UserAgent
import random
import requests
import bs4
from multiprocessing import Pool
import codecs
import functools

def getText(parent):
    return ''.join(parent.find_all(text=True, recursive=False)).strip()

def parse_page(sm_link, proxy_list):
    req = 0
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
        plus = parser.find('div', attrs={'class': "review-plus"}).text
        minus = parser.find('div', attrs={'class': "review-minus"}).text
        print('done: ', sm_link)
        with codecs.open('responses_texts_short.txt', 'a', 'utf-8') as output_file:
            output_file.write('1,' + str(plus) + '\n')
            output_file.write('0,' + str(minus) + '\n')
        return (plus, minus)

if __name__ == '__main__':
    with open("responses.txt", "r") as f:
        url_list = f.read().splitlines()

    proxies = pd.read_csv('proxies.csv', sep='\t', dtype=str)
    proxy_list = []
    for i in range(len(proxies)):
        address = proxies["IP Address"].values[i] + ':' + proxies["Port"].values[i]
        proxy_list.append({"http": 'http://' + address, "https": 'https://' + address})

    random.shuffle(proxy_list)

    p = Pool(100)
    p.map(functools.partial(parse_page, proxy_list=proxy_list), url_list)
