import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://joblab.ru/search.php?r=vac&srprofecy=%EC%E5%F5%E0%ED%E8%EA&kw_w2=1&srzpmin=&srregion=50&srcity=77&srcategory=&submit=1'
ua = UserAgent()
headers = {'User-Agent': ua.chrome}

r = requests.get(url, headers=headers)
print(r.status_code)
time.sleep(5)
# print(r.text)

soup = BeautifulSoup(r.text, 'lxml')
links_all = soup.find_all('a')
for i in links_all:
    if '.html' in i.get('href'):
        print('https://joblab.ru' + i.get('href'))